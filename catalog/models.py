from django.db import models
from django.urls import reverse
import uuid

# Create your models here.
class Purpose(models.Model):
    """
    Model representing a purpose of tools.
    """   
    name = models.Charfield(max_length=200, help_text='Enter a purpose of tool')

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

    def __str__(self):
        """
        String for representing the Model object (in Admin site etc.)
        """
        return self.type_tool
    
    def get_absolute_url(self):
        return reverse("type_detail", args=[str(self.id)])
    

class ToolUnit(models.Model):
    '''
    Model representing a tool unit
    '''
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text='Unique ID for tools unit from the catalog')
    tool = models.ForeignKey(Tool, on_delete=models.SET_NULL, null=True)
    due_back = models.DateField(null=True, blank=True)
    LOAN_STATUS = (
        ('m', 'Maintenance'),
        ('o', 'On loan'),
        ('a', 'Available'),
        ('r', 'Reserved'),
    )

    status = models.CharField(max_length=1, choices=LOAN_STATUS, blank=True, default='m', help_text='Tool availability')

    class Meta:
        ordering = ['due_back']

    def __str__(self):
        """
        String for representing the Model object (in Admin site etc.)
        """
        return f'{self.id} {self.tool.type_tool}'


class Brand(models.Model):
    '''
    Model representing a tools brand
    '''
    brand_name = models.CharField(max_length=50)
    serial_number = models.CharField(max_length=20)

    def get_absolute_url(self):
        return reverse("Brand_detail", args=[str(self.id)])
    
    def __str__(self):
        """
        String for representing the Model object
        """
        return self.brand_name