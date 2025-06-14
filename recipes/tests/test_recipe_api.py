from rest_framework import test
from recipes.tests.test_recipe_base import RecipeMixin
from django.urls import reverse

class RecipeAPIv2Test(test.APITestCase, RecipeMixin):
    def get_recipe_list(self, string=None):
        
        if string is not None:
            api_url = reverse('recipes:recipes-api-list') + f'{string}'
        else:
            api_url = reverse('recipes:recipes-api-list')

        response = self.client.get(api_url)
        return response
    

    def test_recipe_api_list_returns_status_code_200(self):
        response = self.get_recipe_list(string='?page=1')
        self.assertEqual(
            response.status_code,
            200
        )

    def test_recipe_api_list_loads_correct_number_of_recipes(self):
        wanted_numbers_of_recipes = 3
        self.make_recipe_in_batch(qtd=wanted_numbers_of_recipes)

        response = self.get_recipe_list(string='?page=1')

        qtd_of_recipes_load = len(response.data.get('results'))

        self.assertEqual(
            wanted_numbers_of_recipes,
            qtd_of_recipes_load
        )

    def test_recipe_api_list_do_not_show_not_published_recipes(self):
        recipes = self.make_recipe_in_batch(qtd=2)

        recipe_not_published = recipes[0]
        recipe_not_published.is_published = False
        recipe_not_published.save()

        response = self.get_recipe_list(string='?page=1')
        
        self.assertEqual(
            len(response.data.get('results')),
            1
        )

    def test_recipe_api_list_can_load_recipes_by_category(self):
        category_wanted = self.make_category(name='Categoria Desejada')
        category_not_wanted = self.make_category(name='Outra Categoria')

        recipes = self.make_recipe_in_batch(qtd=2)

        recipe_wanted = recipes[0]
        recipe_wanted.title = 'Receita da categoria Certa'
        recipe_wanted.category = category_wanted
        recipe_wanted.save()

        recipe_not_wanted = recipes[1]
        recipe_not_wanted.title = 'Receita da categoria não Desejada'
        recipe_not_wanted.category = category_not_wanted
        recipe_not_wanted.save()

        response = self.get_recipe_list(string=f'?page=1&category_id={category_wanted.pk}')

        self.assertEqual(
            response.status_code,
            200
        )
        self.assertEqual(
            len(response.data.get('results')),
            1
        )
        self.assertEqual(
            response.data.get('results')[0]['title'],
            recipe_wanted.title
        )

        
