from rest_framework.test import APIClient
from django.core.files.uploadedfile import SimpleUploadedFile
from testing.testcases import TestCase
from accounts.models import UserProfile

LOGIN_URL = '/api/accounts/login/'
LOGOUT_URL = '/api/accounts/logout/'
SIGNUP_URL = '/api/accounts/signup/'
LOGIN_STATUS_URL = '/api/accounts/login_status/'
USER_PROFILE_DETAIL_URL = '/api/profiles/{}/'

class AccountApiTests(TestCase):

    def setUp(self):
        super(AccountApiTests, self).setUp()
        # this function is executed when the 'test function' command is triggered
        self.client = APIClient()
        self.user = self.create_user(
            username='admin',
            email='test@test.com',
            password='correct password',
        )

    def test_login(self):
        # test1: method is supposed to be POST
        response = self.client.get(LOGIN_URL, {
            'username': self.user.username,
            'password': 'correct password',
        })
        # login failure: return status code 405 = METHOD_NOT_ALLOWED
        self.assertEqual(response.status_code, 405)

        # test2: password wrong
        response = self.client.post(LOGIN_URL, {
            'username': self.user.username,
            'password': 'wrong password',
        })
        self.assertEqual(response.status_code, 400)

        # test3: correct password
        # verify no user is logged in
        response = self.client.get(LOGIN_STATUS_URL)
        self.assertEqual(response.data['has_logged_in'], False)
        # verify logging in with correct password
        response = self.client.post(LOGIN_URL, {
            'username': self.user.username,
            'password': 'correct password',
        })
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(response.data['user'], None)
        self.assertEqual(response.data['user']['id'], self.user.id)
        # verify login status after logged in
        response = self.client.get(LOGIN_STATUS_URL)
        self.assertEqual(response.data['has_logged_in'], True)

    def test_logout(self):
        # login before testing
        self.client.post(LOGIN_URL, {
            'username': self.user.username,
            'password': 'correct password',
        })
        # verify the user is successfully logged in
        response = self.client.get(LOGIN_STATUS_URL)
        self.assertEqual(response.data['has_logged_in'], True)

        # test1: method is supposed to be post
        response = self.client.get(LOGOUT_URL)
        self.assertEqual(response.status_code, 405)

        # test2: change method to post request
        response = self.client.post(LOGOUT_URL)
        self.assertEqual(response.status_code, 200)
        # verify the user has logged out successfully
        response = self.client.get(LOGIN_STATUS_URL)
        self.assertEqual(response.data['has_logged_in'], False)

    def test_signup(self):
        data = {
            'username': 'someone',
            'email': 'someone@test.com',
            'password': 'any password',
        }
        # test1: method is supposed to be post
        response = self.client.get(SIGNUP_URL, data)
        self.assertEqual(response.status_code, 405)

        # test2: incorrect email
        response = self.client.post(SIGNUP_URL, {
            'username': 'someone',
            'email': 'incorrect email',
            'password': 'any password',
        })
        self.assertEqual(response.status_code, 400)

        # test3: password too short
        response = self.client.post(SIGNUP_URL, {
            'username': 'someone',
            'email': 'someone@test.com',
            'password': '123',
        })
        self.assertEqual(response.status_code, 400)

        # test4: username too long
        response = self.client.post(SIGNUP_URL, {
            'username': 'username is tooooooooooooooooo loooooooong',
            'email': 'someone@test.com',
            'password': 'any password',
        })
        self.assertEqual(response.status_code, 400)

        # test5: successful registration
        response = self.client.post(SIGNUP_URL, data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['user']['username'], 'someone')
        #test if the userprofile has been created
        created_user_id = response.data['user']['id']
        profile = UserProfile.objects.filter(user_id=created_user_id).first()
        self.assertNotEqual(profile, None)
        # verify the newly registered user has logged in
        response = self.client.get(LOGIN_STATUS_URL)
        self.assertEqual(response.data['has_logged_in'], True)

class UserProfileAPITests(TestCase):

    def test_update(self):
        linghu, linghu_client = self.create_user_and_client('linghu')
        p = linghu.profile
        p.nickname = 'old nickname'
        p.save()
        url = USER_PROFILE_DETAIL_URL.format(p.id)

        # test can only be updated by user himself.
        _, dongxie_client = self.create_user_and_client('dongxie')
        response = dongxie_client.put(url, {
            'nickname': 'a new nickname',
        })
        self.assertEqual(response.status_code, 403)
        p.refresh_from_db()
        self.assertEqual(p.nickname, 'old nickname')

        # update nickname
        response = linghu_client.put(url, {
            'nickname': 'a new nickname',
        })
        self.assertEqual(response.status_code, 200)
        p.refresh_from_db()
        self.assertEqual(p.nickname, 'a new nickname')

        # update avatar
        response = linghu_client.put(url, {
            'avatar': SimpleUploadedFile(
                name='my-avatar.jpg',
                content=str.encode('a fake image'),
                content_type='image/jpeg',
            ),
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual('my-avatar' in response.data['avatar'], True)
        p.refresh_from_db()
        self.assertIsNotNone(p.avatar)