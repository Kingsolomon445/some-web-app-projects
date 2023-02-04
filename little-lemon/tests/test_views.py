from django.test import TestCase
from restaurant.models import Menu
from restaurant.serializers import MenuSerializer
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token



class MenuViewTest(TestCase):
    def setUp(self):
        # create some test objects
        Menu.objects.create(name='Breakfast', price=20, description='A delicious breakfast')
        Menu.objects.create(name='Lunch', price=30, description='A delicious lunch')
        Menu.objects.create(name='Dinner', price=40, description='A delicious dinner')


    def test_getall(self):
        menus = Menu.objects.all()

        # Create a user and obtain an auth token
        user = User.objects.create_user(username='testuser1', password='testpass1')
        token = Token.objects.create(user=user)
        auth_header = f'Token {token.key}'

        # Make a GET request to the view with the auth header
        response = self.client.get('/api/menu/', HTTP_AUTHORIZATION=auth_header)

        # Check that the response has a status code of 200
        self.assertEqual(response.status_code, 200)

        # Deserialize the response data
        menu_items = MenuSerializer(menus, many=True).data

        # Check that the deserialized response data is correct
        self.assertEqual(response.data, menu_items)

