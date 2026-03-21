const express = require('express');
const fs = require('fs');
const path = require('path');
const { GoogleGenAI } = require('@google/genai');
const state = require('../config/state');
const { emitStreamLog } = require('../utils/streamer');

const router = express.Router();

router.post('/draft-script', async (req, res) => {
    const { id, host1 = 'Alex', host2 = 'Sam', targetLanguage = 'English' } = req.body;
    const safeId = state.sanitizeId(id);
    const sessionDir = path.join(state.downloadsDir, safeId);
    const apiKey = process.env.GEMINI_API_KEY;

    if (!apiKey) return res.status(401).json({ error: "Gemini API key is missing in environment." });
    
    const sourceFile = path.join(sessionDir, 'original.txt');
    if (!fs.existsSync(sourceFile)) return res.status(404).json({ error: "Source text not found." });

    try {
        const sourceText = fs.readFileSync(sourceFile, 'utf8');
        const ai = new GoogleGenAI({ apiKey: apiKey });

        emitStreamLog(safeId, { message: `Drafting ${targetLanguage} multi-host script via Gemini...` });

        const systemPrompt = `You are a professional podcast producer and scriptwriter.
        Convert the following source text into an engaging, conversational podcast script.
        1. Use exactly two hosts: ${host1} (Host 1) and ${host2} (Host 2).
        2. Output language must be ${targetLanguage}.
        3. Format every line EXACTLY like this: "Name: Spoken text here."
        4. Do NOT include sound effects, brackets, or stage directions.
        5. CRITICAL: The final script MUST NOT exceed 2100 words to comply with LinkedIn duration limits.`;

        const response = await ai.models.generateContent({
            model: 'gemini-2.5-flash',
            contents: `Source Material to adapt:\n${sourceText}`,
            config: { 
                systemInstruction: systemPrompt,
                temperature: 0.7 
            }
        });

        fs.writeFileSync(path.join(sessionDir, 'script.txt'), response.text);
        emitStreamLog(safeId, { message: "Script successfully drafted and formatted!" });
        res.json({ success: true, script: response.text });
    } catch (error) {
        emitStreamLog(safeId, { status: 'error', message: "Failed to draft script: " + error.message });
        res.status(500).json({ error: error.message });
    }
});

module.exports = router;