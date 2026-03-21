import { log, setApiLoading, updateLoadingMessage, displayThumbnail, resetWorkspace, showSessionControls, buildLiveCaptions, syncCaptionsWithAudio } from './ui.js';
import { requestSessionCleanup } from './api.js';

let currentVideoId = `session_${Date.now()}`;

document.getElementById('btn-ingest').addEventListener('click', async () => {
    const url = document.getElementById('sourceUrl').value;
    const fileInput = document.getElementById('sourceFile');
    const file = fileInput.files[0];

    if (!url && !file) return alert("Please enter a URL or select a file.");
    
    setApiLoading(true);
    showSessionControls();
    
    log("Initiating media ingestion...");
    updateLoadingMessage("Extracting text...");
    
    const eventSource = new EventSource(`/api/stream-logs?id=${currentVideoId}`);
    await new Promise(resolve => { eventSource.onopen = resolve; setTimeout(resolve, 500); });
    eventSource.onmessage = e => { const d = JSON.parse(e.data); log(d.message); updateLoadingMessage(d.message); };
    
    const formData = new FormData();
    formData.append('id', currentVideoId);
    if (file) formData.append('file', file);
    else { formData.append('sourceType', 'url'); formData.append('url', url); }
    
    try {
        await fetch('/api/ingest', { method: 'POST', body: formData });
    } catch (e) { log(`❌ ${e.message}`); }
    
    eventSource.close(); setApiLoading(false);
});

const updateScriptStats = () => {
    const text = document.getElementById('script-editor').value;
    const wordCount = text.trim() === '' ? 0 : text.trim().split(/\s+/).length;
    const totalSeconds = Math.round((wordCount / 150) * 60);
    const mins = Math.floor(totalSeconds / 60);
    const secs = (totalSeconds % 60).toString().padStart(2, '0');
    
    document.getElementById('word-count').innerText = wordCount;
    document.getElementById('est-time').innerText = `${mins}:${secs}`;
    
    const warningEl = document.getElementById('linkedin-warning');
    if (wordCount > 0 && (wordCount < 450 || wordCount > 2100)) warningEl.style.display = 'inline';
    else warningEl.style.display = 'none';
};

document.getElementById('script-editor').addEventListener('input', updateScriptStats);

document.getElementById('btn-draft').addEventListener('click', async () => {
    setApiLoading(true);
    log("Initiating Gemini script drafting sequence...");
    updateLoadingMessage("Drafting...");
    
    const host1 = document.getElementById('host1').value || 'Alex';
    const host2 = document.getElementById('host2').value || 'Sam';
    const language = document.getElementById('targetLanguage').value;

    const eventSource = new EventSource(`/api/stream-logs?id=${currentVideoId}`);
    await new Promise(resolve => { eventSource.onopen = resolve; setTimeout(resolve, 500); });
    eventSource.onmessage = e => { const d = JSON.parse(e.data); log(d.message); updateLoadingMessage(d.message); };

    try {
        const res = await fetch('/api/draft-script', {
            method: 'POST', headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ id: currentVideoId, host1, host2, targetLanguage: language })
        });
        const data = await res.json();
        if (!res.ok) throw new Error(data.error);
        document.getElementById('script-editor').value = data.script;
        updateScriptStats();
    } catch (e) { log(`❌ ${e.message}`); }
    
    eventSource.close(); setApiLoading(false);
});

document.getElementById('btn-generate-audio').addEventListener('click', async () => {
    setApiLoading(true);
    log("Initiating audio synthesis pipeline...");
    updateLoadingMessage("Synthesizing...");
    
    const script = document.getElementById('script-editor').value;
    const host1 = document.getElementById('host1').value || 'Alex';
    const host2 = document.getElementById('host2').value || 'Sam';

    const eventSource = new EventSource(`/api/stream-logs?id=${currentVideoId}`);
    await new Promise(resolve => { eventSource.onopen = resolve; setTimeout(resolve, 500); });
    
    eventSource.onmessage = async (e) => {
        const d = JSON.parse(e.data); log(d.message); updateLoadingMessage(d.message);
        
        if (d.status === 'done') {
            eventSource.close(); setApiLoading(false);
            const audio = document.getElementById('podcast-audio');
            const audioUrl = `/downloads/${currentVideoId}/podcast.m4a`;
            const vttUrl = `/downloads/${currentVideoId}/podcast.vtt`;
            
            audio.src = audioUrl;
            document.getElementById('podcast-vtt').src = vttUrl;
            document.getElementById('audio-container').style.display = 'block';

            try {
                const vttRes = await fetch(vttUrl);
                buildLiveCaptions(await vttRes.text());
            } catch (err) { console.error("Failed to load VTT for UI", err); }
        }
    };

    try {
        await fetch('/api/synthesize', {
            method: 'POST', headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ id: currentVideoId, script, host1, host2 })
        });
    } catch(e) { log(`❌ ${e.message}`); eventSource.close(); setApiLoading(false); }
});

document.getElementById('podcast-audio').addEventListener('timeupdate', (e) => {
    syncCaptionsWithAudio(e.target.currentTime);
});

document.getElementById('btn-draft-prompt').addEventListener('click', async () => {
    setApiLoading(true);
    log("Analyzing script for visual concepts...");
    updateLoadingMessage("Designing...");
    
    const eventSource = new EventSource(`/api/stream-logs?id=${currentVideoId}`);
    await new Promise(resolve => { eventSource.onopen = resolve; setTimeout(resolve, 500); });
    eventSource.onmessage = e => { const d = JSON.parse(e.data); log(d.message); updateLoadingMessage(d.message); };

    try {
        const res = await fetch('/api/draft-image-prompt', {
            method: 'POST', headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ id: currentVideoId })
        });
        const data = await res.json();
        if (!res.ok) throw new Error(data.error);

        document.getElementById('image-prompt-input').value = data.prompt;
        document.getElementById('prompt-editor-section').style.display = 'block';
    } catch (e) { log(`❌ ${e.message}`); }
    
    eventSource.close(); setApiLoading(false);
});

document.getElementById('btn-generate-thumbnail').addEventListener('click', async () => {
    setApiLoading(true);
    const userPrompt = document.getElementById('image-prompt-input').value;
    if (!userPrompt) return alert("Please draft or enter a prompt first.");

    log("Sending render request to Gemini 3.1 Flash Image...");
    updateLoadingMessage("Rendering...");

    const eventSource = new EventSource(`/api/stream-logs?id=${currentVideoId}`);
    await new Promise(resolve => { eventSource.onopen = resolve; setTimeout(resolve, 500); });
    eventSource.onmessage = e => { const d = JSON.parse(e.data); log(d.message); updateLoadingMessage(d.message); };

    try {
        const res = await fetch('/api/generate-thumbnail', {
            method: 'POST', headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ id: currentVideoId, prompt: userPrompt })
        });
        const data = await res.json();
        if (!res.ok) throw new Error(data.error);

        displayThumbnail(`/downloads/${currentVideoId}/${data.file}`, ""); 
        updateLoadingMessage("Done!");
    } catch (e) { log(`❌ ${e.message}`); updateLoadingMessage("Error!"); }
    
    eventSource.close(); setApiLoading(false);
});

document.getElementById('btn-generate-linkedin').addEventListener('click', async () => {
    setApiLoading(true);
    const btn = document.getElementById('btn-generate-linkedin');
    btn.disabled = true;
    
    const selectedLangs = Array.from(document.querySelectorAll('input[name="vtt-lang"]:checked'))
                               .map(cb => cb.value);
    
    log(selectedLangs.length > 0 
        ? `Initiating LinkedIn packaging & translating VTT to ${selectedLangs.length} languages...`
        : "Initiating LinkedIn video packaging...");
    updateLoadingMessage("Packaging...");

    const eventSource = new EventSource(`/api/stream-logs?id=${currentVideoId}`);
    await new Promise(resolve => { eventSource.onopen = resolve; setTimeout(resolve, 500); });
    eventSource.onmessage = e => { const d = JSON.parse(e.data); log(d.message); updateLoadingMessage(d.message); };

    try {
        const res = await fetch('/api/generate-linkedin', {
            method: 'POST', headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ id: currentVideoId, targetCaptionLanguages: selectedLangs })
        });
        const data = await res.json();
        if (!res.ok) throw new Error(data.error || "Failed to generate LinkedIn package.");

        document.getElementById('linkedin-post-text').value = data.post;
        document.getElementById('linkedin-video-player').src = `/downloads/${currentVideoId}/${data.video}?t=${Date.now()}`;
        document.getElementById('linkedin-display').style.display = 'block';
    } catch (e) { log(`❌ ${e.message}`); alert(e.message); } 
    finally { eventSource.close(); setApiLoading(false); btn.disabled = false; }
});

document.getElementById('btn-copy-linkedin').addEventListener('click', async () => {
    const textToCopy = document.getElementById('linkedin-post-text').value;
    const btn = document.getElementById('btn-copy-linkedin');
    try {
        await navigator.clipboard.writeText(textToCopy);
        btn.innerText = "✅ Copied!";
        setTimeout(() => { btn.innerText = "📋 Copy Text"; }, 2000);
    } catch (err) { alert("Failed to copy text. Please select and copy manually."); }
});

document.getElementById('btn-clear-session').addEventListener('click', async () => {
    await requestSessionCleanup(currentVideoId);
    resetWorkspace();
    currentVideoId = `session_${Date.now()}`;
});