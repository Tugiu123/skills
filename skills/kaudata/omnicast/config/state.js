const path = require('path');
const fs = require('fs');

const downloadsDir = path.join(__dirname, '../downloads');
if (!fs.existsSync(downloadsDir)) fs.mkdirSync(downloadsDir, { recursive: true });

module.exports = {
    downloadsDir,
    jobs: {},
    sseClients: {},
    jobQueue: [],
    activeJobs: 0,
    MAX_CONCURRENT_JOBS: 2,
    
    sanitizeId: (id) => {
        if (!id || typeof id !== 'string') return 'default_session';
        // Strip non-alphanumeric characters
        const safeId = id.replace(/[^a-zA-Z0-9_-]/g, '');
        // Prevent empty string resolution
        if (!safeId) return 'default_session';
        // Enforce max length
        return safeId.substring(0, 64);
    }
};