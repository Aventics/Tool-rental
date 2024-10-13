from typing import Any
from django.shortcuts import render
from django.views import generic
from .models import Tool, ToolUnit, Brand, Purpose
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
import datetime
from django.contrib import messages
from django.contrib.auth.decorators import permission_required
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin


from .forms import RenewToolForm


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
    paginate_by = 10


class BrandListView(generic.ListView):
    model = Brand
    context_object_name = 'brands_list'
    template_name = 'brands/brands_list.html'
    paginate_by = 10


class BrandDetailView(generic.DetailView):
    model = Brand
    template_name =  'brands/brand_detail.html'
    paginate_by = 10



    
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
    


@permission_required('catalog.can_mark_returned')
def renew_tool_stuff(request, pk):
    tool_inst = get_object_or_404(ToolUnit, pk=pk)

    # Если данный запрос типа POST, тогда
    if request.method == 'POST':

        # Создаём экземпляр формы и заполняем данными из запроса (связывание, binding):
        form = RenewToolForm(request.POST)

        # Проверка валидности данных формы:
        if form.is_valid():
            # Обработка данных из form.cleaned_data
            #(здесь мы просто присваиваем их полю due_back)
            tool_inst.due_back = form.cleaned_data['renewal_date']
            tool_inst.save()

            # Переход по адресу 'all-borrowed':
            return HttpResponseRedirect(reverse('all-borrowed') )

    # Если это GET (или какой-либо ещё), создать форму по умолчанию.
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewToolForm(initial={'renewal_date': proposed_renewal_date,})

    return render(request, 'tools/tool_stuff.html', {'form': form, 'toolinst':tool_inst})


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


class ToolUpdate(UpdateView):
    model = Tool
    fields = '__all__'
    template_name = 'tools/tool_form.html'
    update_message = "Интсрумент успешно изменен."

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.info(self.request, self.update_message)
        return response

class ToolDelete(DeleteView):
    model = Tool
    success_url = reverse_lazy('tools')
    template_name = 'tools/tool_confirm_delete.html'
    delete_message = "Интсрумент успешно удален."

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.error(self.request, self.delete_message)
        return response

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['brand_list'] = Tool.objects.all()
    #     return context