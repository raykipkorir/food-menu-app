from django.urls import path, reverse_lazy
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    #authentication
    path("signup/", views.sign_up, name="sign_up"),

    path("login/", auth_views.LoginView.as_view(template_name="users/login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(template_name="users/logout.html"), name="logout"),

    path(
        "password_change/",
        auth_views.PasswordChangeView.as_view(
            template_name="users/password_change.html",
            success_url=reverse_lazy("foods"),
        ),
        name="password_change",
    ),

    path(
        "password_reset/", 
        auth_views.PasswordResetView.as_view(
            template_name="users/password_reset.html",
            email_template_name="users/password_reset_email.html",
            from_email="raykipkorir02@gmail.com"
            ), 
        name="password_reset"
    ),
    path(
        "password_reset/done/",
        auth_views.PasswordResetDoneView.as_view(template_name="users/password_reset_done.html"),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(template_name="users/setpassword.html"),
        name="password_reset_confirm",
    ),
    path(
        "reset/done/",
        auth_views.PasswordResetCompleteView.as_view(template_name="users/setpassword_done.html"),
        name="password_reset_complete",
    ),
    
    #user profile
    path("edit-profile/", views.edit_profile, name="edit_profile"),
    path("user/<str:username>/", views.profile, name="user_profile"),

    #user
    path("edit-user/", views.edit_user, name="edit_user"),
    path("delete-user/", views.delete_user, name="delete_user"),
    
]
