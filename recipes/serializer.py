from rest_framework import serializers
from .models import Recipe, Tag, Category
from django.contrib.auth.models import User



class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name', 'slug']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        extra_kwargs = {
            'email': {
                'write_only': True
            }
        }
        fields = ['id', 'first_name', 'last_name', 'username', 'email']



class RecipesSerializer(serializers.ModelSerializer):

    tags = TagSerializer(read_only=True, many=True)
    author = AuthorSerializer(read_only=True)
    category = CategorySerializer(read_only=True)

    class Meta:
        extra_kwargs = {
            'is_published':{
                'read_only': True
            },
            'preparation_steps_is_html': {
                'read_only': True
            },
        }
        model = Recipe
        fields = [
            'id',
            'title',
            'description',
            'is_published',
            'preparation_time',
            'preparation_time_unit',
            'servings',
            'servings_unit',
            'preparation_steps',
            'cover',
            'category', 
            'author',   
            'tags',     
        ]
    
    def validate(self, attrs):
        if self.instance is not None and attrs.get('servings') is None:
            attrs['servings'] = self.instance.servings
        
        if self.instance is not None and attrs.get('preparation_time') is None:
            attrs['preparation_time'] = self.instance.preparation_time

        return super().validate(attrs)
