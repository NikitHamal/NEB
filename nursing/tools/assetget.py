import sys, runpy, urllib.request
_o = urllib.request.Request.__init__
def _i(self, url, data=None, headers={}, *a, **k):
    h = dict(headers); h["User-Agent"] = "NEBiansNursingBot/1.0 (https://github.com/NikitHamal/NEB)"
    _o(self, url, data, h, *a, **k)
urllib.request.Request.__init__ = _i
sys.path.insert(0, "/tmp/NEB/notes/pipeline")
sys.argv = ["assets.py"] + sys.argv[1:]
runpy.run_path("/tmp/NEB/notes/pipeline/assets.py", run_name="__main__")
