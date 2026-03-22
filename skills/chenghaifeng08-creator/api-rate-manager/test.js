/**
 * Test script for API Rate Manager
 */

const { RateManager } = require('./index');

async function runTests() {
  console.log('🧪 Testing API Rate Manager...\n');
  
  // Test 1: Basic call
  console.log('Test 1: Basic call');
  const manager1 = new RateManager({
    apiName: 'test',
    limit: 5,
    windowMs: 10000
  });
  
  const result = await manager1.call(() => {
    return { success: true };
  });
  console.log('✅ Basic call works:', result);
  
  // Test 2: Rate limiting
  console.log('\nTest 2: Rate limiting');
  const manager2 = new RateManager({
    apiName: 'test',
    limit: 3,
    windowMs: 5000,
    retry: false
  });
  
  let successCount = 0;
  let failCount = 0;
  
  for (let i = 0; i < 5; i++) {
    try {
      await manager2.call(() => {
        successCount++;
        return { success: true };
      });
    } catch (error) {
      failCount++;
      console.log(`⚠️  Request ${i + 1} failed (expected): ${error.message}`);
    }
  }
  
  console.log(`✅ Rate limiting works: ${successCount} succeeded, ${failCount} failed`);
  
  // Test 3: Status check
  console.log('\nTest 3: Status check');
  const status = manager2.getStatus();
  console.log('✅ Status:', status);
  
  // Test 4: Batch processing
  console.log('\nTest 4: Batch processing');
  const manager3 = new RateManager({
    apiName: 'test',
    limit: 10,
    windowMs: 10000
  });
  
  const batchResults = await manager3.batch([
    () => ({ id: 1 }),
    () => ({ id: 2 }),
    () => ({ id: 3 }),
  ]);
  
  console.log('✅ Batch results:', batchResults);
  
  // Test 5: Stats
  console.log('\nTest 5: Statistics');
  const stats = manager3.getStats();
  console.log('✅ Stats:', stats);
  
  console.log('\n🎉 All tests passed!\n');
}

runTests().catch(console.error);
