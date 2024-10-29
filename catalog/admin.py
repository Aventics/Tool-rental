from django.contrib import admin
from .models import Brand, Purpose, Tool, ToolUnit

admin.site.register(Purpose)

# Регистрация класса Brand
class BrandAdmin(admin.ModelAdmin):
    pass
admin.site.register(Brand, BrandAdmin)


class ToolUnitInline(admin.TabularInline):
    extra = 0
    model = ToolUnit


# Регистрация класса  Tool с использованием декоратора
@admin.register(Tool)
class ToolAdmin(admin.ModelAdmin):
    list_display = ('type_tool', 'display_purpose')
    inlines = [ToolUnitInline]


# # Регистрация класса  ToolUnit с использованием декоратора
@admin.register(ToolUnit)
class ToolUnitAdmin(admin.ModelAdmin):
    list_display = ('tool', 'tool_name', 'brand_name', 'borrower', 'serial_number', 'due_back')
    list_filter = ('status', 'due_back')
    fieldsets = (
        (None, {
            'fields': ('tool', 'tool_name', 'brand_name', 'serial_number', 'id')
        }),
        ('Availability',{
            'fields': ('status', 'due_back', 'borrower')
        })
    )