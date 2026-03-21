const fs = require('fs');
const path = require('path');
const ffmpeg = require('fluent-ffmpeg');
const OpenAI = require('openai');
const { emitStreamLog } = require('./streamer');

function extractAndChunkAudio(videoPath, sessionDir) {
    return new Promise((resolve, reject) => {
        const chunkPattern = path.join(sessionDir, 'chunk_%03d.mp3');
        ffmpeg(videoPath).noVideo().audioCodec('libmp3lame').audioBitrate('128k') 
            .outputOptions(['-f segment', '-segment_time 600']).output(chunkPattern)
            .on('end', () => resolve(fs.readdirSync(sessionDir).filter(f => f.startsWith('chunk_') && f.endsWith('.mp3')).sort().map(f => path.join(sessionDir, f))))
            .on('error', reject).run();
    });
}

// Removed openaiApiKey from parameters
async function transcribeChunks(chunkPaths, sessionId) {
    // The SDK automatically finds process.env.OPENAI_API_KEY
    const openai = new OpenAI(); 
    let fullTranscription = "";
    let previousContext = "";
    
    for (let i = 0; i < chunkPaths.length; i++) {
        emitStreamLog(sessionId, { message: `[Whisper] Transcribing chunk ${i + 1} of ${chunkPaths.length}...` });
        const requestOptions = { file: fs.createReadStream(chunkPaths[i]), model: "whisper-1" };
        if (previousContext) requestOptions.prompt = previousContext;
        const response = await openai.audio.transcriptions.create(requestOptions);
        fullTranscription += response.text + " ";
        previousContext = response.text.slice(-200); 
    }
    return fullTranscription.trim();
}

module.exports = { extractAndChunkAudio, transcribeChunks };