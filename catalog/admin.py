from django.contrib import admin
from .models import Brand, Purpose, Tool, ToolUnit

# Register your models here.
# admin.site.register(Tool)
admin.site.register(Purpose)
# admin.site.register(Brand)
# admin.site.register(ToolUnit)


# Define the Admin class
class BrandAdmin(admin.ModelAdmin):
    pass

# Register the admin class with the associated model
admin.site.register(Brand, BrandAdmin)

class ToolUnitInline(admin.TabularInline):
    extra = 0
    model = ToolUnit

# Register the admin classes for Tool using the decorator
@admin.register(Tool)
class ToolAdmin(admin.ModelAdmin):
    list_display = ('type_tool', 'brand_name', 'display_purpose')
    inlines = [ToolUnitInline]


# Register the admin class for ToolUnit with the decorator
@admin.register(ToolUnit)
class ToolUnitAdmin(admin.ModelAdmin):
    list_display = ('tool', 'borrower', 'serial_number', 'due_back')
    list_filter = ('status', 'due_back')
    fieldsets = (
        (None, {
            'fields': ('tool', 'serial_number', 'id')
        }),
        ('Availability',{
            'fields': ('status', 'due_back', 'borrower')
        })
    )