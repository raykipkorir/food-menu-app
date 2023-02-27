from django.contrib.auth import views as auth_views
from django.test import SimpleTestCase
from django.urls import resolve, reverse

from users.views import delete_user, edit_profile, edit_user, profile, sign_up


class TestUserUrls(SimpleTestCase):
    """Test for user urls"""
    
    # signup, login and logout tests
    def test_signup_url(self) -> None:
        """Testing signup url"""
        url: str = reverse("sign_up")
        self.assertEqual(resolve(url).func, sign_up)
    
    def test_login_url(self) -> None:
        """ Testing login url """
        url: str = reverse("login")
        self.assertEqual(resolve(url).func.view_class, auth_views.LoginView)
    
    def test_logout_url(self) -> None:
        """Testing logout url"""
        url: str = reverse("logout")
        self.assertEqual(resolve(url).func.view_class, auth_views.LogoutView)
    

    # password change test
    def test_password_change_url(self) -> None:
        """Test password change url"""
        url: str = reverse("password_change")
        self.assertEqual(resolve(url).func.view_class, auth_views.PasswordChangeView)
    
    # password reset tests
    def test_password_reset_url(self) -> None:
        """Test password reset url"""
        url: str = reverse("password_reset")
        self.assertEqual(resolve(url).func.view_class, auth_views.PasswordResetView)

    def test_password_reset_done_url(self) -> None:
        """Test password reset done url"""
        url: str = reverse("password_reset_done")
        self.assertEqual(resolve(url).func.view_class, auth_views.PasswordResetDoneView)

    def test_password_reset_confirm_url(self) -> None:
        """Test password reset confirm url"""
        url: str = reverse("password_reset_confirm", args=['uidb', 'test_token'])
        self.assertEqual(resolve(url).func.view_class, auth_views.PasswordResetConfirmView)

    def test_password_reset_confirm_done_url(self) -> None:
        """Test password reset confirm done url"""
        url: str = reverse("password_reset_complete")
        self.assertEqual(resolve(url).func.view_class, auth_views.PasswordResetCompleteView)

    # user profile tests
    def test_edit_profile_url(self) -> None:
        """Test edit profile url"""
        url: str = reverse("edit_profile")
        self.assertEqual(resolve(url).func, edit_profile)
    
    def test_user_profile_url(self) -> None:
        """Test user profile url"""
        url: str = reverse("user_profile", kwargs={"username": "ray"})
        self.assertEqual(resolve(url).func, profile)

    # edit and delete user tests
    def test_edit_user_url(self) -> None:
        """Test edit user url"""
        url: str = reverse("edit_user")
        self.assertEqual(resolve(url).func, edit_user)

    def test_delete_user_url(self) -> None:
        """Test delete user url"""
        url: str = reverse("delete_user")
        self.assertEqual(resolve(url).func, delete_user)
