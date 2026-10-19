import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def update(slug, number):
    path = ROOT/f'notes/content/{slug}/unit-{number:02d}.md'
    source = path.read_text()
    if slug != 'qbank8':
        source = re.sub(r'^```figure caption="(?:Actual practice-question coverage|यस अध्यायमा रहेका अभ्यास प्रश्नको वास्तविक सङ्ख्या)[^\n]*\n.*?^```\s*', '', source, flags=re.M|re.S)
    nepali = bool(re.search(r'^title: "?[\u0900-\u097f]', source, re.M))
    chapters = []
    for section in re.finditer(r'^##[ \t]+([^\n]+)\n(.*?)(?=^##[ \t]+|\Z)', source, re.S|re.M):
        title = re.sub(r'^\d+\.\d+\s*', '', section[1])
        title = re.sub(r'^(Unit|Chapter)\s*\d+:\s*', '', title)
        body = re.sub(r'^:::.*?^:::', '', section[2], flags=re.M|re.S)
        count = len(re.findall(r'^(?:\*\*)?[0-9०-९]+[.।](?:\*\*)?\s+', body, re.M))
        if count:
            chapters.append((title, count))
    if not chapters:
        raise ValueError(path)
    caption = ('यस अध्यायमा रहेका अभ्यास प्रश्नको वास्तविक सङ्ख्या। यो परीक्षाको अङ्कभार वा प्रश्न आउने सम्भावनाको अनुमान होइन।' if nepali else 'Actual practice-question coverage in this chapter. Counts describe this book, not examination weightage or the probability of a question appearing.')
    label = ' प्रश्न' if nepali else ' questions'
    figure='```figure caption="'+caption+'"\nfig, ax = barh_ranked(\n    '+json.dumps([x[0] for x in chapters],ensure_ascii=False)+',\n    '+json.dumps([x[1] for x in chapters])+', unit='+json.dumps(label,ensure_ascii=False)+')\n```'
    if slug=='qbank8':
        source,n=re.subn(r'^```figure[^\n]*\n.*?^```',lambda _:figure,source,count=1,flags=re.M|re.S)
        if n!=1:raise ValueError(path)
    else:
        marker='\n\n'+figure+'\n\n'
        at=source.index('\n## ')
        source=source[:at]+marker+source[at:]
    path.write_text(source)
    return sum(x[1] for x in chapters)


if __name__=='__main__':
    for slug,numbers in [('qbank8',[2,5,8,11,14,17]),('qbank10',[2,5,8,11,14,17]),('qbankc10',[2,5])]:
        for n in numbers:print(slug,n,update(slug,n))
