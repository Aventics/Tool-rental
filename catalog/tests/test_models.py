from django.test import TestCase
from catalog.models import Brand, Tool, ToolUnit, Purpose

class BrandModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        Brand.objects.create(brand_name='Big')

    def test_first_name_label(self):
        brand=Brand.objects.get(id=1)
        field_label = brand._meta.get_field('brand_name').verbose_name
        self.assertEquals(field_label,'brand name')

    def test_brand_name_max_length(self):
        brand=Brand.objects.get(id=1)
        max_length = brand._meta.get_field('brand_name').max_length
        self.assertEquals(max_length,50)

    def test_get_absolute_url(self):
        brand=Brand.objects.get(id=1)
        self.assertEquals(brand.get_absolute_url(),'/catalog/brand/1')


class ToolModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        Tool.objects.create(type_tool='Hammer')
        Tool.objects.create(description='Some description')

    def test_type_tool_label(self):
        tool=Tool.objects.get(id=1)
        field_label = tool._meta.get_field('type_tool').verbose_name
        self.assertEquals(field_label,'type tool')

    def test_tool_description(self):
        tool=Tool.objects.get(id=1)
        field_label= tool._meta.get_field('description').verbose_name
        self.assertEquals(field_label, 'description')

    def test_type_tool_max_length(self):
        tool=Tool.objects.get(id=1)
        max_length = tool._meta.get_field('type_tool').max_length
        self.assertEquals(max_length,200)

    def test_description_tool_max_length(self):
        tool=Tool.objects.get(id=1)
        max_length = tool._meta.get_field('description').max_length
        self.assertEquals(max_length,1000)

    def test_get_absolute_url(self):
        tool=Tool.objects.get(id=1)
        self.assertEquals(tool.get_absolute_url(),'/catalog/tool/1')

