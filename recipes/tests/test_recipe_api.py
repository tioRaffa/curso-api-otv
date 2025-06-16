from rest_framework import test
from recipes.tests.test_recipe_base import RecipeAPIv2TestMixin
from django.urls import reverse


class RecipeAPIv2Test(test.APITestCase, RecipeAPIv2TestMixin):

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

    
    def test_recipe_api_list_user_must_send_jwt_token_to_create_recipe(self):
        api_url = self.get_recipe_api_url()
        recipe_data = self.create_simple_recipe()
        
        response = self.client.post(api_url, data=recipe_data)

        self.assertEqual(
            response.status_code,
            401
        )

    def test_recipe_api_does_not_accept_negative_numbers(self):
        recipe_data = self.create_simple_recipe()
        recipe_data['preparation_time'] = -10
       
        token = self.get_jwt_token_author()
        access = token['jwt_token_access']
        response = self.client.post(
            self.get_recipe_api_url(),
            data=recipe_data,
            HTTP_AUTHORIZATION=f'Bearer {access}'
        )
        self.assertEqual(
            response.status_code,
            400
        )
        self.assertEqual(
            response.data.get('preparation_time')[0],
            'preparation_time deve ser um número positivo.'
        )

    def test_recipe_api_list_logged_user_can_create_a_recipe(self):
        recipe_data = self.create_simple_recipe()
        token = self.get_jwt_token_author()
        access = token['jwt_token_access']

        response = self.client.post(
            self.get_recipe_api_url(),
            data=recipe_data,
            HTTP_AUTHORIZATION=f'Bearer {access}'
        )
        self.assertEqual(
            response.status_code,
            201
        )

    def test_recipe_api_list_logged_user_can_update_a_recipe(self):
        recipe = self.make_recipe()

        jwt_data = self.get_jwt_token_author()
        token_access = jwt_data.get('jwt_token_access')

        author = jwt_data.get('user')
        recipe.author = author
        recipe.save()
        url_api = reverse('recipes:recipes-api-detail', args=(recipe.id,))

        modified_title = f'Modificação feita pelo user: {author.username}'


        response = self.client.patch(
            url_api,
            HTTP_AUTHORIZATION=f'Bearer {token_access}',
            data={
                'title': modified_title
            },
        )


        self.assertEqual(
            response.data.get('title'),
            modified_title
        )
        self.assertEqual(
            response.data['author']['id'],
            author.id
        )
        self.assertEqual(
            response.status_code,
            200
        )