from django.contrib import admin
from .models import Brand, Purpose, Tool, ToolUnit

admin.site.register(Tool)
admin.site.register(Purpose)
admin.site.register(Brand)
admin.site.register(ToolUnit)

# Register your models here.
