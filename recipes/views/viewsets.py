from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from ..models import Recipe
from ..serializer import RecipesSerializer

from ..permissions import IsOwnerOrReadOnly
from django.shortcuts import get_object_or_404

class RecipesApiV2ViewSet(ModelViewSet):

    queryset = Recipe.objects.select_related(
        'author', 'category'
        ).prefetch_related(
        'tags'
        ).all()

    serializer_class = RecipesSerializer
    permission_classes = [IsOwnerOrReadOnly, ]


    def get_queryset(self):
        qs = super().get_queryset()

        uri_category_id = self.request.query_params.get('category_id', '')

        if uri_category_id != '' and uri_category_id.isnumeric():
            qs = qs.filter(category_id=uri_category_id)
        return qs
    

    def get_object(self):
        pk = self.kwargs.get('pk', '')

        obj = get_object_or_404(
            self.get_queryset(),
            pk=pk
        )
        self.check_object_permissions(self.request, obj)
        return obj
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
        return super().perform_create(serializer)    
