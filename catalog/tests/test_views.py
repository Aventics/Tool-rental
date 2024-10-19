

from django.test import TestCase
from catalog.models import Brand
from django.urls import reverse

class BrandsListViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        #Create 13 brands for pagination tests
        number_of_brands = 13
        for brand_num in range(number_of_brands):
            Brand.objects.create(brand_name='Some_brand %s' % brand_num)

    def test_view_url_exists_at_desired_location(self):
        resp = self.client.get('/catalog/brands/')
        self.assertEqual(resp.status_code, 200)

    def test_view_url_accessible_by_name(self):
        resp = self.client.get(reverse('brands'))
        self.assertEqual(resp.status_code, 200)

    def test_view_uses_correct_template(self):
        resp = self.client.get(reverse('brands'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'brands/brands_list.html')

    def test_pagination_is_ten(self):
        resp = self.client.get(reverse('brands'))
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('is_paginated' in resp.context)
        self.assertTrue(resp.context['is_paginated'] == True)
        self.assertTrue(len(resp.context['brands_list']) == 10)

    def test_lists_all_brands(self):
        #Get second page and confirm it has (exactly) remaining 3 items
        resp = self.client.get(reverse('brands')+'?page=2')
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('is_paginated' in resp.context)
        self.assertTrue(resp.context['is_paginated'] == True)
        self.assertTrue( len(resp.context['brands_list']) == 3)


class ToolsListViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        #Create 13 tools for pagination tests
        number_of_tools = 13
        for tool_num in range(number_of_tools):
            Tool.objects.create(type_tool='Some_type %s' % tool_num)

    def test_view_url_exists_at_desired_location(self):
        resp = self.client.get('/catalog/tools/')
        self.assertEqual(resp.status_code, 200)

    def test_view_url_accessible_by_name(self):
        resp = self.client.get(reverse('tools'))
        self.assertEqual(resp.status_code, 200)

    def test_view_uses_correct_template(self):
        resp = self.client.get(reverse('tools'))
        self.assertEqual(resp.status_code, 200)

        self.assertTemplateUsed(resp, 'tools/tools_list.html')

    def test_pagination_is_ten(self):
        resp = self.client.get(reverse('tools'))
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('is_paginated' in resp.context)
        self.assertTrue(resp.context['is_paginated'] == True)
        self.assertTrue(len(resp.context['tools_list']) == 10)

    def test_lists_all_tools(self):
        #Get second page and confirm it has (exactly) remaining 3 items
        resp = self.client.get(reverse('tools')+'?page=2')
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('is_paginated' in resp.context)
        self.assertTrue(resp.context['is_paginated'] == True)
        self.assertTrue( len(resp.context['tools_list']) == 3)



import datetime
from django.utils import timezone

from catalog.models import ToolUnit, Tool, Brand, Purpose
from django.contrib.auth.models import User # Необходимо для представления User как borrower
    
class LoanedToolsByUserListViewTest(TestCase):

    def setUp(self):
        # Создание двух пользователей
        test_user1 = User.objects.create_user(username='testuser1', password='12345')
        test_user1.save()
        test_user2 = User.objects.create_user(username='testuser2', password='12345')
        test_user2.save()

        # Создание инструмента
        test_brand = Brand.objects.create(brand_name='Bosch')
        test_purpose = Purpose.objects.create(name='Electricity')
        test_tool = Tool.objects.create(type_tool='Type Tool', description = 'Some description')
        # Create purpose as a post-step
        purpose_objects_for_tool = Purpose.objects.all()
        test_tool.purpose.set(purpose_objects_for_tool) # Присвоение типов many-to-many напрямую недопустимо
        test_tool.save()

        # Создание 30 объектов ToolUnit
        number_of_tool_copies = 30
        for tool_copy in range(number_of_tool_copies):
            return_date= timezone.now() + datetime.timedelta(days = tool_copy % 5)
            if tool_copy % 2:
                the_borrower=test_user1
            else:
                the_borrower=test_user2
            status='m'
            ToolUnit.objects.create(tool=test_tool, due_back=return_date, borrower=the_borrower, status=status)

    def test_redirect_if_not_logged_in(self):
        resp = self.client.get(reverse('my-borrowed'))
        self.assertRedirects(resp, '/account/login/?next=/catalog/mytools/')

    def test_logged_in_uses_correct_template(self):
        login = self.client.login(username='testuser1', password='12345')
        resp = self.client.get(reverse('my-borrowed'))

        # Проверка что пользователь залогинился
        self.assertEqual(str(resp.context['user']), 'testuser1')
        # Проверка ответа на запрос
        self.assertEqual(resp.status_code, 200)

        # Проверка того, что мы используем правильный шаблон
        self.assertTemplateUsed(resp, 'tools/toolunit_list_borrowed_user.html')


    def test_only_borrowed_toola_in_list(self):
        login = self.client.login(username='testuser1', password='12345')
        resp = self.client.get(reverse('my-borrowed'))

        #Проверка, что пользователь залогинился
        self.assertEqual(str(resp.context['user']), 'testuser1')
        #Check that we got a response "success"
        self.assertEqual(resp.status_code, 200)

        #Проверка, что изначально у нас нет интсрументов в списке
        self.assertTrue('toolunit_list' in resp.context)
        self.assertEqual( len(resp.context['toolunit_list']),0)

        #Теперь все интсрументы "взяты на прокат"
        get_ten_books = ToolUnit.objects.all()[:10]

        for copy in get_ten_books:
            copy.status='o'
            copy.save()

        #Проверка, что все забронированные интсрументы в списке
        resp = self.client.get(reverse('my-borrowed'))
        #Проверка, что пользователь залогинился
        self.assertEqual(str(resp.context['user']), 'testuser1')
        #Проверка успешности ответа
        self.assertEqual(resp.status_code, 200)

        self.assertTrue('toolunit_list' in resp.context)

        #Подтверждение, что все интсрументы принадлежат testuser1 и взяты "на прокат"
        for toolitem in resp.context['toolunit_list']:
            self.assertEqual(resp.context['user'], toolitem.borrower)
            self.assertEqual('o', toolitem.status)

    def test_pages_ordered_by_due_date(self):

        #Изменение статуса на "в прокате"
        for copy in ToolUnit.objects.all():
            copy.status='o'
            copy.save()

        login = self.client.login(username='testuser1', password='12345')
        resp = self.client.get(reverse('my-borrowed'))

        #Пользователь залогинился
        self.assertEqual(str(resp.context['user']), 'testuser1')
        #Check that we got a response "success"
        self.assertEqual(resp.status_code, 200)

        #Подтверждение, что из всего списка показывается только 10 экземпляров
        self.assertEqual( len(resp.context['toolunit_list']),10)

        last_date=0
        for copy in resp.context['toolunit_list']:
            if last_date==0:
                last_date=copy.due_back
            else:
                self.assertTrue(last_date <= copy.due_back)
