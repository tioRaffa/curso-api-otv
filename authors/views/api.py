from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action

from ..serializer import AuthorSerializer
from django.contrib.auth import get_user_model

class AuthorApiViewSet(ReadOnlyModelViewSet):
    serializer_class = AuthorSerializer
    permission_classes = [IsAuthenticated, ]

    def get_queryset(self):
        user = get_user_model()
        queryset = user.objects.filter(
            username=self.request.user.username
        )
        
        return queryset
    
    @action(
            methods=['get'],
            detail=False #              TRUE -> Quando for |PrimaryKey|
    )
    def me(self, request, *args, **kwargs):
        user = self.get_queryset().first()
        
        serializer = self.get_serializer(
            instance=user
        )
        return Response(serializer.data)

