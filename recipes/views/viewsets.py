from rest_framework.viewsets import ModelViewSet

from ..models import Recipe
from ..serializer import RecipesSerializer

from ..permissions import IsOwnerOrReadOnly


class RecipesApiV2ViewSet(ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipesSerializer
    permission_classes = [IsOwnerOrReadOnly, ]


    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.select_related('author', 'category').prefetch_related('tags')
        qs = qs.filter(is_published=True)

        uri_category_id = self.request.query_params.get('category_id', '')

        if uri_category_id != '' and uri_category_id.isnumeric():
            qs = qs.filter(category_id=uri_category_id)

        qs = qs.order_by('-id')
        return qs

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)  
