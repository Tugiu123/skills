const express = require('express');
const fs = require('fs');
const path = require('path');
const archiver = require('archiver');
const state = require('../config/state');

const router = express.Router();

// Helper function to validate path boundaries
const getValidatedSessionDir = (rawId) => {
    if (!rawId) throw new Error("ID is required.");
    const safeId = state.sanitizeId(rawId);
    const baseDir = path.resolve(state.downloadsDir);
    const targetDir = path.resolve(baseDir, safeId);
    
    // CRITICAL: Ensure target strictly starts with baseDir to prevent partial name matching
    if (!targetDir.startsWith(baseDir + path.sep)) {
        throw new Error("Forbidden: Invalid path traversal detected.");
    }
    return targetDir;
};

router.post('/snippet', async (req, res) => { /* Add snippet logic here if needed */ });
router.post('/highlight-reel', async (req, res) => { /* Add reel logic here if needed */ });

router.get('/download-zip', (req, res) => {
    try {
        const sessionDir = getValidatedSessionDir(req.query.id);
        if (!fs.existsSync(sessionDir)) return res.status(404).send("Session not found.");
        
        const safeAttachmentName = `omnicast_session_${path.basename(sessionDir)}.zip`;
        res.attachment(safeAttachmentName);
        
        const archive = archiver('zip', { zlib: { level: 9 } });
        archive.pipe(res);
        archive.directory(sessionDir, false);
        archive.finalize();
    } catch (error) {
        const status = error.message.includes('Forbidden') ? 403 : 400;
        res.status(status).send(error.message);
    }
});

router.delete('/delete-folder', (req, res) => {
    try {
        const sessionDir = getValidatedSessionDir(req.body.id);
        if (fs.existsSync(sessionDir)) fs.rmSync(sessionDir, { recursive: true, force: true });
        res.json({ success: true, message: "Folder safely removed." });
    } catch (error) {
        const status = error.message.includes('Forbidden') ? 403 : 400;
        res.status(status).json({ success: false, error: error.message });
    }
});

module.exports = router;