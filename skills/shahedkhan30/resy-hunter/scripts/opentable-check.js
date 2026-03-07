#!/usr/bin/env node
// opentable-check.js — Query OpenTable availability using Playwright
// Usage: node opentable-check.js <restaurant_id> <date> <party_size> [time]
// Output: JSON with restaurant info and available slots
//
// Auto-logs in with OPENTABLE_EMAIL + OPENTABLE_PASSWORD.
// Session is persisted to .playwright-state/opentable.json for reuse.

const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');

const SKILL_DIR = path.join(process.env.HOME, '.openclaw/skills/resy-hunter');
const STATE_DIR = path.join(SKILL_DIR, '.playwright-state');
const STATE_FILE = path.join(STATE_DIR, 'opentable.json');

async function main() {
  const args = process.argv.slice(2);
  if (args.length < 3) {
    console.error(JSON.stringify({ error: 'Usage: opentable-check.js <restaurant_id> <date> <party_size> [time]' }));
    process.exit(1);
  }

  const restaurantId = args[0];
  const date = args[1];
  const partySize = parseInt(args[2], 10);
  const time = args[3] || '19:00';

  const email = process.env.OPENTABLE_EMAIL;
  const password = process.env.OPENTABLE_PASSWORD;

  if (!email || !password) {
    console.error(JSON.stringify({ error: 'OPENTABLE_EMAIL and OPENTABLE_PASSWORD must be set' }));
    process.exit(1);
  }

  // Ensure state directory exists
  fs.mkdirSync(STATE_DIR, { recursive: true });

  let browser;
  try {
    // Launch with persistent storage state if it exists
    const launchOpts = {
      headless: true,
      args: [
        '--disable-blink-features=AutomationControlled',
        '--no-sandbox',
      ],
    };

    browser = await chromium.launch(launchOpts);

    // Create context with saved state if available
    const contextOpts = {
      userAgent: 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
      viewport: { width: 1280, height: 800 },
    };

    if (fs.existsSync(STATE_FILE)) {
      try {
        contextOpts.storageState = STATE_FILE;
      } catch (e) {
        // Corrupted state file, ignore
      }
    }

    const context = await browser.newContext(contextOpts);
    const page = await context.newPage();

    // Collect availability data from network responses
    let availabilityData = null;

    page.on('response', async (response) => {
      const url = response.url();
      // Intercept availability API responses
      if (url.includes('/availability') || url.includes('/dtp') || url.includes('timeslots')) {
        try {
          const contentType = response.headers()['content-type'] || '';
          if (contentType.includes('json') && response.status() === 200) {
            const data = await response.json();
            if (!availabilityData) {
              availabilityData = data;
            }
          }
        } catch (e) {
          // Non-JSON response, skip
        }
      }
    });

    // Build the OpenTable URL
    const dateTime = `${date}T${time}`;
    const otUrl = `https://www.opentable.com/restref/client/?rid=${restaurantId}&restref=${restaurantId}&datetime=${dateTime}&covers=${partySize}&searchdatetime=${dateTime}&partysize=${partySize}`;

    await page.goto(otUrl, { waitUntil: 'domcontentloaded', timeout: 30000 });

    // Check if we need to log in
    const needsLogin = await detectLoginWall(page);

    if (needsLogin) {
      await performLogin(page, email, password);
      // Save session state after login
      await context.storageState({ path: STATE_FILE });
      // Navigate again to the availability page after login
      await page.goto(otUrl, { waitUntil: 'domcontentloaded', timeout: 30000 });
    }

    // Wait for availability to load
    await page.waitForTimeout(5000);

    // Try to extract slots from the page DOM as a fallback
    let slots = [];

    if (availabilityData) {
      slots = parseAvailabilityResponse(availabilityData, date);
    }

    if (slots.length === 0) {
      // Fallback: extract from DOM
      slots = await extractSlotsFromDOM(page, date);
    }

    // Save state for next run
    try {
      await context.storageState({ path: STATE_FILE });
    } catch (e) {
      // Non-critical
    }

    // Build output
    const output = {
      platform: 'opentable',
      restaurant_id: restaurantId,
      date: date,
      party_size: partySize,
      slots: slots,
      url: `https://www.opentable.com/restref/client/?rid=${restaurantId}&restref=${restaurantId}&datetime=${dateTime}&covers=${partySize}`,
    };

    console.log(JSON.stringify(output, null, 2));
  } catch (err) {
    console.error(JSON.stringify({
      error: `OpenTable check failed: ${err.message}`,
      platform: 'opentable',
      restaurant_id: restaurantId,
      date: date,
      party_size: partySize,
      slots: [],
    }));
    process.exit(1);
  } finally {
    if (browser) await browser.close();
  }
}

async function detectLoginWall(page) {
  try {
    // Check for common login indicators
    const loginButton = await page.$('button[data-test="login-button"], a[href*="login"], #login-button, [data-test="sign-in"]');
    if (loginButton) return true;

    // Check for login form
    const loginForm = await page.$('input[type="email"], input[name="email"], #Email');
    const isOnLoginPage = page.url().includes('login') || page.url().includes('signin');
    if (loginForm && isOnLoginPage) return true;

    // Check if page redirected to login
    if (page.url().includes('/auth/') || page.url().includes('/login')) return true;

    return false;
  } catch (e) {
    return false;
  }
}

async function performLogin(page, email, password) {
  try {
    // Navigate to login page if not already there
    if (!page.url().includes('login') && !page.url().includes('signin')) {
      // Try clicking a sign-in link
      const signInLink = await page.$('a[href*="login"], a[href*="signin"], button:has-text("Sign in"), button:has-text("Log in")');
      if (signInLink) {
        await signInLink.click();
        await page.waitForTimeout(2000);
      } else {
        await page.goto('https://www.opentable.com/login', { waitUntil: 'domcontentloaded', timeout: 15000 });
      }
    }

    // Wait for email input
    await page.waitForSelector('input[type="email"], input[name="email"], #Email', { timeout: 10000 });

    // Fill email
    const emailInput = await page.$('input[type="email"], input[name="email"], #Email');
    if (emailInput) {
      await emailInput.fill(email);
    }

    // Look for a "Continue" or "Next" button before password
    const continueBtn = await page.$('button:has-text("Continue"), button:has-text("Next"), button[type="submit"]');
    if (continueBtn) {
      await continueBtn.click();
      await page.waitForTimeout(2000);
    }

    // Fill password
    await page.waitForSelector('input[type="password"], input[name="password"], #Password', { timeout: 10000 });
    const passwordInput = await page.$('input[type="password"], input[name="password"], #Password');
    if (passwordInput) {
      await passwordInput.fill(password);
    }

    // Submit login
    const submitBtn = await page.$('button:has-text("Sign in"), button:has-text("Log in"), button[type="submit"]');
    if (submitBtn) {
      await submitBtn.click();
    }

    // Wait for login to complete (navigation or state change)
    await page.waitForTimeout(5000);

    // Verify login succeeded
    const stillOnLogin = page.url().includes('login') || page.url().includes('signin');
    if (stillOnLogin) {
      const errorEl = await page.$('[class*="error"], [data-test*="error"], .alert-danger');
      if (errorEl) {
        const errorText = await errorEl.textContent();
        throw new Error(`Login failed: ${errorText}`);
      }
    }
  } catch (err) {
    throw new Error(`OpenTable login failed: ${err.message}`);
  }
}

function parseAvailabilityResponse(data, date) {
  const slots = [];

  try {
    // OpenTable API returns availability in various formats
    // Try common response structures

    // Format 1: data.availability[]
    if (data.availability && Array.isArray(data.availability)) {
      for (const slot of data.availability) {
        const timeStr = slot.datetime || slot.time || slot.dateTime;
        if (timeStr) {
          slots.push({
            time_start: timeStr,
            type: slot.type || slot.areaName || 'Standard',
          });
        }
      }
    }

    // Format 2: data.times[]
    if (data.times && Array.isArray(data.times)) {
      for (const slot of data.times) {
        slots.push({
          time_start: slot.dateTime || slot.time || `${date}T${slot.timeString}`,
          type: slot.type || slot.experienceType || 'Standard',
        });
      }
    }

    // Format 3: data.data.availability or nested
    if (data.data) {
      const nested = data.data.availability || data.data.times || data.data.timeslots;
      if (Array.isArray(nested)) {
        for (const slot of nested) {
          const timeStr = slot.datetime || slot.dateTime || slot.time;
          if (timeStr) {
            slots.push({
              time_start: timeStr,
              type: slot.type || slot.areaName || 'Standard',
            });
          }
        }
      }
    }

    // Format 4: Check for slot objects in root
    if (data.timeslots && Array.isArray(data.timeslots)) {
      for (const slot of data.timeslots) {
        slots.push({
          time_start: slot.dateTime || slot.time,
          type: slot.experienceType || slot.type || 'Standard',
        });
      }
    }
  } catch (e) {
    // Parsing failed, return empty
  }

  return slots;
}

async function extractSlotsFromDOM(page, date) {
  const slots = [];

  try {
    // Extract time slots from DOM elements
    const slotData = await page.evaluate((targetDate) => {
      const results = [];

      // Look for time slot buttons/links
      const timeElements = document.querySelectorAll(
        '[data-test*="time"], [class*="timeslot"], [class*="time-slot"], ' +
        'button[class*="slot"], a[class*="slot"], ' +
        '[data-test="availability-time"], [class*="TimeSlot"], ' +
        'button[data-time], [data-timeslot]'
      );

      for (const el of timeElements) {
        const timeText = el.textContent?.trim();
        const dataTime = el.getAttribute('data-time') || el.getAttribute('data-timeslot') || el.getAttribute('data-datetime');

        if (timeText || dataTime) {
          // Parse time from text like "7:30 PM"
          let time = dataTime || '';
          if (!time && timeText) {
            const match = timeText.match(/(\d{1,2}):(\d{2})\s*(AM|PM)/i);
            if (match) {
              let hours = parseInt(match[1]);
              const mins = match[2];
              const period = match[3].toUpperCase();
              if (period === 'PM' && hours !== 12) hours += 12;
              if (period === 'AM' && hours === 12) hours = 0;
              time = `${targetDate}T${String(hours).padStart(2, '0')}:${mins}`;
            }
          }

          if (time) {
            // Get the area/type from parent or sibling
            const parent = el.closest('[class*="area"], [class*="section"], [data-test*="area"]');
            const type = parent?.getAttribute('data-area') || parent?.querySelector('[class*="area-name"], [class*="section-title"]')?.textContent?.trim() || 'Standard';

            results.push({
              time_start: time,
              type: type,
            });
          }
        }
      }

      // Deduplicate
      const seen = new Set();
      return results.filter((s) => {
        const key = s.time_start;
        if (seen.has(key)) return false;
        seen.add(key);
        return true;
      });
    }, date);

    slots.push(...slotData);
  } catch (e) {
    // DOM extraction failed
  }

  return slots;
}

main();
