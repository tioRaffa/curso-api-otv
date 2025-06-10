from django.urls import path

from recipes import views

app_name = 'recipes'

urlpatterns = [
    path(
        '',
        views.RecipeListViewHome.as_view(),
        name="home"
    ),
    path(
        'recipes/search/',
        views.RecipeListViewSearch.as_view(),
        name="search"
    ),
    path(
        'recipes/tags/<slug:slug>/',
        views.RecipeListViewTag.as_view(),
        name="tag"
    ),
    path(
        'recipes/category/<int:category_id>/',
        views.RecipeListViewCategory.as_view(),
        name="category"
    ),
    path(
        'recipes/<int:pk>/',
        views.RecipeDetail.as_view(),
        name="recipe"
    ),
    path(
        'recipes/api/v1/',
        views.RecipeListViewHomeApi.as_view(),
        name="recipes_api_v1",
    ),
    path(
        'recipes/api/v1/<int:pk>/',
        views.RecipeDetailAPI.as_view(),
        name="recipes_api_v1_detail",
    ),
    path(
        'recipes/theory/',
        views.theory,
        name='theory',
    ),
    path(
        "api/v2/recipes",
        views.RecipesListView.as_view(),
        name="recipes-list-api-v2"
    ),
    path(
        "api/v2/recipes/<int:pk>/",
        views.RecipeDetailView.as_view(),
        name="recipe-detail-api-v2",
    ),
    path(
        "api/v2/categories/",
        views.category_api_list,
        name="category-list-api-v2"
    ),
    
    
]
