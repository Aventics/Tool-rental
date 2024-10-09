from django.test import TestCase

from catalog.models import Brand

class AuthorModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        #Set up non-modified objects used by all test methods
        Brand.objects.create(brand_name='Big')

    def test_first_name_label(self):
        brand=Brand.objects.get(id=1)
        field_label = Brand._meta.get_field('brand_name').verbose_name
        self.assertEquals(field_label,'brand name')

    def test_brand_name_max_length(self):
        brand=Brand.objects.get(id=1)
        max_length = brand._meta.get_field('brand_name').max_length
        self.assertEquals(max_length,50)

    def test_get_absolute_url(self):
        brand=Brand.objects.get(id=1)
        #This will also fail if the urlconf is not defined.
        self.assertEquals(brand.get_absolute_url(),'/catalog/brand/1')