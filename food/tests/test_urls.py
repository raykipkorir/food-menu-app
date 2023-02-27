from django.test import SimpleTestCase
from django.urls import resolve, reverse

from food.views import (AllFoods, FoodAddView, FoodDetailView, FoodUpdateView, food_delete_view, 
                        searched_food)


class TestFoodUrls(SimpleTestCase):
    """Tests for food urls"""

    def test_all_foods_url(self) -> None:
        """Testing all foods url"""
        url: str = reverse("foods")
        self.assertEqual(resolve(url).func.view_class,  AllFoods)

    def test_food_add_url(self) -> None:
        """Testing food add url"""
        url: str = reverse("food_add")
        self.assertEqual(resolve(url).func.view_class, FoodAddView)

    def test_food_detail_url(self) -> None:
        """Testing food detail url"""
        url: str = reverse("food_detail", kwargs={"pk": 1})
        self.assertEqual(resolve(url).func.view_class, FoodDetailView)

    def test_food_update_url(self) -> None:
        """Testing food update url"""
        url: str = reverse("food_update", kwargs={"pk": 1})
        self.assertEqual(resolve(url).func.view_class, FoodUpdateView)

    def test_food_delete_url(self) -> None:
        """Testing food delete url"""
        url: str = reverse("food_delete", kwargs={"pk": 1})
        self.assertEqual(resolve(url).func, food_delete_view)
    
    def test_food_search_url(self) -> None:
        """Testing food search url"""
        url: str = reverse("search")
        self.assertEqual(resolve(url).func, searched_food)
