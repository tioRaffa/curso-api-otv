from rest_framework.viewsets import ModelViewSet

from ..models import Recipe
from ..serializer import RecipesSerializer


class RecipesApiV2ViewSet(ModelViewSet):
    queryset = Recipe.objects.select_related(
        'author', 'category'
    ).prefetch_related(
        'tags'
    ).all()

    serializer_class = RecipesSerializer

    def get_queryset(self):
        qs = super().get_queryset()

        category_id = self.request.query_params.get('category_id', '')

        if category_id != '' and category_id.isnumeric():
            qs = qs.filter(category_id=category_id)

        return qs
    