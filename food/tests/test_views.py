from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from food.models import Food

User = get_user_model()


class TestFoodViews(TestCase):

    def setUp(self) -> None:
        self.client = Client()
        self.user: User = User.objects.create_user(
            username="ray",
            email="ray@email.com",
            password="testing321"
        )
        self.food: Food = Food.objects.create(
            name="TestFood",
            price="200",
            user=self.user
        )
        # self.data = Food(name="TestFood2", price=200, user=self.user)
        
        self.client.login(username="ray", password="testing321")
    
    def test_all_foods_view(self) -> None:
        response = self.client.get(reverse("foods"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "food/all_foods.html")

    def test_food_detail_view(self) -> None:
        response = self.client.get(reverse("food_detail", kwargs={"pk": self.food.id}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "food/food_detail.html")

    def test_food_add_view_GET(self) -> None:
        response = self.client.get(reverse("food_add"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "food/add_food.html")
    

    # def test_food_add_view_POST(self) -> None:
    #     print(type(self.data))
    #     # data = {"name": "TestFood2", "price": 200, "user": self.user}
    #     response = self.client.post(reverse("food_add"), self.data, content_type="application/json")
    #     food = Food.objects.get(name__iexact="TestFood2")
    #     # self.assertEqual(response.status_code, 200)
    #     self.assertRedirects(response, reverse("food_detail", kwargs={"pk": food.id}))

    # def test_food_update_view_GET(self) -> None:
    #     response = self.client.get(reverse("food_update", kwargs={"pk":self.food.id}))
    #     self.assertEqual(response.status_code, 200)
    #     self.assertTemplateUsed("food/edit_food.html")

    # def test_food_update_view_POST(self) -> None:
    #     response = self.client.post(reverse("food_update", kwargs={"pk": self.food.id}), data=self.food, content_type="application/json")
    #     self.assertRedirects(response, reverse("food_update", kwargs={"pk": self.food.id}))
