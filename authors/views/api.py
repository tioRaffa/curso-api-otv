from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.permissions import IsAuthenticated

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