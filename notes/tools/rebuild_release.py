import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'notes/pipeline'))
sys.path.insert(0, str(ROOT / 'notes/tools'))
import build_pdf
import push_branch


def main(slugs):
    completed = []
    for slug in slugs:
        path, chapters, pages = build_pdf.build(slug)
        relative = str(Path(path).relative_to(ROOT))
        if os.environ.get('NEB_PUSH_BOOKS') == '1':
            sha = push_branch.push([relative], f'build(notes): regenerate {slug} complete book ({pages} pages)', root=str(ROOT))
        else:
            sha = ''
        completed.append({'slug': slug, 'path': relative, 'chapters': chapters, 'pages': pages,
                          'bytes': Path(path).stat().st_size, 'commit': sha})
        report = ROOT / 'task/book-builds.json'
        report.parent.mkdir(exist_ok=True)
        previous = json.loads(report.read_text()) if report.exists() else []
        previous = [x for x in previous if x['slug'] != slug]
        report.write_text(json.dumps(previous + [completed[-1]], ensure_ascii=False, indent=2)+'\n')
    return completed


if __name__ == '__main__':
    main(sys.argv[1:])
