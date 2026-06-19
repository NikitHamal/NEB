#!/usr/bin/env python3
"""NEB/SEE result scraper with caching.

Supports multiple official result sources:
- neb.ntc.net.np  (NEB Class 12)
- see.ntc.net.np  (SEE Class 10)

Results are cached in Django's cache framework so repeated lookups
for the same symbol number are instant and don't hammer the origin.
"""

import logging
import re
import time
from urllib.parse import urlencode
from django.core.cache import cache

logger = logging.getLogger('nebians.services.result_scraper')

CACHE_PREFIX = 'neb_result_'
CACHE_TTL = None  # Results never change after publication; cache forever so lookups survive official site downtime.

# ── source adapters ──────────────────────────────────────────────────

class SourceAdapter:
    """Base interface for a result-source scraper."""
    name = ''
    exam_label = ''

    def get_form_token(self, batch: str = '') -> tuple[str, str]:
        """GET the form page and extract (token_name, token_value)."""
        raise NotImplementedError

    def form_url_for_batch(self, batch: str) -> str:
        """Return the form URL for a given batch/year."""
        return self.form_url

    def result_url_for_batch(self, batch: str) -> str:
        """Return the result POST URL for a given batch/year."""
        return self.result_url

    def fetch_result(self, symbol: str, dob: str, token_name: str, token_value: str, batch: str = '') -> dict | None:
        """POST credentials and return parsed result dict, or None if not found."""
        raise NotImplementedError

    def parse_result(self, html: str, symbol: str) -> dict | None:
        """Extract student info + grades from the result HTML."""
        raise NotImplementedError


class NtcNEBAdapter(SourceAdapter):
    """Scraper for neb.ntc.net.np (NEB Class 12)."""
    name = 'neb.ntc.net.np'
    exam_label = 'NEB Class 12'
    form_url = 'https://neb.ntc.net.np/'
    result_url = 'https://neb.ntc.net.np/results.php'

    def get_form_token(self, batch: str = '') -> tuple[str, str]:
        import urllib.request
        url = self.form_url_for_batch(batch)
        req = urllib.request.Request(url, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        resp = urllib.request.urlopen(req, timeout=20)
        html = resp.read().decode('utf-8', errors='replace')
        m = re.search(r'<input[^>]+name="([A-F0-9]+)"[^>]+value="([A-F0-9]+)"', html)
        if m:
            return m.group(1), m.group(2)
        return '', ''

    def form_url_for_batch(self, batch: str) -> str:
        if batch and batch != '2083':
            return f'https://neb.ntc.net.np/{batch}/'
        return self.form_url

    def result_url_for_batch(self, batch: str) -> str:
        if batch and batch != '2083':
            return f'https://neb.ntc.net.np/{batch}/results.php'
        return self.result_url

    def fetch_result(self, symbol: str, dob: str, token_name: str, token_value: str, batch: str = '') -> dict | None:
        import urllib.request
        url = self.result_url_for_batch(batch)
        data = urlencode({
            'symbol': symbol,
            'dob': dob,
            token_name: token_value,
            'submit': 'Submit'
        }).encode()
        req = urllib.request.Request(url, data=data, method='POST')
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
        try:
            resp = urllib.request.urlopen(req, timeout=30)
            html = resp.read().decode('utf-8', errors='replace')
        except urllib.error.HTTPError as e:
            if e.code == 404:
                return None  # site not live yet
            raise
        if ('not found' in html.lower() or 'invalid' in html.lower()
            or 'record not found' in html.lower()
            or 'not a valid' in html.lower()):
            return None
        return self.parse_result(html, symbol)

    def parse_result(self, html: str, symbol: str) -> dict | None:
        """Parse NEB result HTML into a structured dict."""
        result = {
            'symbol': symbol,
            'source': self.name,
            'exam': self.exam_label,
            'student_name': '',
            'school': '',
            'subjects': [],
            'gpa': '',
            'grade': '',
            'raw_html': html,
        }

        # Try to find student name — varies by year/format
        for pattern in [
            r'<b>Name</b>\s*:\s*([^<]+)',            # current NEB: <b>Name</b> : LAXMI NEPAL
            r'Student\s*Name[^:]*:\s*([^<]+)',
            r'Name[^:]*:\s*([^<]+)',
            r'<strong>([^<]+)</strong>\s*</td>\s*<td[^>]*>\d',
        ]:
            m = re.search(pattern, html, re.I)
            if m:
                result['student_name'] = m.group(1).strip()
                break

        # School/college
        m = re.search(r'<b>School\s*Name</b>\s*:\s*([^<]+)', html, re.I)
        if not m:
            m = re.search(r'(?:School|College|Institution)\s*[^:]*:\s*([^<]+)', html, re.I)
        if m:
            result['school'] = m.group(1).strip()

        # GPA — try current table format first
        m = re.search(r'<td[^>]*colspan="4"[^>]*>GPA\s*:\s*</td>\s*<td[^>]*><b>([\d.]+)', html, re.I)
        if m:
            result['gpa'] = m.group(1).strip()
        else:
            m = re.search(r'(?:GPA|Grade\s*Point\s*Average)[^:]*:\s*([\d.]+)', html, re.I)
            if m:
                result['gpa'] = m.group(1).strip()

        # Parse subject table — find the grade table first
        table_m = re.search(
            r'<table[^>]*class="border-main"[^>]*>.*?<tr[^>]*>.*?</tr>\s*(.*?)</table>',
            html, re.I | re.S
        )
        if table_m:
            table_html = table_m.group(1)
        else:
            # fallback: find any table with GRADE-SHEET nearby
            m = re.search(r'GRADE\s*[- ]*\s*SHEET.*?<table[^>]*>(.*?)</table>', html, re.I | re.S)
            if m:
                # skip header row
                inner = re.sub(r'<tr[^>]*>.*?<b>.*?</b>.*?</tr>', '', m.group(1), count=1, flags=re.I | re.S)
                table_html = inner
            else:
                table_html = ''

        for row in re.findall(
            r'<tr[^>]*>\s*<td[^>]*>(.*?)</td>\s*<td[^>]*>(.*?)</td>\s*<td[^>]*>(.*?)</td>\s*<td[^>]*>(.*?)</td>\s*<td[^>]*>(.*?)</td>',
            table_html, re.I | re.S
        ):
            code = re.sub(r'<[^>]+>', '', row[0]).strip()
            name = re.sub(r'<[^>]+>', '', row[1]).strip()
            credit = re.sub(r'<[^>]+>', '', row[2]).strip()
            grade = re.sub(r'<[^>]+>', '', row[3]).strip()
            gp = re.sub(r'<[^>]+>', '', row[4]).strip()

            # Skip header row
            if name.lower() in ('subject', 'subjects') or code.lower() == 'code':
                continue
            # Skip GPA summary row
            if 'gpa' in name.lower() or 'gpa' in code.lower():
                continue

            if name and grade:
                result['subjects'].append({
                    'code': code,
                    'name': name,
                    'credit_hour': credit,
                    'grade': grade,
                    'grade_point': gp,
                })

        # Simpler fallback: td pairs in a table
        if not result['subjects']:
            td_pairs = re.findall(r'<td[^>]*>([^<]+)</td>\s*<td[^>]*>([^<]+)</td>', html)
            # Attempt subject-grade extraction from pairs
            known = ['English', 'Nepali', 'Math', 'Science', 'Social', 'Physics', 'Chemistry',
                     'Biology', 'Account', 'Economics', 'Computer', 'Optional']
            for a, b in td_pairs:
                a = a.strip()
                b = b.strip()
                if any(k.lower() in a.lower() for k in known) and re.match(r'^[A-E][+-]?$', b):
                    result['subjects'].append({
                        'code': '',
                        'name': a,
                        'credit_hour': '',
                        'grade': b,
                        'grade_point': '',
                    })

        # Determine overall grade from GPA
        if result['gpa']:
            try:
                gp = float(result['gpa'])
                if gp >= 3.6: result['grade'] = 'A+'
                elif gp >= 3.2: result['grade'] = 'A'
                elif gp >= 2.8: result['grade'] = 'B+'
                elif gp >= 2.4: result['grade'] = 'B'
                elif gp >= 2.0: result['grade'] = 'C+'
                elif gp >= 1.6: result['grade'] = 'C'
                elif gp >= 1.2: result['grade'] = 'D+'
                elif gp >= 0.8: result['grade'] = 'D'
                else: result['grade'] = 'E'
            except ValueError:
                pass

        return result if (result['subjects'] or result['student_name']) else None


class NtcSEEAdapter(SourceAdapter):
    """Scraper for see.ntc.net.np (SEE / Class 10)."""
    name = 'see.ntc.net.np'
    exam_label = 'SEE (Class 10)'
    form_url = 'https://see.ntc.net.np/'
    result_url = 'https://see.ntc.net.np/results.php'

    def get_form_token(self, batch: str = '') -> tuple[str, str]:
        import urllib.request
        url = self.form_url_for_batch(batch)
        req = urllib.request.Request(url, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        resp = urllib.request.urlopen(req, timeout=20)
        html = resp.read().decode('utf-8', errors='replace')
        m = re.search(r'<input[^>]+name="([A-F0-9]+)"[^>]+value="([A-F0-9]+)"', html)
        if m:
            return m.group(1), m.group(2)
        return '', ''

    def form_url_for_batch(self, batch: str) -> str:
        if batch and batch != '2083':
            return f'https://see.ntc.net.np/{batch}/'
        return self.form_url

    def result_url_for_batch(self, batch: str) -> str:
        if batch and batch != '2083':
            return f'https://see.ntc.net.np/{batch}/results.php'
        return self.result_url

    def fetch_result(self, symbol: str, dob: str, token_name: str, token_value: str, batch: str = '') -> dict | None:
        import urllib.request
        url = self.result_url_for_batch(batch)
        data = urlencode({
            'symbol': symbol,
            'dob': dob,
            token_name: token_value,
            'submit': 'Submit'
        }).encode()
        req = urllib.request.Request(url, data=data, method='POST')
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
        try:
            resp = urllib.request.urlopen(req, timeout=30)
            html = resp.read().decode('utf-8', errors='replace')
        except urllib.error.HTTPError as e:
            if e.code == 404:
                return None
            raise
        if 'not found' in html.lower() or 'invalid' in html.lower():
            return None
        return self.parse_result(html, symbol)

    def parse_result(self, html: str, symbol: str) -> dict | None:
        result = {
            'symbol': symbol,
            'source': self.name,
            'exam': self.exam_label,
            'student_name': '',
            'school': '',
            'subjects': [],
            'gpa': '',
            'grade': '',
            'raw_html': html,
        }
        m = re.search(r'Student\s*Name[^:]*:\s*([^<]+)', html, re.I)
        if m:
            result['student_name'] = m.group(1).strip()
        m = re.search(r'(School|College)[^:]*:\s*([^<]+)', html, re.I)
        if m:
            result['school'] = m.group(2).strip()
        m = re.search(r'(?:GPA|Grade\s*Point)[^:]*:\s*([\d.]+)', html, re.I)
        if m:
            result['gpa'] = m.group(1).strip()

        rows = re.findall(
            r'<tr[^>]*>\s*<td[^>]*>(.*?)</td>\s*<td[^>]*>(.*?)</td>\s*<td[^>]*>(.*?)</td>\s*<td[^>]*>(.*?)</td>',
            html, re.I | re.S
        )
        if rows:
            for row in rows:
                name = re.sub(r'<[^>]+>', '', row[0]).strip()
                credit = re.sub(r'<[^>]+>', '', row[1]).strip()
                grade = re.sub(r'<[^>]+>', '', row[2]).strip()
                gp = re.sub(r'<[^>]+>', '', row[3]).strip()
                if name and grade:
                    result['subjects'].append({
                        'code': '',
                        'name': name,
                        'credit_hour': credit,
                        'grade': grade,
                        'grade_point': gp,
                    })

        if result['gpa']:
            try:
                gp = float(result['gpa'])
                if gp >= 3.6: result['grade'] = 'A+'
                elif gp >= 3.2: result['grade'] = 'A'
                elif gp >= 2.8: result['grade'] = 'B+'
                elif gp >= 2.4: result['grade'] = 'B'
                elif gp >= 2.0: result['grade'] = 'C+'
                elif gp >= 1.6: result['grade'] = 'C'
                elif gp >= 1.2: result['grade'] = 'D+'
                elif gp >= 0.8: result['grade'] = 'D'
                else: result['grade'] = 'E'
            except ValueError:
                pass

        return result if (result['subjects'] or result['student_name']) else None


class SEEEdusanjalAdapter(SourceAdapter):
    """Scraper for see.edusanjal.com (SEE / Class 10, no DOB needed)."""
    name = 'see.edusanjal.com'
    exam_label = 'SEE (Class 10)'
    api_url = 'https://see.edusanjal.com/api/result'

    def get_form_token(self, batch: str = '') -> tuple[str, str]:
        return 'bypass', '1'

    def fetch_result(self, symbol: str, dob: str, token_name: str, token_value: str, batch: str = '') -> dict | None:
        import urllib.request, json as pyjson
        url = f'{self.api_url}/{symbol.strip()}'
        req = urllib.request.Request(url, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'application/json',
        })
        try:
            resp = urllib.request.urlopen(req, timeout=20)
            body = resp.read().decode('utf-8', errors='replace')
        except urllib.error.HTTPError as e:
            if e.code in (404, 500):
                return None
            raise

        try:
            data = pyjson.loads(body)
        except (ValueError, pyjson.JSONDecodeError):
            return None

        return self._parse_api_response(data, symbol)

    def _parse_api_response(self, data: dict, symbol: str) -> dict | None:
        if not data or data.get('error'):
            return None

        result = {
            'symbol': symbol,
            'source': self.name,
            'exam': self.exam_label,
            'student_name': '',
            'school': '',
            'subjects': [],
            'gpa': '',
            'grade': '',
        }

        result['student_name'] = data.get('name') or data.get('student_name') or ''
        result['school'] = data.get('school') or data.get('college') or ''
        result['gpa'] = str(data.get('gpa') or data.get('grade_point_average') or '')

        subjects_raw = data.get('subjects') or data.get('grades') or []
        for s in subjects_raw:
            if isinstance(s, dict):
                result['subjects'].append({
                    'code': str(s.get('code', '')),
                    'name': str(s.get('name', s.get('subject', ''))),
                    'credit_hour': str(s.get('credit_hour', s.get('cr', ''))),
                    'grade': str(s.get('grade', s.get('gp', ''))),
                    'grade_point': str(s.get('grade_point', s.get('gpa', ''))),
                })

        if result['gpa']:
            try:
                gp = float(result['gpa'])
                if gp >= 3.6: result['grade'] = 'A+'
                elif gp >= 3.2: result['grade'] = 'A'
                elif gp >= 2.8: result['grade'] = 'B+'
                elif gp >= 2.4: result['grade'] = 'B'
                elif gp >= 2.0: result['grade'] = 'C+'
                elif gp >= 1.6: result['grade'] = 'C'
                elif gp >= 1.2: result['grade'] = 'D+'
                elif gp >= 0.8: result['grade'] = 'D'
                else: result['grade'] = 'E'
            except ValueError:
                pass

        return result if result['subjects'] else None


# ── adapter registry ─────────────────────────────────────────────────

ADAPTERS: dict[str, SourceAdapter] = {
    'neb': NtcNEBAdapter(),
    'see': SEEEdusanjalAdapter(),
}

EXAM_CHOICES = [(k, v.exam_label) for k, v in ADAPTERS.items()]


# ── public API ───────────────────────────────────────────────────────

def check_result(exam: str, symbol: str, dob: str, batch: str = '') -> dict:
    """Check a result.

    Args:
        exam: 'neb' or 'see'
        symbol: symbol number
        dob: date of birth (YYYY/MM/DD or YYYY-MM-DD)
        batch: exam year/batch (e.g. '2080', '2081', '2082', '2083')

    Returns:
        dict with keys: success, data/error, cached
    """
    adapter = ADAPTERS.get(exam)
    if not adapter:
        return {'success': False, 'error': f'Unknown exam: {exam}'}

    cache_key = f'{CACHE_PREFIX}{exam}:{batch}:{symbol}'

    # Check cache first
    cached = cache.get(cache_key)
    if cached:
        cached['_cached'] = True
        return {'success': True, 'data': cached, 'cached': True}

    # Fetch from source
    try:
        token_name, token_value = adapter.get_form_token(batch=batch)
        if not token_name:
            return {'success': False, 'error': 'Source site is currently unavailable (token not found)'}
        time.sleep(0.5)  # rate-limit courtesy
        result = adapter.fetch_result(symbol, dob, token_name, token_value, batch=batch)
    except Exception as e:
        logger.exception('result_scraper error for %s %s batch=%s', exam, symbol, batch)
        import urllib.error
        if isinstance(e, urllib.error.HTTPError):
            if e.code == 404:
                if cached := cache.get(cache_key):
                    cached['_cached'] = True
                    return {'success': True, 'data': cached, 'cached': True}
                return {
                    'success': False,
                    'error': f'The result page for batch {batch} was not found on the official board. It might not be published yet.'
                }
            if cached := cache.get(cache_key):
                cached['_cached'] = True
                return {'success': True, 'data': cached, 'cached': True}
            return {'success': False, 'error': f'Official server error (HTTP {e.code}). Please try again later.'}
        elif isinstance(e, urllib.error.URLError):
            msg = 'Connection timed out or failed. The official result server may be overloaded or down.'
            if cached := cache.get(cache_key):
                msg += ' Serving previously cached result.'
                cached['_cached'] = True
                return {'success': True, 'data': cached, 'cached': True}
            return {'success': False, 'error': msg}
        return {'success': False, 'error': f'Error fetching result: {str(e)}'}

    if result is None:
        return {'success': False, 'error': 'Record not found. Check your symbol number and date of birth.'}

    # Tag with batch in result
    result['batch'] = batch

    # Strip raw_html from everything — it's large, only needed for debugging
    result.pop('raw_html', None)

    cache.set(cache_key, result, CACHE_TTL)

    result['_cached'] = False
    return {'success': True, 'data': result, 'cached': False}
