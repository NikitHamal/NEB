import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "nebians.settings")
os.environ.setdefault("SECRET_KEY", "local-check-key")
os.environ.setdefault("DEBUG", "1")
django.setup()

from api import smallest_proxy as s

for pool in s.POOLS:
    voices = s.get_voices(pool)
    print(pool, "->", len(voices), "voices")
    if voices:
        v = voices[0]
        print("   sample:", v)
print("resolve 'Kelsey' ->", s.resolve_voice("Kelsey"))
print("resolve '' ->", s.resolve_voice(""))
print("resolve 'Magnus' on v3.1 ->", s.resolve_voice("Magnus", "smallest/lightning-v3.1"))
print("chunks of 600 chars ->", [len(c) for c in s.split_chunks("word " * 120)])
print("models:", [m["id"] for m in s.get_models()])
print("no key ->", s.generate_tts("Hello."))
