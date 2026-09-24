from django.test import Client, TestCase, RequestFactory
from django.contrib.auth.models import User as DjangoUser
from api.models import (
    AccountDeletionRequest, Announcement, BlogComment, BlogCommentLike,
    Bookmark, EditHistory, FCMToken, Follow, Notification, Poll, PollOption,
    PollVote, Post, PostLike, Reply, ReplyLike, Resource, ResourceComment,
    ResourceCommentLike, ResourceLike, ResourceRequest, User, UserPhoto,
)
from api.security import get_user_by_auth_token, issue_auth_token
from api.services import delete_user_account
from web.views_admin import admin_pending_resources


class AdminPendingResourcesTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.admin_user = User.objects.create(
            id='admin_platform_user',
            username='admin_platform',
            created_at=1000,
            is_admin=True,
        )
        self.raw_token = issue_auth_token(self.admin_user)

        # Group 1 (3 resources)
        Resource.objects.create(
            id='res_g1_1',
            title='Group 1 Lead',
            subject='Physics',
            grade_level='12',
            type='PDF',
            approval_status='pending',
            upload_group_id='group_1',
            is_lead=True,
            added_at=1000
        )
        Resource.objects.create(
            id='res_g1_2',
            title='Group 1 Part 2',
            subject='Physics',
            grade_level='12',
            type='PDF',
            approval_status='pending',
            upload_group_id='group_1',
            is_lead=False,
            added_at=1001
        )
        Resource.objects.create(
            id='res_g1_3',
            title='Group 1 Part 3',
            subject='Physics',
            grade_level='12',
            type='PDF',
            approval_status='pending',
            upload_group_id='group_1',
            is_lead=False,
            added_at=1002
        )

        # Group 2 (2 resources)
        Resource.objects.create(
            id='res_g2_1',
            title='Group 2 Lead',
            subject='Chemistry',
            grade_level='11',
            type='PDF',
            approval_status='pending',
            upload_group_id='group_2',
            is_lead=True,
            added_at=2000
        )
        Resource.objects.create(
            id='res_g2_2',
            title='Group 2 Part 2',
            subject='Chemistry',
            grade_level='11',
            type='PDF',
            approval_status='pending',
            upload_group_id='group_2',
            is_lead=False,
            added_at=2001
        )

        # Single Resource
        Resource.objects.create(
            id='res_single_1',
            title='Single Resource',
            subject='Math',
            grade_level='10',
            type='PDF',
            approval_status='pending',
            upload_group_id='',
            is_lead=True,
            added_at=3000
        )

    def test_admin_pending_resources_query_count(self):
        request = self.factory.get('/admin/resources/pending/')
        request.session = {'auth_token': self.raw_token}

        with self.assertNumQueries(2):
            response = admin_pending_resources(request)

        self.assertEqual(response.status_code, 200)

    def test_admin_pending_resources_via_client(self):
        session = self.client.session
        session['auth_token'] = self.raw_token
        session.save()

        response = self.client.get('/admin/resources/pending/')

        self.assertEqual(response.status_code, 200)
        pending_resources = response.context['pending_resources']
        self.assertEqual(len(pending_resources), 3)

        # Check group 1
        g1 = pending_resources[0]
        self.assertEqual(g1['title'], 'Group 1 Lead')
        self.assertEqual(len(g1['group_files']), 3)

        # Check group 2
        g2 = pending_resources[1]
        self.assertEqual(g2['title'], 'Group 2 Lead')
        self.assertEqual(len(g2['group_files']), 2)

        # Check single resource
        single = pending_resources[2]
        self.assertEqual(single['title'], 'Single Resource')
        self.assertEqual(len(single['group_files']), 1)


class AdminAccountAccessTests(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            id='platform_admin',
            username='platform_admin',
            display_name='Platform Admin',
            gender='other',
            class_level='12',
            created_at=1000,
            is_admin=True,
        )
        self.raw_token = issue_auth_token(self.user)
        session = self.client.session
        session['auth_token'] = self.raw_token
        session['user_data'] = {
            'id': self.user.id,
            'username': self.user.username,
            'display_name': self.user.display_name,
            'gender': self.user.gender,
            'class_level': self.user.class_level,
            'is_admin': True,
        }
        session.save()

    def test_admin_account_enters_panel_without_separate_login(self):
        response = self.client.get('/admin/')
        self.assertRedirects(response, '/admin/dashboard/')
        self.assertEqual(self.client.get('/admin/users/').status_code, 200)
        self.assertEqual(self.client.get('/backgroundagent/').status_code, 200)
        self.assertContains(self.client.get('/'), 'Admin Panel')

    def test_promotion_grants_existing_account_session_access(self):
        self.user.is_admin = False
        self.user.save(update_fields=['is_admin'])
        self.assertEqual(self.client.get('/admin/').status_code, 403)

        self.user.is_admin = True
        self.user.save(update_fields=['is_admin'])
        response = self.client.get('/admin/')
        self.assertRedirects(response, '/admin/dashboard/')

    def test_demotion_removes_access_immediately(self):
        self.user.is_admin = False
        self.user.save(update_fields=['is_admin'])
        self.assertEqual(self.client.get('/admin/').status_code, 403)

    def test_private_profile_admin_keeps_panel_access(self):
        self.user.is_locked = True
        self.user.save(update_fields=['is_locked'])
        response = self.client.get('/admin/')
        self.assertRedirects(response, '/admin/dashboard/')

    def test_banned_admin_loses_panel_access(self):
        self.user.is_banned = True
        self.user.save(update_fields=['is_banned'])
        response = self.client.get('/admin/')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/login/?next=/admin/dashboard/')

    def test_revoked_token_loses_panel_access(self):
        token_row = self.user.auth_tokens.get()
        token_row.revoked_at = 1
        token_row.save(update_fields=['revoked_at'])
        response = self.client.get('/admin/')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/login/?next=/admin/dashboard/')
        with self.assertRaises(User.DoesNotExist):
            get_user_by_auth_token(self.raw_token)

    def test_legacy_session_flag_does_not_grant_access(self):
        self.client = Client()
        session = self.client.session
        session['is_admin'] = True
        session.save()
        response = self.client.get('/admin/')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/login/?next=/admin/dashboard/')

    def test_separate_django_staff_login_does_not_grant_panel_access(self):
        self.client = Client()
        staff_user = DjangoUser.objects.create_user(
            username='separate_staff',
            password='password',
            is_staff=True,
        )
        self.client.force_login(staff_user)
        response = self.client.get('/admin/')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/login/?next=/admin/dashboard/')

    def test_admin_actions_record_the_platform_account(self):
        resource = Resource.objects.create(
            id='review_resource',
            title='Review resource',
            subject='Physics',
            grade_level='12',
            type='PDF',
            approval_status='pending',
            added_at=4000,
        )
        response = self.client.post('/admin/resources/pending/', {
            'resource_id': resource.id,
            'action': 'approve',
        })
        self.assertEqual(response.status_code, 302)
        resource.refresh_from_db()
        self.assertEqual(resource.reviewed_by_id, self.user.id)

    def test_admin_logout_revokes_the_platform_session(self):
        response = self.client.get('/admin/logout/')
        self.assertRedirects(response, '/')
        self.assertNotIn('auth_token', self.client.session)
        with self.assertRaises(User.DoesNotExist):
            get_user_by_auth_token(self.raw_token)


class AdminAccountDeletionTests(TestCase):
    def _login_admin(self):
        admin = User.objects.create(
            id='deletion_admin', username='deletion_admin',
            created_at=1000, is_admin=True,
        )
        session = self.client.session
        session['auth_token'] = issue_auth_token(admin)
        session.save()
        return admin

    def _build_full_world(self):
        other = User.objects.create(
            id='w_other', username='w_other', created_at=1,
            follower_count=1, following_count=1,
            likes_received_count=2, unread_notification_count=1,
        )
        doomed = User.objects.create(
            id='w_doomed', username='w_doomed', created_at=1,
        )
        p1 = Post.objects.create(
            id='w_p1', user=doomed, title='doomed post',
            content='bye', category='Science', created_at=10,
        )
        r1 = Reply.objects.create(
            id='w_r1', post=p1, user=doomed, content='r1', created_at=11,
        )
        Reply.objects.create(
            id='w_r2', post=p1, parent_reply=r1, user=other,
            content='r2', created_at=12,
        )
        PostLike.objects.create(post=p1, user=other)
        p2 = Post.objects.create(
            id='w_p2', user=other, title='other post',
            content='hi', category='Science', created_at=13,
            thumbs_up_count=1,
        )
        PostLike.objects.create(post=p2, user=doomed)
        r3 = Reply.objects.create(
            id='w_r3', post=p2, user=doomed, content='r3', created_at=14,
        )
        Reply.objects.create(
            id='w_r4', post=p2, parent_reply=r3, user=other,
            content='r4', created_at=15,
        )
        Reply.objects.create(
            id='w_r5', post=p2, user=other, content='r5',
            created_at=16, thumbs_up_count=1,
        )
        ReplyLike.objects.create(reply_id='w_r5', user=doomed)
        ReplyLike.objects.create(reply=r3, user=other)
        Follow.objects.create(follower=doomed, following=other, created_at=17)
        Follow.objects.create(follower=other, following=doomed, created_at=18)
        res1 = Resource.objects.create(
            id='w_res1', title='doomed resource', subject='Physics',
            grade_level='12', type='PDF', approval_status='approved',
            uploaded_by=doomed, like_count=1, comment_count=1, added_at=19,
        )
        ResourceLike.objects.create(resource=res1, user=doomed)
        c1 = ResourceComment.objects.create(
            id='w_c1', resource=res1, user=doomed,
            content='c1', created_at=20,
        )
        ResourceCommentLike.objects.create(comment=c1, user=other)
        ann1 = Announcement.objects.create(
            id='w_ann1', title='ann', slug='w-ann',
        )
        b1 = BlogComment.objects.create(
            id='w_b1', announcement=ann1, author=doomed,
            text='b1', created_at=21,
        )
        BlogComment.objects.create(
            id='w_b2', announcement=ann1, author=other,
            parent_comment=b1, text='b2', created_at=22,
        )
        BlogComment.objects.create(
            id='w_b3', announcement=ann1, author=other, text='b3',
            created_at=23, like_count=1, reply_count=1,
        )
        BlogComment.objects.create(
            id='w_b4', announcement=ann1, author=doomed,
            parent_comment_id='w_b3', text='b4', created_at=24,
        )
        BlogCommentLike.objects.create(comment_id='w_b3', user=doomed)
        Bookmark.objects.create(
            id='w_bm1', user=doomed, target_type='post',
            target_id='w_p2', created_at=25,
        )
        Notification.objects.create(
            id='w_n1', recipient=doomed, actor=other, verb='reply',
            target_type='post', target_id='w_p2',
            is_read=False, created_at=26,
        )
        Notification.objects.create(
            id='w_n2', recipient=other, actor=doomed, verb='like',
            target_type='post', target_id='w_p2',
            is_read=False, created_at=27,
        )
        FCMToken.objects.create(
            token='w_tok_doomed', user=doomed, created_at=28,
        )
        UserPhoto.objects.create(
            user=doomed, url='https://example.com/p.png', uploaded_at=29,
        )
        poll = Poll.objects.create(id='w_poll1', post=p2, created_at=30)
        opt = PollOption.objects.create(id='w_opt1', poll=poll, text='yes')
        PollVote.objects.create(
            id='w_vote1', poll=poll, option=opt, user=doomed, created_at=31,
        )
        EditHistory.objects.create(
            id='w_eh1', target_type='post', target_id='w_p2',
            field='content', edited_by=doomed, edited_at=32,
        )
        AccountDeletionRequest.objects.create(
            id='w_delreq1', user=doomed, created_at=33,
            scheduled_delete_at=34,
        )
        return {'doomed': doomed, 'other': other, 'p2': p2, 'res1': res1, 'ann1': ann1}

    def test_delete_user_account_removes_everything(self):
        admin = self._login_admin()
        world = self._build_full_world()
        doomed, other = world['doomed'], world['other']

        self.assertTrue(delete_user_account(doomed.id, completed_by=admin))

        self.assertFalse(User.objects.filter(pk=doomed.id).exists())
        for model, field in [
            (Post, 'user_id'), (Reply, 'user_id'),
            (PostLike, 'user_id'), (ReplyLike, 'user_id'),
            (ResourceLike, 'user_id'), (ResourceComment, 'user_id'),
            (ResourceCommentLike, 'user_id'), (BlogCommentLike, 'user_id'),
            (Bookmark, 'user_id'), (EditHistory, 'edited_by_id'),
            (UserPhoto, 'user_id'), (FCMToken, 'user_id'),
            (PollVote, 'user_id'),
        ]:
            self.assertFalse(
                model.objects.filter(**{field: doomed.id}).exists(),
                f'{model.__name__}.{field} still references deleted user',
            )
        self.assertFalse(BlogComment.objects.filter(author_id=doomed.id).exists())
        self.assertFalse(Follow.objects.filter(follower_id=doomed.id).exists())
        self.assertFalse(Follow.objects.filter(following_id=doomed.id).exists())
        self.assertFalse(Notification.objects.filter(recipient_id=doomed.id).exists())
        self.assertFalse(Notification.objects.filter(actor_id=doomed.id).exists())
        self.assertFalse(
            AccountDeletionRequest.objects.filter(user_id=doomed.id).exists()
        )

        res1 = Resource.objects.get(pk='w_res1')
        self.assertIsNone(res1.uploaded_by_id)
        self.assertEqual(res1.source_type, 'anonymous')
        self.assertEqual(res1.like_count, 0)
        self.assertEqual(res1.comment_count, 0)

        p2 = Post.objects.get(pk='w_p2')
        self.assertEqual(p2.thumbs_up_count, 0)
        r5 = Reply.objects.get(pk='w_r5')
        self.assertEqual(r5.thumbs_up_count, 0)
        b3 = BlogComment.objects.get(pk='w_b3')
        self.assertEqual(b3.like_count, 0)
        self.assertEqual(b3.reply_count, 0)

        other.refresh_from_db()
        self.assertEqual(other.follower_count, 0)
        self.assertEqual(other.following_count, 0)
        self.assertEqual(other.likes_received_count, 0)
        self.assertEqual(other.unread_notification_count, 0)

        self.assertTrue(Post.objects.filter(pk='w_p2').exists())
        self.assertTrue(Reply.objects.filter(pk='w_r5').exists())
        self.assertTrue(BlogComment.objects.filter(pk='w_b3').exists())
        self.assertTrue(Announcement.objects.filter(pk='w_ann1').exists())

    def test_deletions_process_page_completes_without_500(self):
        self._login_admin()
        doomed = User.objects.create(
            id='w_doomed2', username='w_doomed2', created_at=1,
        )
        Post.objects.create(
            id='w_p9', user=doomed, title='gone',
            content='gone', category='Science', created_at=2,
        )
        req = AccountDeletionRequest.objects.create(
            id='w_delreq9', user=doomed, created_at=3,
            scheduled_delete_at=4,
        )
        response = self.client.post(
            f'/admin/deletions/{req.id}/process/', {'action': 'delete'},
        )
        self.assertEqual(response.status_code, 302)
        self.assertFalse(User.objects.filter(pk=doomed.id).exists())
        self.assertFalse(Post.objects.filter(pk='w_p9').exists())
        self.assertFalse(
            AccountDeletionRequest.objects.filter(pk=req.id).exists()
        )

    def test_user_edit_page_delete_uses_full_cascade(self):
        self._login_admin()
        doomed = User.objects.create(
            id='w_doomed3', username='w_doomed3', created_at=1,
        )
        other = User.objects.create(
            id='w_other3', username='w_other3', created_at=1,
            follower_count=1,
        )
        Post.objects.create(
            id='w_p8', user=doomed, title='gone',
            content='gone', category='Science', created_at=2,
        )
        survivor = Post.objects.create(
            id='w_p7', user=other, title='stays',
            content='stays', category='Science', created_at=3,
            thumbs_up_count=1,
        )
        PostLike.objects.create(post=survivor, user=doomed)
        Follow.objects.create(follower=doomed, following=other, created_at=4)
        response = self.client.post(
            f'/admin/users/{doomed.id}/', {'_method': 'delete'},
        )
        self.assertEqual(response.status_code, 302)
        self.assertFalse(User.objects.filter(pk=doomed.id).exists())
        self.assertFalse(Post.objects.filter(pk='w_p8').exists())
        self.assertFalse(PostLike.objects.filter(user_id=doomed.id).exists())
        self.assertFalse(Follow.objects.filter(follower_id=doomed.id).exists())
        survivor.refresh_from_db()
        self.assertEqual(survivor.thumbs_up_count, 0)
        other.refresh_from_db()
        self.assertEqual(other.follower_count, 0)
