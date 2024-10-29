from datetime import date
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
import uuid


# Модель назначение инструмента.
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
    

# Модель категории инструмента
class Tool(models.Model):
    type_tool = models.CharField(max_length=200, help_text='Tools type')
    purpose = models.ManyToManyField(Purpose, help_text='Select a purpose for this tool')

    # Преобразование "назначения" в строку для отображения
    def display_purpose(self):
        return ', '.join([purpose.name for purpose in self.purpose.all()[:3]])
    display_purpose.short_description = 'Purpose'

    def __str__(self):
        return self.type_tool
    
    def get_absolute_url(self):
        return reverse("tool-detail", args=[str(self.id)])
    

# Модель производителя
class Brand(models.Model):
    brand_name = models.CharField(max_length=50)

    # Сортировка
    class Meta:
        ordering = ['brand_name']

    def get_absolute_url(self):
        return reverse('brand-detail', args=[str(self.id)])
    
    def __str__(self):
        return self.brand_name
    

# Модель экземпляра инструмента
class ToolUnit(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text='Unique ID for tools unit from the catalog')
    tool = models.ForeignKey(Tool, on_delete=models.SET_NULL, null=True)
    tool_name = models.CharField(max_length=200, help_text='Enter a tool name', null=True, blank=True)
    brand_name = models.ForeignKey(Brand, on_delete=models.SET_NULL, null=True)
    description = models.TextField(max_length=1000, help_text='Enter a brief description', null=True, blank=True)
    serial_number = models.CharField(max_length=20, help_text='Enter a serial number', null=True, blank=True)
    due_back = models.DateField(null=True, blank=True)
    borrower = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    cover = models.URLField('cover_url', null=True, blank=True, help_text='URL for tool cover')

    LOAN_STATUS = (
        ('m', 'На обслуживании'),
        ('o', 'В аренде'),
        ('a', 'Доступен'),
        ('r', 'Зарезервирован'),
    )

    status = models.CharField(max_length=1, choices=LOAN_STATUS, blank=True, default='m', help_text='Tool availability')

    class Meta:
        ordering = ['status']
        permissions = (("can_mark_returned", "Set tool as returned"),)

    @property
    def is_overdue(self):
        if self.due_back and date.today() > self.due_back:
            return True
        return False
    
    def get_absolute_url(self):
        return reverse('tool_unit_update', kwargs={'pk': self.pk})

    def __str__(self):
        return f'{Tool.type_tool} {self.id}'


    
