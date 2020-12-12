from django.test import TestCase, Client
from accounts.forms import CustomUserCreationForm, CustomPasswordResetForm, CustomSetPasswordForm
from accounts.models import CustomUser, UserProfile


class UserCreationFormTests(TestCase):
    def tearDown(self):
        CustomUser.objects.all().delete()

    def test_valid_form_and_create_user(self):
        """
        This method is testing if UserCreationForm validates the data. It should not raise any exceptions.
        Also it should create a user of type CustomUser.
        """
        data = {
            'username': 'testuser',
            'password1': 'reallystrongpassword123',
            'password2': 'reallystrongpassword123',
            'email': 'testemail@gmail.com',
        }
        form = CustomUserCreationForm(data)
        self.assertTrue(form.is_valid())
        user = form.save()
        self.assertTrue(isinstance(user, CustomUser))

    def test_invalid_form_email_error(self):
        """
        This method is testing if UserCreationForm returns an error for email field. It is required by design.
        """
        data = {
            'username': 'testuser',
            'password1': 'reallystrongpassword123',
            'password2': 'reallystrongpassword123',
        }
        form = CustomUserCreationForm(data)
        self.assertFalse(form.is_valid())

    def test_password_mismatch(self):
        """
        This method is testing if UserCreationForm is returning an error for password mismatch
        """
        data = {
            'username': 'testuser',
            'password1': 'reallystrongpassword123',
            'password2': 'reallystrongpassword1234',
            'email': 'testemail@gmail.com',
        }
        form = CustomUserCreationForm(data)
        self.assertFalse(form.is_valid())

    def test_various_outcomes(self):
        """
        This method is testing various outcomes. Like an error for a short name, too long name and etc..
        """
        short_username = {
            'username': 'q',
            'password1': 'reallystrongpassword123',
            'password2': 'reallystrongpassword123',
            'email': 'testemail@gmail.com',
        }

        form = CustomUserCreationForm(short_username)
        self.assertFalse(form.is_valid())

        long_username = short_username.copy()
        long_username['username'] = 'test' * 50

        form = CustomUserCreationForm(long_username)
        self.assertFalse(form.is_valid())

    def test_user_creation_if_it_has_userprofile(self):
        """
        This method is testing if creating an user with UserCreationForm.save() is creating a UserProfile model.
        """
        data = {
            'username': 'testuser5',
            'password1': 'reallystrongpassword123',
            'password2': 'reallystrongpassword123',
            'email': 'testemail@gmail.com',
        }
        form = CustomUserCreationForm(data)
        user = form.save()
        userprofile = UserProfile.objects.get(user=user)
        self.assertTrue(userprofile)


class PasswordResetFormTests(TestCase):
    def test_valid_form(self):
        """
        This method is testing if PasswordResetForm is returning True for valid email.
        """
        data = {
            'email': 'testemail@gmail.com'
        }
        form = CustomPasswordResetForm(data)
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        """
        This method is testing if PasswordResetForm is returning False for invalid email
        """
        data = {
            'email': 'incorrect@gm.'
        }
        form = CustomPasswordResetForm(data)
        self.assertFalse(form.is_valid())


class SetPasswordFormTests(TestCase):
    @classmethod
    def setUpClass(cls):
        data = {
            'username': 'testuser',
            'password1': 'reallystrongpassword123',
            'password2': 'reallystrongpassword123',
            'email': 'testemail@gmail.com',
        }
        cls.user = CustomUserCreationForm(data).save()
        cls.client = Client()

    @classmethod
    def tearDownClass(cls):
        CustomUser.objects.all().delete()

    def test_valid_password_change(self):
        """
        This method is testing if SetPasswordForm is working as expected with correct data.
        """
        data = {
            'new_password1': 'qwerasd123',
            'new_password2': 'qwerasd123',
        }
        form = CustomSetPasswordForm(self.user, data)
        self.assertTrue(form.is_valid())
        credentials = {'username': self.user.username, 'password': 'reallystrongpassword123'}
        self.client.login(**credentials)
        self.client.logout()
        form.save()
        self.client.login(username=credentials['username'], password='qwerasd123')

    def test_invalid_password_change(self):
        """
        This method is testing if SetPasswordForm is returning False for incorrect data.
        """
        data = {
            'new_password1': 'qwerasd123',
            'new_password2': 'qwerasd1234',
        }
        form = CustomSetPasswordForm(self.user, data)
        self.assertFalse(form.is_valid())
