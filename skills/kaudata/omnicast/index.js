require('dotenv').config();
const express = require('express');
const fs = require('fs');
const path = require('path');
const rateLimit = require('express-rate-limit');

const state = require('./config/state');
const ingestRoutes = require('./routes/ingest');
const draftRoutes = require('./routes/draft');
const synthesizeRoutes = require('./routes/synthesize');
const utilityRoutes = require('./routes/utilities');
const imageRoutes = require('./routes/images');
const linkedinRoutes = require('./routes/linkedin'); // NEW

const app = express();
const port = process.env.PORT || 7860;

app.use(express.static('public'));
app.use('/downloads', express.static(state.downloadsDir)); 
app.use(express.json({ limit: '50mb' }));

app.use('/api', ingestRoutes);
app.use('/api', draftRoutes);
app.use('/api', synthesizeRoutes);
app.use('/api', utilityRoutes);
app.use('/api', imageRoutes);
app.use('/api', linkedinRoutes); // NEW

app.get('/api/stream-logs', (req, res) => {
    const { id } = req.query;
    res.writeHead(200, { 'Content-Type': 'text/event-stream', 'Cache-Control': 'no-cache', 'Connection': 'keep-alive' });
    state.sseClients[id] = res;
    res.write(`data: ${JSON.stringify({ message: "Connection established." })}\n\n`);
    req.on('close', () => { delete state.sseClients[id]; });
});

app.listen(port, () => console.log(`🚀 Studio running securely at http://127.0.0.1:${port}`));