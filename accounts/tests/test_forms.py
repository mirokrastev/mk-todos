from django.test import TestCase
from accounts.forms import CustomUserCreationForm, CustomPasswordResetForm
from accounts.models import CustomUser, UserProfile


class UserCreationFormTests(TestCase):
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
        This metod is testing various outcomes. Like an error for a short name, too long name and etc..
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

        form = CustomPasswordResetForm(long_username)
        self.assertFalse(form.is_valid())

    def test_user_creation_if_it_has_userprofile(self):
        """
        This method is testing if creating an user with UserCreationForm.save() is creating a UserProfile model.
        It is somewhat a redundant test, but you never know what can break :)
        """
        data = {
            'username': 'testuser',
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
    pass
