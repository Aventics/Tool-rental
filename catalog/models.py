from datetime import date
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
import uuid


# Create your models here.
class Purpose(models.Model):
    """
    Model representing a purpose of tools.
    """   
    name = models.CharField(max_length=200, help_text='Enter a purpose of tool')

    def __str__(self):
        """
        String for representing the Model object (in Admin site etc.)
        """
        return self.name
    

class Tool(models.Model):
    '''
    Model representing a tool (Brand name, type and other)
    '''
    type_tool = models.CharField(max_length=200, help_text='Tools type')
    brand_name = models.ForeignKey('Brand', on_delete=models.SET_NULL, null=True)
    description = models.TextField(max_length=1000, help_text='Enter a brief description')
    purpose = models.ManyToManyField(Purpose, help_text='Select a purpose for this tool')

    def display_purpose(self):
        '''
        Creates a string for the Purpose. This is required to display purpose in Admin
        '''
        return ', '.join([purpose.name for purpose in self.purpose.all()[:3]])
    display_purpose.short_description = 'Purpose'

    def __str__(self):
        """
        String for representing the Model object (in Admin site etc.)
        """
        return self.type_tool
    
    def get_absolute_url(self):
        return reverse("tool-detail", args=[str(self.id)])
    

class ToolUnit(models.Model):
    '''
    Model representing a tool unit
    '''
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text='Unique ID for tools unit from the catalog')
    tool = models.ForeignKey(Tool, on_delete=models.SET_NULL, null=True)
    serial_number = models.CharField(max_length=20, help_text='Enter a serial number', null=True, blank=True)
    due_back = models.DateField(null=True, blank=True)
    borrower = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    LOAN_STATUS = (
        ('m', 'Maintenance'),
        ('o', 'On loan'),
        ('a', 'Available'),
        ('r', 'Reserved'),
    )

    status = models.CharField(max_length=1, choices=LOAN_STATUS, blank=True, default='m', help_text='Tool availability')

    class Meta:
        ordering = ['due_back']
        permissions = (("can_mark_returned", "Set book as returned"),)

    @property
    def is_overdue(self):
        if self.due_back and date.today() > self.due_back:
            return True
        return False

    def __str__(self):
        """
        String for representing the Model object (in Admin site etc.)
        """
        return f'{Tool.type_tool} {self.id}'


class Brand(models.Model):
    '''
    Model representing a tools brand
    '''
    brand_name = models.CharField(max_length=50)

    class Meta:
        ordering = ['brand_name']

    def get_absolute_url(self):
        return reverse('brand-detail', args=[str(self.id)])
    
    
    def __str__(self):
        """
        String for representing the Model object
        """
        return self.brand_name
    
