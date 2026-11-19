"""Wave 32 Nepal: Ministry of Education scholarship categories for 2081/82 (Edusanjal news of 9 February 2025 and OnlineKhabar English of 9 February 2025,
both quoting the ministry's published details), CTEVT special scholarship 2082 notice (collegenp.com: NPR 3,500 monthly stipend, 1,500 travel, 2,500 clothing,
free hostel). Read on 2026-11-20. Where the two news pages disagree (clothing or uniform allowance NPR 2,000 or 2,500) the text says both.
No count of awards is printed for these schemes, so they are open calls like the wave 30 city Class 11 scholarships.
"""

SCHOLARSHIPS_ADD = [
    {'id': 's-moest-poor', 'name': 'Ministry of Education scholarship for economically disadvantaged students (Class 11 and 12 and technical)', 'scope': 'nepal', 'levels': ['diploma', 'bachelor'],
     'by': 'Ministry of Education, Science and Technology (MoEST), Government of Nepal',
     'covers': 'In 2081/82 the ministry set aside NPR 600 million for economically disadvantaged students: NPR 24,000 a year for Class 11 and 12 science, NPR 18,000 a year for other Class 11 and 12 subjects and NPR 6,000 a year for Class 6 to 10 (both news pages). For technical education the same news pages print NPR 15,000 a year for general courses and NPR 21,000 a year for technical courses.',
     'who': 'Students from economically disadvantaged families who study in a community school or approved institution; the school or local level confirms the family situation. The ministry did not print a student count for this scheme in the pages read.',
     'how': 'Ask the school principal or your local level education unit about the yearly list and documents; the ministry publishes quotas through the local level, not through a single national form.',
     'link': 'https://moe.gov.np', 'type': 'Government'},
    {'id': 's-moest-tech', 'name': 'Ministry of Education technical education scholarship for Dalit, Muslim and marginalised students', 'scope': 'nepal', 'levels': ['diploma'],
     'by': 'Ministry of Education, Science and Technology (MoEST), delivered through CTEVT',
     'covers': 'A budget of NPR 59.4 million in 2081/82 pays a monthly stipend of NPR 3,500, a yearly travel allowance of NPR 1,500 and a yearly clothing allowance (NPR 2,000 on Edusanjal, NPR 2,500 on OnlineKhabar and in the CTEVT special scholarship 2082 notice). The CTEVT notice adds free hostel accommodation.',
     'who': 'Students from Dalit, Muslim, disadvantaged and marginalised communities who qualify for a CTEVT diploma or pre diploma seat. The CTEVT special scholarship (480 seats for 2083, with 78 local levels without access to technical education) is the main way seats are given.',
     'how': 'Apply on the yearly CTEVT special scholarship notice (see the CTEVT special scholarship in this list); the stipend rates above are the ministry figures for that scheme.',
     'link': 'https://ctevt.org.np', 'type': 'Government'},
    {'id': 's-moest-higher', 'name': 'Ministry of Education higher education scholarship for martyr, conflict victim, Kamalari, Muslim women and disabled students', 'scope': 'nepal', 'levels': ['bachelor', 'master'],
     'by': 'Ministry of Education, Science and Technology (MoEST), Government of Nepal',
     'covers': 'NPR 24,000 a year at bachelor and master level (Edusanjal, 9 February 2025, quoting the ministry for 2081/82).',
     'who': 'Children of martyrs, conflict victims, freed Kamalari, Muslim women and students with disabilities who study at bachelor or master level. A separate residential scheme pays NPR 50,000 a year to students with disabilities, freed Kamlari, marginalised students, street children, HIV affected students and Badi community students (12,065 students, NPR 603.2 million, OnlineKhabar).',
     'how': 'Apply through your campus or the university scholarship notice that follows the ministry call; keep the proof of category (martyr or conflict victim certificate, disability card or local level letter).',
     'link': 'https://moe.gov.np', 'type': 'Government'},
]

SCHOLARSHIP_NOTE_ADD = {
    's-quota': 'In 2081/82 the ministry reported NPR 5.11 billion for 10,594 students under the Medical Education Scholarship (Edusanjal and OnlineKhabar, 9 February 2025).',
}

FAQ_ADD = [
    {'id': 'fw32-9', 'topic': 'general', 'q': 'How much does the Nepal government spend on scholarships, and who gets the money?',
     'a': ('The Ministry of Education, Science and Technology said on 9 February 2025 that it had set aside NPR 7.39 billion for scholarships in 2081/82, for about 1.5 million students from primary to higher and technical education (OnlineKhabar and Edusanjal). '
           'The biggest lines: NPR 5.11 billion for 10,594 students in medical education, NPR 603.2 million for 12,065 students on residential scholarships (NPR 50,000 a year each), NPR 210 million for 552,000 Dalit students in Class 1 to 5, '
           'NPR 600 million for economically disadvantaged students (NPR 24,000 a year in Class 11 and 12 science, NPR 18,000 in other subjects, NPR 6,000 in Class 6 to 10) and NPR 59.4 million for technical education. Karnali girls in Class 1 to 5 get NPR 1,000 a year. '
           'Ask your school or local level which list your name can be put on, because most of these do not have a national online form.'),
     'go': []},
    {'id': 'fw32-10', 'topic': 'after10', 'q': 'I am Dalit, Muslim or from a marginalised family: what does a CTEVT diploma cost me?',
     'a': ('Nothing, if you get a seat in the special scholarship. The ministry says Dalit, Muslim and marginalised students in technical education get a monthly stipend of NPR 3,500, a yearly travel allowance of NPR 1,500 and a clothing allowance (NPR 2,000 on one page, NPR 2,500 on another); '
           'the CTEVT special scholarship notice also lists free hostel accommodation. CTEVT announced 480 seats for 2083 (457 diploma and 23 pre diploma) for these groups and for 78 local levels where technical education had not reached. '
           'For the 3,417 classified (free) seats, half go to the general group and half to targeted groups. A student who got a CTEVT scholarship once cannot get another, and must serve where the government assigns after finishing if it asks.'),
     'go': ['dip-engineering']},
]
