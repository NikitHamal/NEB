import re
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DIGITS = str.maketrans('0123456789', '०१२३४५६७८९')


def number(n):
    return str(n).translate(DIGITS)


def numbered(text, bold=False):
    pattern = r'^\*\*([०-९0-9]+)[.।]\*\*\s*' if bold else r'^([०-९0-9]+)[.।]\s*'
    matches = list(re.finditer(pattern, text, re.M))
    return [text[m.end():matches[i+1].start() if i+1 < len(matches) else len(text)].strip()
            for i, m in enumerate(matches)]


def pool(body, group):
    match = re.search(r'\*\*समूह '+group+r'[^\n]+\n(.*?)^::: note [^\n]+\n(.*?)^:::', body, re.M | re.S)
    if not match:
        raise ValueError(group)
    questions, answers = numbered(match[1]), numbered(match[2], bold=True)
    if len(questions) != len(answers):
        raise ValueError((group, len(questions), len(answers)))
    return list(zip(questions, answers))


def header(unit, title):
    return f'---\nsubject: Question Bank\ngrade: 10\nunit: {unit}\ntitle: "{title}"\nhours: 0\narea: सामाजिक अध्ययन तथा मानव मूल्य शिक्षा\n---\n\n'


def render(items, marks, start=1):
    questions, answers = [], []
    for n, (q, a) in enumerate(items, start):
        q = re.sub(r'\s*<span class="marks">.*?</span>', '', q, flags=re.S)
        questions.append(f'**{number(n)}.** {q} <span class="marks">[{marks}]</span>')
        answers.append(f'**{number(n)}.** {a}')
    return '\n\n'.join(questions)+'\n\n::: note कारणसहित उत्तरकुञ्जी\n'+'\n\n'.join(answers)+'\n:::\n\n'


def main():
    units = []
    for path in sorted((ROOT/'notes/content/soc10').glob('unit-*.md')):
        source = path.read_text()
        title = re.search(r'^title: (.+)$', source, re.M)[1].strip('"')
        practice = source.split('## अभ्यास',1)[1]
        units.append({'title': title, 'objective': pool(practice,'क'), 'short': pool(practice,'ख'), 'long': pool(practice,'ग')})
    extras = json.loads((ROOT/'notes/editorial/social10-extra.json').read_text())
    for unit, extra in zip(units, extras, strict=True):
        unit['objective'].extend((q, a) for q, a in extra)
    caution = '::: caution अभ्यास सामग्रीबारे\nयी प्रश्न नेबियन्सको सामाजिक अध्ययन पुस्तकका अभ्यासबाट सङ्कलित र पुनर्व्यवस्थित हुन्। यी विगतका प्रश्नपत्रको प्रतिलिपि वा आगामी परीक्षाको भविष्यवाणी होइनन्। आफ्नो विद्यालयले दिएको हालको विशिष्टीकरण तालिकासँग प्रश्नको ढाँचा मिलाउनुहोस्।\n:::\n\n'
    objective = header(14,'सामाजिक अध्ययन: एकाइअनुसार वस्तुगत प्रश्नसङ्ग्रह')+caution
    objective += 'छोटो प्रश्नको उत्तरमा तथ्य, मिति वा अवधारणा स्पष्ट लेख्नुहोस्। विकल्पयुक्त प्रश्न पहिले विकल्प नहेरी हल गर्नुहोस् र त्यसपछि उत्तरकुञ्जीको कारणसँग तुलना गर्नुहोस्। गलत भएका प्रश्नको विषय र गल्तीको कारण छुट्टै कापीमा राख्नुहोस्।\n\n'
    subjective = header(15,'सामाजिक अध्ययन: एकाइअनुसार विषयगत प्रश्नसङ्ग्रह')+caution
    subjective += 'चार अङ्कको उत्तरमा प्रश्नले मागेको अवधारणा र कारण स्पष्ट पार्नुहोस्। सात अङ्कको उत्तरमा परिचय, सम्बन्धित आधार, उदाहरण र निष्कर्ष जोड्नुहोस्। तलका उत्तर अध्ययनका विस्तृत आधार हुन्; परीक्षामा प्रश्नको निर्देशन र अङ्कअनुसार छानेर लेख्नुहोस्।\n\n'
    for i,u in enumerate(units,1):
        objective+=f'## १४.{number(i)} {u["title"]}\n\n'+render(u['objective'],1)
        subjective+=f'## १५.{number(i)} {u["title"]}\n\n**छोटो उत्तर अभ्यास — चार अङ्क**\n\n'+render(u['short'],4)
        subjective+='**लामो उत्तर अभ्यास — सात अङ्क**\n\n'+render(u['long'],7)
    models = header(16,'सामाजिक अध्ययन: नमुना प्रश्नपत्र र पुनरावलोकन योजना')+caution
    models+='## १६.१ अभ्यासको ढाँचा\n\n| समूह | प्रश्न | प्रतिप्रश्न अङ्क | जम्मा |\n|---|---|---|---|\n| क — अति छोटो | ११ | १ | ११ |\n| ख — छोटो | ९ | ४ | ३६ |\n| ग — लामो | ४ | ७ | २८ |\n| पूर्णाङ्क | २४ | | ७५ |\n\nयी तीन नमुना पत्र स्वअध्ययनका लागि बनाइएका हुन्। एउटै विषय फरक ढङ्गले दोहोरिन सक्छ। पहिलो पटक पुस्तक नहेरी हल गर्नुहोस्; दोस्रो पटक उत्तरको कारण जाँच्नुहोस्; तेस्रो पटक गल्ती भएको विषय मात्र फेरि लेख्नुहोस्। विद्यालयले तोकेको समयमा अभ्यास गर्नुहोस्।\n\n'
    for s in range(3):
        models+=f'## १६.{number(s+2)} नमुना प्रश्नपत्र — {number(s+1)}\n\n'
        obj=[u['objective'][s%len(u['objective'])] for u in units]+[units[s]['objective'][(s+1)%len(units[s]['objective'])]]
        short=[units[(i+s)%10]['short'][s%len(units[(i+s)%10]['short'])] for i in range(9)]
        long=[units[i]['long'][s%len(units[i]['long'])] for i in [(s+2)%10,(s+5)%10,(s+6)%10,(s+9)%10]]
        obj=[(re.split(r'\s*\(क\)',q)[0].strip(),re.sub(r'^\([कखगघ]\)\s*[—–-]?\s*','',a)) for q,a in obj]
        models+='**समूह क — अति छोटो उत्तर**\n\n'+render(obj,1)
        models+='**समूह ख — छोटो उत्तर**\n\n'+render(short,4,12)
        models+='**समूह ग — लामो उत्तर**\n\n'+render(long,7,21)
    models+='## १६.५ पुनरावलोकन प्राथमिकता\n\nप्राथमिकता प्रश्न आउने सम्भावनाको दाबी होइन; आफ्नै कमजोरी सुधार्ने क्रम हो।\n\n| आफ्नो अवस्था | अब गर्ने काम | पूरा भएको प्रमाण |\n|---|---|---|\n| तथ्य याद छैन | एकाइको पाँच वस्तुगत प्रश्न दोहोर्‍याउने | पुस्तक नहेरी सही उत्तर र कारण |\n| तथ्य थाहा छ, व्याख्या आउँदैन | सोही एकाइको छोटो प्रश्न लेख्ने | कारण र स्थानीय उदाहरण |\n| उत्तर लामो तर असम्बन्धित छ | निर्देशनका क्रियापद छुट्याउने | प्रश्नका सबै मागलाई सम्बोधन |\n| नक्सा वा तथ्याङ्क कमजोर छ | सम्बन्धित चित्र र तालिका अभ्यास गर्ने | शीर्षक, सङ्केत, एकाइ र सही निष्कर्ष |\n\n::: tip साथीबाट जाँच गराउने विधि\nआफ्नो उत्तर साटेर प्रश्नका मागअगाडि चिनो लगाउनुहोस्। तथ्यगत गल्ती, छुटेको कारण र अस्पष्ट उदाहरण फरक चिह्नले देखाउनुहोस्। उत्तरकुञ्जीसँग तुलना गरेपछि आफ्नै शब्दमा संशोधित उत्तर लेख्नुहोस्।\n:::\n'
    for n,body in [(14,objective),(15,subjective),(16,models)]:
        (ROOT/f'notes/content/qbank10/unit-{n:02}.md').write_text(body)
    p=ROOT/'notes/curriculum/qbank10.md';t=p.read_text();t=t.replace('# PART: Social Studies','# PART: सामाजिक अध्ययन तथा मानव मूल्य शिक्षा')
    for a,b in [('Social Studies: Unit-wise Objective Question Bank','सामाजिक अध्ययन: एकाइअनुसार वस्तुगत प्रश्नसङ्ग्रह'),('Social Studies: Unit-wise Subjective Question Bank','सामाजिक अध्ययन: एकाइअनुसार विषयगत प्रश्नसङ्ग्रह'),('Social Studies: Model Question Sets and Predicted Questions','सामाजिक अध्ययन: नमुना प्रश्नपत्र र पुनरावलोकन योजना')]:t=t.replace(a,b)
    p.write_text(t)
    print('Social studies bank localised: 100 objective items, 60 subjective questions, 3 complete practice papers.')


if __name__=='__main__':
    main()
