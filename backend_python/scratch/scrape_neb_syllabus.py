import requests
from bs4 import BeautifulSoup, NavigableString
import json
import time
import re
import sys

CHAPTERS = [
    {'chapter_id': 'class-12-english-critical-thinking', 'chapter_title': 'Unit 1: Critical Thinking', 'order': 1,
     'url': 'https://nebplus2notes.com/class-12/english/ld/critical-thinking/'},
    {'chapter_id': 'class-12-english-family', 'chapter_title': 'Unit 2: Family', 'order': 2,
     'url': 'https://nebplus2notes.com/class-12/english/ld/family/'},
    {'chapter_id': 'class-12-english-sports', 'chapter_title': 'Unit 3: Sports', 'order': 3,
     'url': 'https://nebplus2notes.com/class-12/english/ld/sports/'},
    {'chapter_id': 'class-12-english-technology', 'chapter_title': 'Unit 4: Technology', 'order': 4,
     'url': 'https://nebplus2notes.com/class-12/english/ld/technology/'},
    {'chapter_id': 'class-12-english-education', 'chapter_title': 'Unit 5: Education', 'order': 5,
     'url': 'https://nebplus2notes.com/class-12/english/ld/education/'},
    {'chapter_id': 'class-12-english-money-and-economy', 'chapter_title': 'Unit 6: Money and Economy', 'order': 6,
     'url': 'https://nebplus2notes.com/class-12/english/ld/money-and-economy/'},
    {'chapter_id': 'class-12-english-humour', 'chapter_title': 'Unit 7: Humour', 'order': 7,
     'url': 'https://nebplus2notes.com/class-12/english/ld/humour/'},
    {'chapter_id': 'class-12-english-human-culture', 'chapter_title': 'Unit 8: Human Culture', 'order': 8,
     'url': 'https://nebplus2notes.com/class-12/english/ld/human-culture/'},
    {'chapter_id': 'class-12-english-ecology-and-environment', 'chapter_title': 'Unit 9: Ecology and Environment', 'order': 9,
     'url': 'https://nebplus2notes.com/class-12/english/ld/ecology-and-environment/'},
    {'chapter_id': 'class-12-english-career-opportunities', 'chapter_title': 'Unit 10: Career Opportunities', 'order': 10,
     'url': 'https://nebplus2notes.com/class-12/english/ld/career-opportunities/'},
    {'chapter_id': 'class-12-english-hobbies', 'chapter_title': 'Unit 11: Hobbies', 'order': 11,
     'url': 'https://nebplus2notes.com/class-12/english/ld/hobbies/'},
    {'chapter_id': 'class-12-english-animal-world', 'chapter_title': 'Unit 12: Animal World', 'order': 12,
     'url': 'https://nebplus2notes.com/class-12/english/ld/animal-world/'},
    {'chapter_id': 'class-12-english-history', 'chapter_title': 'Unit 13: History', 'order': 13,
     'url': 'https://nebplus2notes.com/class-12/english/ld/history/'},
    {'chapter_id': 'class-12-english-human-rights', 'chapter_title': 'Unit 14: Human Rights', 'order': 14,
     'url': 'https://nebplus2notes.com/class-12/english/ld/human-rights/'},
    {'chapter_id': 'class-12-english-leisure-and-entertainment', 'chapter_title': 'Unit 15: Leisure and Entertainment', 'order': 15,
     'url': 'https://nebplus2notes.com/class-12/english/ld/leisure-and-entertainment/'},
    {'chapter_id': 'class-12-english-fantasy', 'chapter_title': 'Unit 16: Fantasy', 'order': 16,
     'url': 'https://nebplus2notes.com/class-12/english/ld/fantasy/'},
    {'chapter_id': 'class-12-english-war-and-peace', 'chapter_title': 'Unit 17: War and Peace', 'order': 17,
     'url': 'https://nebplus2notes.com/class-12/english/ld/war-and-peace/'},
    {'chapter_id': 'class-12-english-music-and-creation', 'chapter_title': 'Unit 18: Music and Creation', 'order': 18,
     'url': 'https://nebplus2notes.com/class-12/english/ld/music-and-creation/'},
    {'chapter_id': 'class-12-english-migration-and-diaspora', 'chapter_title': 'Unit 19: Migration and Diaspora', 'order': 19,
     'url': 'https://nebplus2notes.com/class-12/english/ld/migration-and-diaspora/'},
    {'chapter_id': 'class-12-english-power-and-politics', 'chapter_title': 'Unit 20: Power and Politics', 'order': 20,
     'url': 'https://nebplus2notes.com/class-12/english/ld/power-and-politics/'},
    {'chapter_id': 'class-12-english-neighbours', 'chapter_title': 'Story 1: Neighbours', 'order': 21,
     'url': 'https://nebplus2notes.com/class-12/english/lit/ss/neighbours/'},
    {'chapter_id': 'class-12-english-a-respectable-woman', 'chapter_title': 'Story 2: A Respectable Woman', 'order': 22,
     'url': 'https://nebplus2notes.com/class-12/english/lit/ss/a-respectable-woman/'},
    {'chapter_id': 'class-12-english-a-devoted-son', 'chapter_title': 'Story 3: A Devoted Son', 'order': 23,
     'url': 'https://nebplus2notes.com/class-12/english/lit/ss/a-devoted-son/'},
    {'chapter_id': 'class-12-english-the-treasure-in-the-forest', 'chapter_title': 'Story 4: The Treasure in the Forest', 'order': 24,
     'url': 'https://nebplus2notes.com/class-12/english/lit/ss/the-treasure-in-the-forest/'},
    {'chapter_id': 'class-12-english-my-old-home', 'chapter_title': 'Story 5: My Old Home', 'order': 25,
     'url': 'https://nebplus2notes.com/class-12/english/lit/ss/my-old-home/'},
    {'chapter_id': 'class-12-english-half-closed-eyes-buddha', 'chapter_title': 'Story 6: The Half-closed Eyes of the Buddha and the Slowly Sinking Sun', 'order': 26,
     'url': None},
    {'chapter_id': 'class-12-english-a-very-old-man-with-enormous-wings', 'chapter_title': 'Story 7: A Very Old Man with Enormous Wings', 'order': 27,
     'url': 'https://nebplus2notes.com/class-12/english/lit/ss/a-very-old-man-with-enormous-wings/'},
    {'chapter_id': 'class-12-english-a-day', 'chapter_title': 'Poem 1: A Day', 'order': 28,
     'url': 'https://nebplus2notes.com/class-12/english/lit/poems/a-day/'},
    {'chapter_id': 'class-12-english-every-morning-i-wake', 'chapter_title': 'Poem 2: Every Morning I Wake', 'order': 29,
     'url': 'https://nebplus2notes.com/class-12/english/lit/poems/every-morning-i-wake/'},
    {'chapter_id': 'class-12-english-i-was-my-own-route', 'chapter_title': 'Poem 3: I Was My Own Route', 'order': 30,
     'url': 'https://nebplus2notes.com/class-12/english/lit/poems/i-was-my-own-route/'},
    {'chapter_id': 'class-12-english-the-awakening-age', 'chapter_title': 'Poem 4: The Awakening Age', 'order': 31,
     'url': 'https://nebplus2notes.com/class-12/english/lit/poems/the-awakening-age/'},
    {'chapter_id': 'class-12-english-soft-storm', 'chapter_title': 'Poem 5: Soft Storm', 'order': 32,
     'url': 'https://nebplus2notes.com/class-12/english/lit/poems/soft-storm/'},
    {'chapter_id': 'class-12-english-on-libraries', 'chapter_title': 'Essay 1: On Libraries', 'order': 33,
     'url': 'https://nebplus2notes.com/class-12/english/lit/essays/on-libraries/'},
    {'chapter_id': 'class-12-english-marriage-as-a-social-institution', 'chapter_title': 'Essay 2: Marriage as a Social Institution', 'order': 34,
     'url': 'https://nebplus2notes.com/class-12/english/lit/essays/marriage-as-a-social-institution/'},
    {'chapter_id': 'class-12-english-knowledge-and-wisdom', 'chapter_title': 'Essay 3: Knowledge and Wisdom', 'order': 35,
     'url': 'https://nebplus2notes.com/class-12/english/lit/essays/knowledge-and-wisdom/'},
    {'chapter_id': 'class-12-english-humility', 'chapter_title': 'Essay 4: Humility', 'order': 36,
     'url': 'https://nebplus2notes.com/class-12/english/lit/essays/humility/'},
    {'chapter_id': 'class-12-english-human-rights-and-the-age-of-inequality', 'chapter_title': 'Essay 5: Human Rights and the Age of Inequality', 'order': 37,
     'url': 'https://nebplus2notes.com/class-12/english/lit/essays/human-rights-and-the-age-of-inequality/'},
    {'chapter_id': 'class-12-english-a-matter-of-husbands', 'chapter_title': 'Play 1: A Matter of Husbands', 'order': 38,
     'url': 'https://nebplus2notes.com/class-12/english/lit/oap/a-matter-of-husbands/'},
    {'chapter_id': 'class-12-english-facing-death', 'chapter_title': 'Play 2: Facing Death', 'order': 39,
     'url': 'https://nebplus2notes.com/class-12/english/lit/oap/facing-death/'},
    {'chapter_id': 'class-12-english-the-bull', 'chapter_title': 'Play 3: The Bull', 'order': 40,
     'url': 'https://nebplus2notes.com/class-12/english/lit/oap/the-bull/'},
]

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
}

def html_to_markdown(element):
    if element is None:
        return ''
    result = []
    for child in element.children:
        if isinstance(child, NavigableString):
            text = str(child)
            text = text.replace('\xa0', ' ')
            text = text.replace('\u2019', "'")
            text = text.replace('\u2018', "'")
            text = text.replace('\u201c', '"')
            text = text.replace('\u201d', '"')
            text = text.replace('\u2013', '-')
            text = text.replace('\u2014', '--')
            text = text.replace('&ldquo;', '"').replace('&rdquo;', '"')
            text = text.replace('&rsquo;', "'").replace('&lsquo;', "'")
            text = text.replace('&ndash;', '-').replace('&mdash;', '--')
            result.append(text)
        elif child.name == 'h1':
            result.append('\n## ' + child.get_text(strip=True) + '\n')
        elif child.name == 'h2':
            result.append('\n## ' + child.get_text(strip=True) + '\n')
        elif child.name == 'h3':
            result.append('\n### ' + child.get_text(strip=True) + '\n')
        elif child.name == 'h4':
            result.append('\n#### ' + child.get_text(strip=True) + '\n')
        elif child.name == 'h5':
            result.append('\n##### ' + child.get_text(strip=True) + '\n')
        elif child.name == 'p':
            p_class = child.get('class', [])
            if 'text_image_in_post' in p_class:
                continue
            inner = html_to_markdown(child)
            if inner.strip():
                result.append('\n' + inner.strip() + '\n')
        elif child.name == 'b' or child.name == 'strong':
            inner = html_to_markdown(child)
            if inner.strip():
                result.append('**' + inner.strip() + '**')
        elif child.name == 'i' or child.name == 'em':
            inner = html_to_markdown(child)
            if inner.strip():
                result.append('*' + inner.strip() + '*')
        elif child.name == 'br':
            result.append('\n')
        elif child.name == 'a':
            href = child.get('href', '')
            if '/cdn-cgi/' in href or 'email-protection' in str(child.get('class', [])):
                result.append(child.get_text())
            else:
                result.append(child.get_text())
        elif child.name == 'img':
            src = child.get('src', '')
            alt = child.get('alt', '')
            if 'appstore' in src or 'playstore' in src:
                continue
            result.append(f'![{alt}]({src})')
        elif child.name == 'div':
            div_class = child.get('class', [])
            if 'app-buttons-in-post' in div_class:
                continue
            inner = html_to_markdown(child)
            if inner.strip():
                result.append(inner)
        elif child.name == 'table':
            rows = child.find_all('tr')
            for ri, row in enumerate(rows):
                cells = row.find_all(['th', 'td'])
                cell_texts = [c.get_text(strip=True) for c in cells]
                result.append('| ' + ' | '.join(cell_texts) + ' |')
                if ri == 0:
                    result.append('| ' + ' | '.join(['---'] * len(cells)) + ' |')
            result.append('\n')
        elif child.name == 'ul' or child.name == 'ol':
            for li in child.find_all('li', recursive=False):
                inner = html_to_markdown(li)
                result.append('- ' + inner.strip())
            result.append('\n')
        elif child.name == 'li':
            inner = html_to_markdown(child)
            result.append(inner.strip())
        elif child.name == 'blockquote':
            inner = html_to_markdown(child)
            lines = inner.strip().split('\n')
            for line in lines:
                result.append('> ' + line)
            result.append('\n')
        elif child.name == 'hr':
            result.append('\n---\n')
        elif child.name == 'span':
            inner = html_to_markdown(child)
            result.append(inner)
        elif child.name in ['script', 'style', 'nav', 'header', 'footer', 'noscript', 'iframe']:
            continue
        else:
            inner = html_to_markdown(child)
            result.append(inner)
    
    return ''.join(result)


def extract_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    
    for tag in soup.find_all(['script', 'style', 'nav', 'noscript', 'iframe']):
        tag.decompose()
    
    content_div = soup.find('div', class_='content')
    if not content_div:
        article = soup.find('article')
        if article:
            content_div = article.find('div', class_='content')
    
    if not content_div:
        article = soup.find('article')
        if article:
            content_div = article
    
    if not content_div:
        return '', ''
    
    app_divs = content_div.find_all('div', class_='app-buttons-in-post')
    for div in app_divs:
        div.decompose()
    app_ps = content_div.find_all('p', class_='text_image_in_post')
    for p in app_ps:
        p.decompose()
    
    markdown = html_to_markdown(content_div)
    
    markdown = re.sub(r'\n{3,}', '\n\n', markdown)
    markdown = re.sub(r'^\s+', '', markdown, flags=re.MULTILINE)
    markdown = markdown.strip()
    
    while '\n\n\n' in markdown:
        markdown = markdown.replace('\n\n\n', '\n\n')
    
    text_content = markdown
    
    question_answers = ''
    qa_markers = [
        '### Comprehension',
        '### Understanding the text',
        '### Reference to the context',
        '### Reference beyond the text',
        '### Critical Thinking',
        '## Comprehension',
        '## Understanding the text',
        '## Reference to the context',
        '## Reference beyond the text',
        '## Critical Thinking',
    ]
    first_qa_idx = len(text_content)
    for marker in qa_markers:
        idx = text_content.find(marker)
        if idx > 0 and idx < first_qa_idx:
            first_qa_idx = idx
    
    if first_qa_idx < len(text_content):
        question_answers = text_content[first_qa_idx:].strip()
    
    return text_content, question_answers


def scrape_chapter(chapter, session):
    url = chapter['url']
    if not url:
        print(f"  SKIPPED (no URL): {chapter['chapter_title']}")
        return None
    print(f"Fetching: {chapter['chapter_title']}")
    try:
        resp = session.get(url, headers=HEADERS, timeout=30)
        if resp.status_code == 404:
            print(f"  404 Not Found: {url}")
            return None
        resp.raise_for_status()
        text_content, question_answers = extract_content(resp.text)
        return {
            'grade_level': 'Class 12',
            'subject': 'English',
            'chapter_id': chapter['chapter_id'],
            'chapter_title': chapter['chapter_title'],
            'order': chapter['order'],
            'text_content': text_content,
            'question_answers': question_answers,
        }
    except Exception as e:
        print(f"  ERROR: {e}")
        return None


def main():
    output_file = sys.argv[1] if len(sys.argv) > 1 else 'class12_english_content.json'
    
    session = requests.Session()
    results = []
    errors = []
    
    for i, chapter in enumerate(CHAPTERS):
        data = scrape_chapter(chapter, session)
        if data:
            results.append(data)
            tc = len(data.get('text_content', ''))
            qa = len(data.get('question_answers', ''))
            print(f"  OK (text={tc} chars, qa={qa} chars)")
        else:
            if chapter['url']:
                errors.append(chapter['chapter_title'])
            print(f"  FAILED/SKIPPED")
        time.sleep(1.5)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    print(f"\nDone! {len(results)} chapters scraped, {len(errors)} errors.")
    print(f"Saved to: {output_file}")
    if errors:
        print(f"Errors: {errors}")

if __name__ == '__main__':
    main()