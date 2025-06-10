from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework import status

from ..models import Recipe, Category, Tag
from ..serializer import RecipesSerializer, CategorySerializer, TagSerializer


class RecipesListView(ListCreateAPIView):
    queryset = Recipe.objects.select_related(
        'category', 'author').prefetch_related(
        'tags').all().order_by('id')
    serializer_class = RecipesSerializer
    

class RecipeDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Recipe.objects.select_related(
        'category', 'author'
    ).prefetch_related('tags').all()
    
    serializer_class = RecipesSerializer

