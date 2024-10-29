from typing import Any
import datetime
import pandas
import re

from django.shortcuts import render
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import permission_required
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin

from .models import Tool, ToolUnit, Brand
from .forms import RenewToolForm, UploadToolsFileForm
from .utils import create_toolunit_from_df

# Отображение страницы каталога
def catalog_main(request):
    # Подсчет инстрементов
    num_tools = Tool.objects.all().count()
    num_tool_units = ToolUnit.objects.all().count()
    # Доступные инстременты
    num_tool_available = ToolUnit.objects.filter(status__exact='a').count()
    num_brands = Brand.objects.count()

    context = {'num_tools':num_tools, 
               'num_tool_units':num_tool_units, 
               'num_brands':num_brands, 
               'num_tool_available':num_tool_available, }

    return render(
        request = request,
        template_name='catalog_page.html',
        context=context
    ) 



    # Список инструментов
class ToolListView(generic.ListView):
    model = Tool
    context_object_name = 'tools_list'  
    template_name = 'tools/tools_list.html'
    paginate_by = 15


    # Детали инструментов
class ToolDetailView(generic.DetailView):
    model = Tool
    template_name =  'tools/tool_detail.html'
    paginate_by = 15


    # Список производителей
class BrandListView(generic.ListView):
    model = Brand
    context_object_name = 'brands_list'
    template_name = 'brands/brands_list.html'
    paginate_by = 15


    # Детали производителей
class BrandDetailView(generic.DetailView):
    model = Brand
    template_name =  'brands/brand_detail.html'
    paginate_by = 10


    # Список экземпляров инструмента
class ToolUnitDetailView(generic.DetailView):
    model = ToolUnit 
    template_name = 'tools/tool_unit_detail.html'
    context_object_name = 'tool_unit'
    paginate_by = 15


# Список инструментов арендованных определенным пользователем
class LoanedToolsByUserListView(LoginRequiredMixin,generic.ListView):
    model = ToolUnit
    template_name ='tools/toolunit_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        return ToolUnit.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')


# Список всех арендованных инструментов
class LoanedToolsByAllListView(LoginRequiredMixin,PermissionRequiredMixin,generic.ListView,):
    model = ToolUnit
    template_name ='tools/toolunit_list_borrowed_all.html'
    paginate_by = 10

    permission_required = 'catalog.can_mark_returned'

    def get_queryset(self):
        return ToolUnit.objects.filter(status__exact='o').order_by('due_back')
    

# Ограничение доступа
@permission_required('catalog.can_mark_returned')
def renew_tool_stuff(request, pk):
    tool_inst = get_object_or_404(ToolUnit, pk=pk)

    if request.method == 'POST':
        form = RenewToolForm(request.POST)

        if form.is_valid():
            tool_inst.due_back = form.cleaned_data['renewal_date']
            tool_inst.save()

            return HttpResponseRedirect(reverse('all-borrowed'))
    # Если это GET, создать форму по умолчанию.
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewToolForm(initial={'renewal_date': proposed_renewal_date,})

    return render(request, 'tools/tool_stuff.html', {'form': form, 'toolinst':tool_inst})



# Управление типом инструмента от имени администратора:
    # Создать инструмент
class ToolCreate(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, generic.CreateView):
    permission_required = 'catalog.can_mark_returned'
    model = Tool
    fields = '__all__'
    template_name = 'tools/tool_form.html'   
    success_message = "Интсрумент успешно создан."

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, self.success_message)
        return response


    # Изменить инструмент
class ToolUpdate(UpdateView):
    model = Tool
    fields = '__all__'
    template_name = 'tools/tool_form.html'
    update_message = "Интсрумент успешно изменен."

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.info(self.request, self.update_message)
        return response


    # Удалить инструмент
class ToolDelete(DeleteView):
    model = Tool
    success_url = reverse_lazy('tools')
    template_name = 'tools/tool_confirm_delete.html'
    delete_message = "Интсрумент успешно удален."

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.error(self.request, self.delete_message)
        return response



# Управление еденицей инструмента от имени администратора
    # Создать экземпляр инструмента
class ToolUnitCreate(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, generic.CreateView):
    permission_required = 'catalog.can_mark_returned'
    model = ToolUnit
    fields = '__all__'
    template_name = 'tools/tool_form.html'   
    success_message = "Интсрумент успешно создан."

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, self.success_message)
        return response


    # Изменить экземпляр инструмента
class ToolUnitUpdate(UpdateView):
    model = ToolUnit
    fields = '__all__'
    template_name = 'tools/tool_form.html'
    update_message = "Интсрумент успешно изменен."

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.info(self.request, self.update_message)
        return HttpResponseRedirect(reverse('tools'))


    # Удалить экземпляр инструмента
class ToolUnitDelete(DeleteView):
    model = ToolUnit
    success_url = reverse_lazy('tools')
    template_name = 'tools/tool_unit_confirm_delete.html'
    delete_message = "Инструмент успешно удален."

    def delete(self, request, *args, **kwargs):
        messages.success(request, self.delete_message)
        return super().delete(request, *args, **kwargs)
    

# Управление брендом от имени администратора
    # Создать бренд
class BrandCreate(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, generic.CreateView):
    permission_required = 'catalog.can_mark_returned'
    model = Brand
    fields = '__all__'
    template_name = 'brands/brand_form.html'   
    success_message = "Бренд успешно создан."

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, self.success_message)
        return response


    # Изменить бренд
class BrandUpdate(UpdateView):
    model = Brand
    fields = '__all__'
    template_name = 'brands/brand_form.html'
    update_message = "Бренд успешно изменен."

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.info(self.request, self.update_message)
        return response


    # Удалить бренд
class BrandDelete(DeleteView):
    model = Brand
    success_url = reverse_lazy('brands')
    template_name = 'brands/brand_confirm_delete.html'
    delete_message = "Бренд успешно удален."

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.error(self.request, self.delete_message)
        return response



# Загрузка файлов:
def tool_file_upload_view(request):
    if request.method == 'POST':
        if 'file' not in request.FILES:
            return HttpResponse('No file uploaded')
               
        file = request.FILES['file']
        file_format = file.name.split('.')[-1].lower()
        
        if file_format == 'csv':
            try:
                df = pandas.read_csv(file)
            except Exception as e:
                return HttpResponse(f'Error reading CSV file: {e}')
        elif file_format in ['xls', 'xlsx']:
            try:
                df = pandas.read_excel(file)
            except Exception as e:
                return HttpResponse(f'Error reading Excel file: {e}')
        else:
            return HttpResponse('Unsupported file format')
            

        create_toolunit_from_df(df)


        return HttpResponse(df.to_html())
    else:
        form = UploadToolsFileForm()
        return render(request, 'tools/tool_file_upload.html', context={'form': form})
    


# Функция поиска
def searching(request):
    if request.method == "POST":
        searched = request.POST.get('searched').title()
        searched = re.sub(r'\b\w{1,2}\b', lambda match: match.group(0) * (len(match.group(0)) + 1), searched)
        tools_results = Tool.objects.filter(type_tool__icontains=searched)
        brand_results = Brand.objects.filter(brand_name__icontains=searched)
        tool_unit_results = ToolUnit.objects.filter(tool_name__icontains=searched)
        return render(request, "catalog/search_page.html", {'searched':searched, 
                                                            'tools_results':tools_results,
                                                            'brand_results':brand_results,
                                                            'tool_unit_results':tool_unit_results})
    else:
        return render(request, "catalog/search_page.html")
    