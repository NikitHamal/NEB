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
