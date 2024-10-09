from typing import Any
from django.shortcuts import render
from django.views import generic
from .models import Tool, ToolUnit, Brand, Purpose
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin


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
        template_name='catalog_page.html',
        context=context
    ) 


class ToolListView(generic.ListView):
    model = Tool
    context_object_name = 'tools_list'  
    template_name = 'tools/tools_list.html'
    paginate_by = 10


class ToolDetailView(generic.DetailView):
    model = Tool
    template_name =  'tools/tool_detail.html'


class BrandListView(generic.ListView):
    model = Brand
    context_object_name = 'brands_list'
    template_name = 'brands/brands_list.html'
    paginate_by = 10


class BrandDetailView(generic.DetailView):
    model = Tool
    template_name =  'brands/brand_detail.html'



    
class LoanedToolsByUserListView(LoginRequiredMixin,generic.ListView):
    """
    Generic class-based view listing tools on loan to current user.
    """
    model = ToolUnit
    template_name ='tools/toolunit_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        return ToolUnit.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')


class LoanedToolsByAllListView(LoginRequiredMixin,PermissionRequiredMixin,generic.ListView,):
    """
    Generic class-based view listing tools on loan to current user.
    """
    model = ToolUnit
    template_name ='tools/toolunit_list_borrowed_all.html'
    paginate_by = 10

    permission_required = 'catalog.can_mark_returned'

    def get_queryset(self):
        return ToolUnit.objects.filter(status__exact='o').order_by('due_back')

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['brand_list'] = Tool.objects.all()
    #     return context