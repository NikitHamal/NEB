"""Offline tests for the Paradee TTS proxy (no network — pure functions only)."""
import io
import wave

from django.test import SimpleTestCase

from api import paradee_proxy as pq


def _make_wav(seconds=1.0, rate=24000):
    bio = io.BytesIO()
    with wave.open(bio, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(rate)
        w.writeframes(b"\x00\x00" * int(seconds * rate))
    return bio.getvalue()


class ParadeeUnitTests(SimpleTestCase):
    def test_models(self):
        models = pq.get_models()
        self.assertTrue(any(m["id"] == "paradee/paradee-8m" for m in models))

    def test_speed_clamp(self):
        self.assertEqual(pq._clamp_speed(9.9), 2.0)
        self.assertEqual(pq._clamp_speed(0.1), 0.5)
        self.assertEqual(pq._clamp_speed(None), 1.0)
        self.assertEqual(pq._clamp_speed("fast"), 1.0)

    def test_empty_text_rejected_without_network(self):
        r = pq.generate_tts("")
        self.assertEqual(r["status"], "error")

    def test_overlong_text_rejected_without_network(self):
        r = pq.generate_tts("x" * (pq.MAX_TEXT + 1))
        self.assertEqual(r["status"], "error")
        self.assertIn("too long", r["error"])

    def test_chunk_budget(self):
        chunks = pq.split_chunks("Hello world. " * 300)
        self.assertTrue(1 < len(chunks) <= pq.MAX_CHUNKS)
        for c in chunks:
            self.assertLessEqual(len(c), pq.CHUNK_TARGET + 1)
        joined = " ".join(chunks)
        for word in "Hello world.".split():
            self.assertIn(word, joined)

    def test_chunk_punctuation_lossless(self):
        text = 'She said "hi!" (loudly). Then left... 3.14 is pi.'
        chunks = pq.split_chunks(text)
        self.assertEqual(" ".join(" ".join(chunks).split()), " ".join(text.split()))

    def test_wav_concat_duration(self):
        a, b = _make_wav(1.0), _make_wav(2.0)
        out = pq.concat_wav([a, b])
        self.assertAlmostEqual(pq.wav_duration_sec(out), 3.0, places=1)
        self.assertTrue(out.startswith(b"RIFF"))

    def test_wav_concat_single_passthrough(self):
        a = _make_wav(0.5)
        self.assertEqual(pq.concat_wav([a]), a)

    def test_wav_concat_mismatch_rejected(self):
        a = _make_wav(1.0, rate=24000)
        b = _make_wav(1.0, rate=16000)
        with self.assertRaises(ValueError):
            pq.concat_wav([a, b])

    def test_sse_parse(self):
        kind, payload = pq._parse_sse('event: complete\ndata: [{"url": "https://x/audio.wav"}]')
        self.assertEqual(kind, "complete")
        self.assertIn("audio.wav", payload)
        self.assertEqual(pq._find_audio([{"url": "/gradio_api/file=/tmp/g/audio.wav"}]),
                         pq.BASE + "/gradio_api/file=/tmp/g/audio.wav")
