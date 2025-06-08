from rest_framework.decorators import api_view
from rest_framework.response import Response

from ..models import Recipe
from ..serializer import RecipesSerializer


@api_view(http_method_names=['get', 'post'])
def recipe_api_list(request):

    recipe = Recipe.objects.select_related(
        'category', 'author'
    ).prefetch_related(
        'tags'
    ).all().order_by('id')


    serializer = RecipesSerializer(instance=recipe, many=True)

    return Response(serializer.data)


@api_view(http_method_names=['get'])
def recipe_api_detail(request, pk):

    recipe = Recipe.objects.select_related(
        'category', 'author'
    ).prefetch_related(
        'tags'
    ).filter(
        pk=pk
    ).first()

    serializer = RecipesSerializer(instance=recipe)
    return Response(serializer.data)