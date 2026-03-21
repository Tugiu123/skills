const express = require('express');
const fs = require('fs');
const path = require('path');
const multer = require('multer');
const axios = require('axios');
const cheerio = require('cheerio');
const { YoutubeTranscript } = require('youtube-transcript-plus');
const state = require('../config/state');
const { emitStreamLog } = require('../utils/streamer');
const { processLocalFile } = require('../utils/fileProcessor'); // NEW

const router = express.Router();
const tempUploadsDir = path.join(state.downloadsDir, 'temp_uploads');
if (!fs.existsSync(tempUploadsDir)) fs.mkdirSync(tempUploadsDir, { recursive: true });
const upload = multer({ dest: tempUploadsDir, limits: { fileSize: 500 * 1024 * 1024 } });

router.post('/ingest', upload.single('file'), async (req, res) => {
    const { id, sourceType, url } = req.body;
    const safeId = state.sanitizeId(id);
    const sessionDir = path.join(state.downloadsDir, safeId);

    if (!fs.existsSync(sessionDir)) fs.mkdirSync(sessionDir, { recursive: true });
    let extractedText = "";

    try {
        emitStreamLog(safeId, { message: "Initializing ingestion engine..." });

        if (sourceType === 'url' && url) {
            if (url.toLowerCase().endsWith('.mp4')) {
                const tempVideoPath = path.join(sessionDir, 'downloaded.mp4');
                const response = await axios({ method: 'GET', url: url, responseType: 'stream' });
                const writer = fs.createWriteStream(tempVideoPath);
                response.data.pipe(writer);
                await new Promise((resolve, reject) => { writer.on('finish', resolve); writer.on('error', reject); });
                
                // Process the downloaded file
                extractedText = await processLocalFile(tempVideoPath, 'video/mp4', sessionDir, safeId);
                if (fs.existsSync(tempVideoPath)) fs.unlinkSync(tempVideoPath);
                
            } else if (url.includes('youtube.com/watch') || url.includes('youtu.be/')) {
                emitStreamLog(safeId, { message: "Detected YouTube URL. Fetching closed captions..." });
                try {
                    const transcriptData = await YoutubeTranscript.fetchTranscript(url);
                    extractedText = transcriptData.map(item => item.text).join(' ');
                    emitStreamLog(safeId, { message: "YouTube transcript successfully extracted!" });
                } catch (ytError) {
                    throw new Error("Could not fetch YouTube transcript. Ensure the video has English captions.");
                }
            } else {
                emitStreamLog(safeId, { message: "Scraping target URL..." });
                const response = await axios.get(url, { headers: { 'User-Agent': 'Mozilla/5.0' }, timeout: 10000 });
                const $ = cheerio.load(response.data);
                $('header, footer, nav, aside, script, style, noscript, svg').remove();
                
                let contentContainer = $('article').length > 0 ? $('article') : $('body');
                contentContainer.find('p, h1, h2, h3').each((i, el) => {
                    const text = $(el).text().trim();
                    if (text.length > 1) extractedText += text + "\n\n";
                });
            }
        } else if (req.file) {
            const tempPath = req.file.path;
            const mimeType = req.file.mimetype;
            emitStreamLog(safeId, { message: `Processing uploaded file...` });

            try {
                extractedText = await processLocalFile(tempPath, mimeType, sessionDir, safeId);
            } finally {
                if (fs.existsSync(tempPath)) fs.unlinkSync(tempPath);
            }
        }

        if (!extractedText.trim()) throw new Error("Could not extract meaningful text.");
        fs.writeFileSync(path.join(sessionDir, 'original.txt'), extractedText.trim());

        emitStreamLog(safeId, { message: "Ingestion complete! Ready for script drafting." });
        res.json({ success: true, fullText: extractedText.trim() });
    } catch (error) {
        emitStreamLog(safeId, { status: 'error', message: error.message });
        res.status(500).json({ error: error.message });
    }
});
module.exports = router;