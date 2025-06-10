from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from ..models import Recipe, Category, Tag
from ..serializer import RecipesSerializer, CategorySerializer, TagSerializer


class RecipesListView(APIView):
    def get(self, request):
        recipes = Recipe.objects.select_related(
            'category', 'author'
        ).prefetch_related(
            'tags'
        ).all().order_by('id')

        serializer = RecipesSerializer(instance=recipes, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = RecipesSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    

class RecipeDetailView(APIView):
    def get_recipe(self, pk):
        recipe = Recipe.objects.select_related(
            'category', 'author'
        ).prefetch_related(
            'tags'
        ).filter(
            pk=pk
        ).first()

        return recipe
    
    def get(self, request, pk):
        recipe = self.get_recipe(pk=pk)
        serializer = RecipesSerializer(instance=recipe)
        return Response(serializer.data)
    
    def patch(self, request, pk):
        recipe = self.get_recipe(pk=pk)
        serializer = RecipesSerializer(
            instance=recipe,
            data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
    def delete(self, request, pk):
        recipe = self.get_recipe(pk=pk)
        recipe.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

