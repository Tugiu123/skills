/**
 * API Rate Manager
 * Smart rate limit management with auto-retry and queuing
 */

class RateManager {
  constructor(options = {}) {
    this.apiName = options.apiName || 'default';
    this.limit = options.limit || 100;
    this.windowMs = options.windowMs || 60000;
    this.retry = options.retry !== false;
    this.maxRetries = options.maxRetries || 5;
    this.queueSize = options.queueSize || 100;
    this.onLimitHit = options.onLimitHit || null;
    this.onRetry = options.onRetry || null;
    
    // State
    this.requests = [];
    this.queue = [];
    this.stats = {
      totalCalls: 0,
      successfulCalls: 0,
      retries: 0,
      rateLimitsHit: 0,
      averageWaitTime: 0
    };
  }
  
  /**
   * Get current rate limit status
   */
  getStatus() {
    const now = Date.now();
    const windowStart = now - this.windowMs;
    const recentRequests = this.requests.filter(t => t > windowStart);
    const remaining = Math.max(0, this.limit - recentRequests.length);
    const resetIn = recentRequests.length > 0 
      ? (recentRequests[0] + this.windowMs) - now 
      : 0;
    
    return {
      remaining,
      limit: this.limit,
      resetIn: Math.max(0, resetIn),
      queued: this.queue.length,
      apiName: this.apiName
    };
  }
  
  /**
   * Check if rate limit is exceeded
   */
  isRateLimited() {
    const status = this.getStatus();
    return status.remaining === 0;
  }
  
  /**
   * Wait for specified milliseconds
   */
  sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
  }
  
  /**
   * Execute a function with rate limit protection
   */
  async call(fn, attempt = 1) {
    this.stats.totalCalls++;
    
    // Check rate limit
    if (this.isRateLimited()) {
      this.stats.rateLimitsHit++;
      
      const status = this.getStatus();
      
      // Notify callback
      if (this.onLimitHit) {
        this.onLimitHit(status);
      }
      
      // Retry logic
      if (this.retry && attempt <= this.maxRetries) {
        this.stats.retries++;
        
        // Notify retry callback
        if (this.onRetry) {
          this.onRetry(attempt, this.maxRetries);
        }
        
        // Wait for reset
        const waitTime = status.resetIn || 1000;
        await this.sleep(waitTime);
        
        // Record wait time for stats
        this.stats.averageWaitTime = 
          (this.stats.averageWaitTime * (this.stats.retries - 1) + waitTime) / this.stats.retries;
        
        // Retry
        return this.call(fn, attempt + 1);
      }
      
      // Queue the request if not retrying
      if (this.queue.length < this.queueSize) {
        return new Promise((resolve, reject) => {
          this.queue.push({ fn, resolve, reject, attempt });
        });
      }
      
      throw new Error(`Rate limit exceeded for ${this.apiName} after ${attempt} attempts`);
    }
    
    // Record this request
    this.requests.push(Date.now());
    
    // Execute the function
    try {
      const result = await fn();
      this.stats.successfulCalls++;
      return result;
    } catch (error) {
      throw error;
    }
  }
  
  /**
   * Execute multiple functions with rate limit protection
   */
  async batch(fns) {
    const results = [];
    
    for (const fn of fns) {
      try {
        const result = await this.call(fn);
        results.push({ success: true, result });
      } catch (error) {
        results.push({ success: false, error: error.message });
      }
    }
    
    return results;
  }
  
  /**
   * Process queued requests
   */
  async processQueue() {
    while (this.queue.length > 0 && !this.isRateLimited()) {
      const { fn, resolve, reject, attempt } = this.queue.shift();
      
      try {
        const result = await this.call(fn, attempt);
        resolve(result);
      } catch (error) {
        reject(error);
      }
    }
  }
  
  /**
   * Start queue processor
   */
  startQueueProcessor(intervalMs = 5000) {
    setInterval(() => {
      this.processQueue();
    }, intervalMs);
  }
  
  /**
   * Get usage statistics
   */
  getStats() {
    return {
      ...this.stats,
      status: this.getStatus()
    };
  }
  
  /**
   * Reset rate limit counters
   */
  reset() {
    this.requests = [];
    this.queue = [];
    this.stats = {
      totalCalls: 0,
      successfulCalls: 0,
      retries: 0,
      rateLimitsHit: 0,
      averageWaitTime: 0
    };
  }
}

module.exports = { RateManager };
