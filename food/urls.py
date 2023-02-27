from django.urls import path

from . import views

urlpatterns = [
    path("", views.AllFoods.as_view(), name="foods"),
    path("foods/", views.AllFoods.as_view(), name="foods"),
    path("new/", views.FoodAddView.as_view(), name="food_add"),
    path("foods/<int:pk>/", views.FoodDetailView.as_view(), name="food_detail"),
    path("foods/<int:pk>/edit/", views.FoodUpdateView.as_view(), name="food_update"),
    path("foods/<int:pk>/delete/", views.food_delete_view, name="food_delete"),

    path("search/", views.searched_food, name="search"),

    # ajax
    path("like-food/", views.like_food, name="like_food"),
]
