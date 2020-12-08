from django.test import TestCase
from accounts.models import CustomUser, UserProfile


class CustomUserBasicTests(TestCase):
    def tearDown(self) -> None:
        CustomUser.objects.all().delete()

    def test_basic_user_creation(self):
        """
        This method is testing a basic user creation.
        The credentials are hardcoded, and for this reason it's a basic test.
        """
        credentials = {
            'username': 'testusernew',
            'password': 'testpass'
        }
        CustomUser.objects.create(**credentials)
        user_obj = CustomUser.objects.get(username=credentials['username'])
        self.assertTrue(user_obj.username, 'testusernew')

    def test_customuser_should_raise_exception(self):
        """
        This method is testing if CustomUser will raise an error if no match is found.
        It should raise a DoesNotExist exception.
        """
        with self.assertRaises(CustomUser.DoesNotExist):
            user_obj = CustomUser.objects.get(username='notfound', password='testpassword')

    def test_creating_user_should_create_userprofile(self):
        """
        This method is testing if creating an user from CustomUser is creating a UserProfile.
        It should be created because it's using a signal.
        """
        credentials = {
            'username': 'testusernew',
            'password': 'testpass'
        }
        CustomUser.objects.create(**credentials)
        user_obj = CustomUser.objects.get(username=credentials['username'])
        userprofile_obj = UserProfile.objects.get(user=user_obj)


class UserProfileBasicTests(TestCase):
    @classmethod
    def setUpClass(cls):
        """
        setUp method to create a userprofile instance.
        """
        super().setUpClass()

        credentials = {
            'username': 'testuser',
            'password': 'password',
        }
        CustomUser.objects.create_user(**credentials)
        user_obj = CustomUser.objects.get(username=credentials['username'])
        cls.userprofile = UserProfile.objects.get(user=user_obj)

    def tearDown(self):
        """
        tearDown method to revert the UserProfile instance to default.
        """
        self.userprofile.bio = None
        self.userprofile.dark_mode = False

    def test_userprofile_fields(self):
        """
        This method is testing if UserProfile has avatar, bio and dark_mode fields
        """
        self.assertEqual(self.userprofile.avatar.url, '/media/images/default-user-avatar.jpg')
        self.assertIsNone(self.userprofile.bio)
        self.assertFalse(self.userprofile.dark_mode)

    def test_manipulating_userprofile_fields(self):
        """
        This method is testing if it's possible to change UserProfile fields.
        """
        self.userprofile.bio = 'Hello!'
        self.userprofile.dark_mode = True

        self.assertEqual(self.userprofile.bio, 'Hello!')
        self.assertTrue(self.userprofile.dark_mode)
