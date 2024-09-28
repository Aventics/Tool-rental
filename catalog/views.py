from django.shortcuts import render
from .models import Tool, ToolUnit, Brand, Purpose

# Create your views here.
def catalog_main(request):
    '''
    funk review for home page
    '''
    # Gen "count" some main objects
    num_tools = Tool.objects.all().count()
    num_tool_units = ToolUnit.objects.all().count()
    # Available tools ( status = 'a')
    num_tool_available = ToolUnit.objects.filter(status__exact='a').count()
    num_brands = Brand.objects.count() # Method "all()" is default

    context = {'num_tools':num_tools, 
               'num_tool_units':num_tool_units, 
               'num_brands':num_brands, 
               'num_tool_available':num_tool_available, }

    # Drawing HTML-tamplate 'index.html' with data inside 'context'
    return render(
        request = request,
        template_name='catalog_main_page.html',
        context=context
    ) 