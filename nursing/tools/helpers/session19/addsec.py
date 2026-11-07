#!/usr/bin/env python3
"""addsec.py N : insert /tmp/parts/kN.py (checker section for unit N) into check_frh.py, replacing an older section N."""
import sys,re
n=sys.argv[1]; p='/tmp/NEB/nursing/tools/check_frh.py'; t=open(p).read()
sec=open(f'/tmp/parts/k{n}.py').read().rstrip()+"\n"
t=re.sub(rf"# ---- U{n}-BEGIN.*?# ---- U{n}-END\n","",t,flags=re.S)
t=t.replace("# ---- END OF UNITS",f"# ---- U{n}-BEGIN\n{sec}# ---- U{n}-END\n# ---- END OF UNITS")
open(p,'w').write(t)
