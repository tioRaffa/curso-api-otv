from rest_framework.routers import SimpleRouter
from django.urls import path
from recipes import views

from rest_framework_simplejwt.views import TokenVerifyView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


app_name = 'recipes'

router = SimpleRouter()
router.register('recipes', views.RecipesApiV2ViewSet)

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
    
    # JWT
    path(
        'recipes/api/token/', 
         TokenObtainPairView.as_view(), 
         name='token_obtain_pair'
    ),
    path(
        'recipes/api/token/refresh/', 
         TokenRefreshView.as_view(), 
         name='token_refresh'
    ),
    path(
        'recipes/api/token/verify/', 
        TokenVerifyView.as_view(), 
        name='token_verify'
    ),
]

# ROUTER ViewSet API
urlpatterns += router.urls