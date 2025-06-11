from rest_framework.viewsets import ModelViewSet

from ..models import Recipe
from ..serializer import RecipesSerializer


class RecipesAPiListViewSet(ModelViewSet):
    queryset = Recipe.objects.select_related(
        'author', 'category'
    ).prefetch_related(
        'tags'
    ).all()

    serializer_class = RecipesSerializer