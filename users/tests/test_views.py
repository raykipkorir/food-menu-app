from typing import Dict

from django.contrib.auth import get_user_model
from django.contrib.auth import views as auth_views
from django.test import Client, TestCase
from django.urls import reverse

from users.models import UserProfile

User = get_user_model()

# signup and password change tests

class TestUserViews(TestCase):

    def setUp(self) -> None:
        self.client = Client()
        self.user: User = User.objects.create_user(
            username="ray",
            email="ray@email.com",
            password="testing321"
        )
        self.client.login(username="ray", password="testing321")

    # signup tests
    def test_signup_view_GET(self) -> None:
        self.client.logout()
        response = self.client.get(reverse("sign_up"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "users/sign_up.html")

    # def test_signup_view_POST(self) -> None:
    #     self.client.logout()
    #     data: Dict[str] = {
    #         "username": "John Doe",
    #         "email": "johndoe@gmail.com", 
    #         "password1": "testing321", 
    #         "password2": "testing321"
    #     }
    #     response = self.client.post(reverse("sign_up"), data=data, content_type="application/json")
    #     self.assertRedirects(response, reverse("foods"))

    # profile tests
    def test_profile_view(self) -> None:
        response = self.client.get(reverse("user_profile", kwargs={"username": self.user.username}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "users/user_profile.html")

    def test_edit_profile_view_GET(self) -> None:
        response = self.client.get(reverse("edit_profile"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "users/edit_profile.html")

    def test_edit_profile_view_POST(self) -> None:
        response = self.client.post(
            reverse("edit_profile"), 
            self.user.userprofile, 
            content_type="application/json"
            )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("user_profile", kwargs={"username": self.user.username}))

    # delete user tests
    def test_delete_user_view_GET(self) -> None:
        response = self.client.get(reverse("delete_user"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "users/delete_user.html")

    def test_delete_user_view_POST(self) -> None:
        response = self.client.post(reverse("delete_user"))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("foods"))

    # login and logout tests
    def test_login_view(self) -> None:
        response = self.client.get(reverse("login"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "users/login.html")
    
    def test_logout_view(self) -> None:
        response = self.client.get(reverse("logout"))
        self.assertEqual(response.status_code, 302)

    # password change tests
    def test_password_change_view_GET(self) -> None:
        response = self.client.get(reverse("password_change"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "users/password_change.html")

    # def test_password_change_view_POST(self) -> None:
    #     data: Dict[str]= {
    #         "old_password": "testing321", 
    #         "new_password1": "testing321", 
    #         "new_password2": "testing321"
    #     }
    #     response = self.client.post(
    #         reverse("password_change"), 
    #         data=data,
    #         content_type="application/json",
    #         # follow=True
    #         )
    #     self.assertRedirects(response, reverse("foods"))

    # password reset tests
    def test_password_reset_view_GET(self) -> None:
        response = self.client.get(reverse("password_reset"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "users/password_reset.html")

    # def test_password_reset_view_POST(self) -> None:
    #     data = {"email": self.user.email}
    #     user = User.objects.get(username="ray")
    #     response = self.client.post(reverse("password_reset"), data=user.email, content_type="application/json")
    #     self.assertRedirects(response, reverse("password_reset_done"))

    def test_password_reset_done_view(self) -> None:
        response = self.client.get(reverse("password_reset_done"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "users/password_reset_done.html")

    # def test_password_reset_confirm_view_GET(self) -> None:
    #     response = self.client.get(reverse("password_reset_confirm"))
    #     self.assertEqual(response.status_code, 200)
    #     self.assertTemplateUsed(response, "users/setpassword.html")

    # def test_password_reset_confirm_view_POST(self) -> None:
    #     data = {}
    #     response = self.client.post(reverse("password_reset_confirm"), data=data, content_type="application/json")
    #     self.assertRedirects(response, reverse("password_reset_complete"))

    def test_password_reset_complete_view(self) -> None:
        response = self.client.get(reverse("password_reset_complete"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "users/setpassword_done.html")



