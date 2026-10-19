import html
import json
from pathlib import Path
import i18n


def rows(asset_ids, registry):
    path = Path(__file__).resolve().parents[1] / 'assets/credits-ne.json'
    translations = json.loads(path.read_text())
    output = []
    for aid in asset_ids:
        if aid not in translations:
            return None
        text, original = translations[aid], registry[aid]
        license_name = original['license'].replace('CC BY-SA', 'क्रिएटिभ कमन्स श्रेय–समानअनुमति').replace('CC BY', 'क्रिएटिभ कमन्स श्रेय').replace('CC0', 'क्रिएटिभ कमन्स शून्य').replace('Public domain', 'सार्वजनिक सम्पत्ति')
        license_name = i18n.num_str(license_name)
        source = original.get('page', '')
        link = f'<a href="{html.escape(source, quote=True)}">मूल चित्र र श्रेय विवरण</a>'
        if original.get('license_url'):
            link += f' · <a href="{html.escape(original["license_url"], quote=True)}">पूर्ण अनुमतिपत्र</a>'
        output.append(f'<div class="cr"><b>{html.escape(text["title"])}</b> — {html.escape(text["author"])}; {html.escape(license_name)}। {link}</div>')
    return ''.join(output)
