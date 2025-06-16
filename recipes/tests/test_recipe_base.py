from django.test import TestCase
from recipes.models import Category, Recipe, User
from django.urls import reverse


class RecipeMixin:
    def make_category(self, name='Category'):
        return Category.objects.create(name=name)

    def make_author(
        self,
        first_name='user',
        last_name='name',
        username='username',
        password='123456',
        email='username@email.com',
    ):
        return User.objects.create_user(
            first_name=first_name,
            last_name=last_name,
            username=username,
            password=password,
            email=email,
        )

    def make_recipe(
        self,
        category_data=None,
        author_data=None,
        title='Recipe Title',
        description='Recipe Description',
        slug='recipe-slug',
        preparation_time=10,
        preparation_time_unit='Minutos',
        servings=5,
        servings_unit='Porções',
        preparation_steps='Recipe Preparation Steps',
        preparation_steps_is_html=False,
        is_published=True,
    ):
        if category_data is None:
            category_data = {}

        if author_data is None:
            author_data = {}

        return Recipe.objects.create(
            category=self.make_category(**category_data),
            author=self.make_author(**author_data),
            title=title,
            description=description,
            slug=slug,
            preparation_time=preparation_time,
            preparation_time_unit=preparation_time_unit,
            servings=servings,
            servings_unit=servings_unit,
            preparation_steps=preparation_steps,
            preparation_steps_is_html=preparation_steps_is_html,
            is_published=is_published,
        )

    def make_recipe_in_batch(self, qtd=10):
        recipes = []
        for i in range(qtd):
            kwargs = {
                'title': f'Recipe Title {i}',
                'slug': f'r{i}',
                'author_data': {'username': f'u{i}'}
            }
            recipe = self.make_recipe(**kwargs)
            recipes.append(recipe)
        return recipes


class RecipeTestBase(TestCase, RecipeMixin):
    def setUp(self) -> None:
        return super().setUp()


class RecipeAPIv2TestMixin(RecipeMixin):
    def create_simple_recipe(self):
        data = {
            'title': 'Minha Receita de Teste',
            'description': 'Uma descrição qualquer.',
            'preparation_time': 10,
            'preparation_time_unit': 'Minutos',
            'servings': 2,
            'servings_unit': 'Porções',
            'preparation_steps': 'Faça isso e aquilo.',
            }
        return data

    def get_recipe_api_url(self, url=None):
        if url is not None:
            url_api = reverse(f'{url}')
        else:
            url_api = reverse('recipes:recipes-api-list')
        return url_api        

    def get_recipe_list(self, string=None):
        
        if string is not None:
            api_url = reverse('recipes:recipes-api-list') + f'{string}'
        else:
            api_url = reverse('recipes:recipes-api-list')

        response = self.client.get(api_url)
        return response
    
    
    def get_jwt_token_author(self, username='Pintudinho'):
        user_data = {
            'username': username,
            'password': 'password'
        }
        user = self.make_author(
            username=user_data.get('username'),
            password=user_data.get('password')
        )
        url_api = reverse('recipes:token_obtain_pair')
        
        response = self.client.post(
            url_api, 
            data={**user_data}
        )
        data = {
            'jwt_token_access': response.data.get('access'),
            'jwt_token_refresh': response.data.get('refresh'),
            'user': user
        }
        
        return data