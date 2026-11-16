"""What a profile page needs to know about a person's school, or about an institution's people."""
from api import institutions as svc
from api.models_institutions import Institution

from .view_helpers import _avatar_url


def school_context(profile_user):
    out = {'school_slug': profile_user.school_slug or '', 'school_url': '', 'school_external': False,
           'institution_people': None}
    if profile_user.role != 'institution':
        if profile_user.school_slug:
            inst = Institution.objects.filter(slug=profile_user.school_slug).only(
                'slug', 'website', 'verified', 'claimed_by').select_related('claimed_by').first()
            if inst and inst.verified and inst.claimed_by_id:
                out['school_url'] = '/app/profile/%s/' % inst.claimed_by.username
            elif inst and inst.website:
                out['school_url'] = inst.website
                out['school_external'] = True
            elif inst:
                out['school_url'] = '/app/schools/%s/' % inst.slug
        elif profile_user.school_username:
            out['school_url'] = '/app/profile/%s/' % profile_user.school_username
        return out
    inst = Institution.objects.filter(claimed_by=profile_user).first()
    if not inst:
        return out
    counts = svc.people_counts(inst)
    people = [{
        'username': u.username, 'name': u.display_name or u.username, 'photo': _avatar_url(u),
        'role': 'Teacher' if u.role == 'teacher' else 'Student',
    } for u in svc.people_list(inst, 18)]
    out['institution_people'] = {'slug': inst.slug, 'counts': counts, 'people': people, 'verified': inst.verified,
                                 'website': inst.website, 'kind': inst.kind_label}
    return out


def _money(n):
    return 'NPR {:,}'.format(n) if n else ''


def folio_context(inst):
    """The claimed institution's portfolio as display rows for the school page, or None while it is empty."""
    from api import institution_profile as ip
    d = ip.get(inst)
    if not d:
        return None

    def names(key, rows):
        label = dict(rows)
        return [label[v] for v in d.get(key, []) if v in label]

    facts = []

    def add(label, value):
        if value not in (None, '', []):
            facts.append({'label': label, 'value': value})

    add('Established', inst.est)
    add('Principal', ' · '.join(x for x in (d.get('principal'), d.get('principalTitle')) if x))
    add('Ownership', dict(ip.OWNERSHIP).get(d.get('ownership')))
    add('Medium', ', '.join(names('mediums', ip.MEDIUMS)))
    add('Students', d.get('students'))
    add('Teachers', d.get('teachers'))
    add('Staff', d.get('staff'))
    add('Classrooms', d.get('classrooms'))
    lo, hi = d.get('feeMin'), d.get('feeMax')
    add('Yearly fee', _money(lo) if lo and (not hi or hi == lo) else ' to '.join(x for x in (_money(lo), _money(hi)) if x))
    contact = [x for x in (d.get('address'), d.get('phone'), d.get('email')) if x]
    out = {
        'about': d.get('about', ''), 'motto': d.get('motto', ''), 'facts': facts,
        'levels': names('levels', ip.LEVELS), 'streams': names('streams', ip.STREAMS),
        'facilities': names('facilities', ip.FACILITIES), 'affiliations': names('affiliations', ip.AFFILIATIONS),
        'branches': d.get('branches') or [], 'programs': d.get('programs') or [],
        'admission_open': bool(d.get('admissionOpen')), 'admission_note': d.get('admissionNote', ''),
        'contact': contact, 'email': d.get('email', ''),
        'socials': [{'name': k, 'url': v} for k, v in (d.get('socials') or {}).items()],
    }
    return out if (facts or any(out[k] for k in ('about', 'levels', 'facilities', 'branches', 'programs', 'contact'))) else None
