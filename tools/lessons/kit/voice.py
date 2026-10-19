import asyncio
import hashlib
import json
import os
import subprocess
import time

HERE = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(HERE, "..", ".cache", "tts")

VOICES = {
    "en": {"voice": "en-US-AndrewMultilingualNeural", "rate": "-4%", "pitch": "+0Hz"},
    "ne": {"voice": "ne-NP-HemkalaNeural", "rate": "-6%", "pitch": "+0Hz"},
    "ne-m": {"voice": "ne-NP-SagarNeural", "rate": "-6%", "pitch": "+0Hz"},
}


def _duration(path):
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=nw=1:nk=1", path],
        capture_output=True, text=True,
    ).stdout.strip()
    return float(out)


async def _synth(text, voice, rate, pitch, mp3, vtt):
    import edge_tts

    comm = edge_tts.Communicate(text, voice, rate=rate, pitch=pitch, boundary="SentenceBoundary")
    sub = edge_tts.SubMaker()
    with open(mp3, "wb") as f:
        async for chunk in comm.stream():
            if chunk["type"] == "audio":
                f.write(chunk["data"])
            elif chunk["type"] in ("WordBoundary", "SentenceBoundary"):
                sub.feed(chunk)
    with open(vtt, "w", encoding="utf-8") as f:
        f.write(sub.get_srt())


def speak(text, lang="en"):
    """Synthesize `text` once and cache it. Returns (wav_path, seconds, srt_cues)."""
    cfg = VOICES[lang]
    os.makedirs(CACHE, exist_ok=True)
    key = hashlib.sha1(json.dumps([text, cfg], ensure_ascii=False).encode()).hexdigest()[:20]
    mp3 = os.path.join(CACHE, key + ".mp3")
    wav = os.path.join(CACHE, key + ".wav")
    srt = os.path.join(CACHE, key + ".srt")
    meta = os.path.join(CACHE, key + ".json")
    if os.path.exists(meta) and os.path.exists(wav):
        m = json.load(open(meta, encoding="utf-8"))
        return wav, m["dur"], m["cues"]
    last = None
    for attempt in range(10):
        try:
            asyncio.run(asyncio.wait_for(_synth(text, cfg["voice"], cfg["rate"], cfg["pitch"], mp3, srt), timeout=30 + len(text) / 12))
            if os.path.getsize(mp3) > 1000:
                break
        except Exception as e:
            last = e
        time.sleep(2 + attempt * 3)
    else:
        raise RuntimeError(f"tts failed: {last}")
    subprocess.run(
        ["ffmpeg", "-y", "-v", "error", "-i", mp3, "-af", "silenceremove=start_periods=1:start_threshold=-50dB,areverse,silenceremove=start_periods=1:start_threshold=-50dB,areverse",
         "-ar", "48000", "-ac", "1", wav],
        check=True,
    )
    dur = _duration(wav)
    cues = _parse_srt(open(srt, encoding="utf-8").read())
    json.dump({"dur": dur, "cues": cues, "text": text}, open(meta, "w", encoding="utf-8"), ensure_ascii=False)
    return wav, dur, cues


def _ts(s):
    h, m, rest = s.split(":")
    sec, ms = rest.split(",")
    return int(h) * 3600 + int(m) * 60 + int(sec) + int(ms) / 1000


def _parse_srt(s):
    cues = []
    for block in s.strip().split("\n\n"):
        lines = block.strip().splitlines()
        if len(lines) < 3:
            continue
        a, b = lines[1].split(" --> ")
        cues.append([_ts(a.strip()), _ts(b.strip()), " ".join(lines[2:]).strip()])
    if cues:
        off = cues[0][0]
        cues = [[max(0, x - off), max(0, y - off), t] for x, y, t in cues]
    return cues
