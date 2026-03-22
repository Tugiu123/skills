/**
 * Social Content Pro - Test Suite
 */

const { SocialContentPro } = require('../index');

function assert(condition, message) {
  if (!condition) {
    throw new Error(`❌ ASSERTION FAILED: ${message}`);
  }
  console.log(`✅ ${message}`);
}

async function runTests() {
  console.log('\n🧪 Running Social Content Pro Tests...\n');
  
  const creator = new SocialContentPro({
    niche: 'crypto trading',
    platforms: ['twitter', 'instagram'],
    tone: 'professional'
  });

  try {
    // Test 1: Generate Ideas
    console.log('Test 1: Generate Content Ideas');
    const ideas = await creator.generateIdeas({ count: 5 });
    assert(Array.isArray(ideas), 'Ideas is an array');
    assert(ideas.length > 0, 'Has ideas');
    if (ideas.length > 0) {
      const idea = ideas[0];
      assert(idea.title, 'Has title');
      assert(idea.platform, 'Has platform');
      assert(idea.hook, 'Has hook');
      assert(typeof idea.viralScore === 'number', 'Has viral score');
      console.log(`   Generated ${ideas.length} ideas, best viral score: ${Math.max(...ideas.map(i => i.viralScore))}\n`);
    }

    // Test 2: Create Post
    console.log('Test 2: Create Platform-Specific Post');
    const post = await creator.createPost({
      topic: 'Bitcoin halving explained',
      platform: 'twitter',
      format: 'thread'
    });
    assert(post.platform === 'twitter', 'Platform is twitter');
    assert(post.content, 'Has content');
    assert(Array.isArray(post.hashtags), 'Has hashtags');
    console.log(`   Created ${post.format} with ${post.characterCount} chars\n`);

    // Test 3: Get Hashtags
    console.log('Test 3: Get Viral Hashtags');
    const hashtags = await creator.getHashtags({
      niche: 'crypto',
      platform: 'instagram',
      count: 15
    });
    assert(Array.isArray(hashtags.hashtags), 'Hashtags is array');
    assert(hashtags.hashtags.length > 0, 'Has hashtag data');
    assert(hashtags.recommended, 'Has recommendations');
    console.log(`   Got ${hashtags.hashtags.length} hashtags, recommended: ${hashtags.recommended.length}\n`);

    // Test 4: Plan Calendar
    console.log('Test 4: Plan Content Calendar');
    const calendar = await creator.planCalendar({
      days: 7,
      postsPerDay: 2,
      platforms: ['twitter', 'instagram']
    });
    assert(calendar.calendar, 'Has calendar');
    assert(calendar.calendar.length === 7, '7 days planned');
    assert(calendar.totalPosts === 14, '14 posts total');
    console.log(`   Planned ${calendar.totalPosts} posts over ${calendar.calendar.length} days\n`);

    // Test 5: Get Analytics
    console.log('Test 5: Get Analytics');
    const analytics = await creator.getAnalytics({
      platform: 'twitter',
      period: '30d'
    });
    assert(typeof analytics.totalPosts === 'number', 'Has total posts');
    assert(typeof analytics.engagementRate === 'number', 'Has engagement rate');
    assert(Array.isArray(analytics.recommendations), 'Has recommendations');
    console.log(`   ${analytics.totalPosts} posts, ${analytics.engagementRate}% engagement\n`);

    // Test 6: Analyze Competitor
    console.log('Test 6: Analyze Competitor');
    const competitor = await creator.analyzeCompetitor({
      username: '@competitor',
      platform: 'twitter',
      period: '30d'
    });
    assert(competitor.username, 'Has username');
    assert(typeof competitor.followerCount === 'number', 'Has follower count');
    assert(Array.isArray(competitor.topPosts), 'Has top posts');
    assert(Array.isArray(competitor.insights), 'Has insights');
    console.log(`   Analyzed ${competitor.username}, ${competitor.followerCount} followers\n`);

    // Test 7: Schedule Post
    console.log('Test 7: Schedule Post');
    const schedule = await creator.schedulePost({
      content: 'Test post content',
      platform: 'twitter',
      autoOptimize: true
    });
    assert(schedule.success, 'Schedule successful');
    assert(schedule.schedule, 'Has schedule data');
    assert(schedule.schedule.status === 'scheduled', 'Status is scheduled');
    console.log(`   Post scheduled for ${schedule.schedule.scheduledTime}\n`);

    // Test 8: Platform Config
    console.log('Test 8: Platform Configuration');
    assert(creator.platformConfig.twitter, 'Twitter config exists');
    assert(creator.platformConfig.instagram, 'Instagram config exists');
    assert(creator.platformConfig.tiktok, 'TikTok config exists');
    assert(creator.platformConfig.twitter.hashtagLimit === 3, 'Twitter hashtag limit correct');
    assert(creator.platformConfig.instagram.hashtagLimit === 30, 'Instagram hashtag limit correct');
    console.log('   All platform configs present\n');

    // Test 9: Viral Hooks
    console.log('Test 9: Viral Hooks Library');
    assert(Array.isArray(creator.viralHooks), 'Has viral hooks');
    assert(creator.viralHooks.length > 0, 'Has multiple hooks');
    assert(creator.viralHooks.some(h => h.includes('Stop')), 'Has "Stop" hook');
    assert(creator.viralHooks.some(h => h.includes('How to')), 'Has "How to" hook');
    console.log(`   ${creator.viralHooks.length} viral hooks loaded\n`);

    // Test 10: Multi-Platform Support
    console.log('Test 10: Multi-Platform Support');
    const platforms = ['tiktok', 'instagram', 'twitter', 'linkedin', 'xiaohongshu'];
    for (const platform of platforms) {
      assert(creator.platformConfig[platform], `${platform} config exists`);
    }
    console.log(`   All ${platforms.length} platforms supported\n`);

    console.log('========================================');
    console.log('✅ All tests passed!');
    console.log('========================================\n');

  } catch (error) {
    console.error('\n❌ Test failed:', error.message);
    console.error(error.stack);
    process.exit(1);
  }
}

runTests();
