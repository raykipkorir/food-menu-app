import json

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)

from .forms import AddFoodForm
from .models import Category, Food, Like


class AllFoods(ListView):
    model = Food
    context_object_name = "foods"
    template_name = "food/all_foods.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        categories = Category.objects.all()
        context["categories"] = categories
        return context

    def get_queryset(self):
        if 'category' in self.request.GET:
            category = self.request.GET.get("category")
            foods = Food.objects.filter(category__name=category)
        elif 'tag' in self.request.GET:
            tag = self.request.GET.get("tag")
            foods = Food.objects.filter(tags__name=tag)
        else:
            foods = Food.objects.all()
        return foods


class FoodDetailView(DetailView):
    model = Food
    context_object_name = "food"
    template_name = "food/food_detail.html"


class FoodUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Food
    form_class = AddFoodForm
    template_name = "food/edit_food.html"

    def test_func(self):
        food = self.get_object()
        return self.request.user == food.user


class FoodAddView(LoginRequiredMixin, CreateView):
    form_class = AddFoodForm
    context_object_name = "form"
    template_name = "food/add_food.html"

    def form_valid(self, form):
        food = form.save(commit=False)
        food.user = self.request.user
        food.save()
        form.save_m2m()
        # return  super().form_valid(form)
        return redirect("food", pk=food.pk)

@login_required()
def food_delete_view(request, pk):
    food = Food.objects.get(id=pk)
    if request.user == food.user:
        food.delete()
        messages.success(request, message=f"{food.name} deleted successfully")
    else:
        return redirect("foods")
    return redirect("user_profile", username=food.user.username)


def searched_food(request):
    if "query" in request.GET:
        query = request.GET.get("query")
        foods = Food.objects.filter(name__icontains=query)
    else:
        foods = Food.objects.all() 
    return render(request, "food/all_foods.html", {"foods":foods})


# liking food functionality 
def like_food(request):
    data = request.body
    food_name = json.loads(data)["food_name"]
    food = Food.objects.get(name=food_name)
    try:
        like = Like.objects.get(user=request.user, food=food)
        style = {"like_status":"regular"}
        like.delete()
    except Like.DoesNotExist:
        Like.objects.create(user=request.user, food=food)
        style = {"like_status":"solid"}
    food_likes = Like.objects.filter(food=food).count()
    return JsonResponse({ "food_likes": food_likes, **style})

