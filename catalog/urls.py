from django.urls import path, re_path
from . import views

urlpatterns = [
        path('', views.catalog_main, name='catalog_main'),
        re_path(r'^tools/$', views.ToolListView.as_view(), name='tools'),
        re_path(r'^tool/(?P<pk>\d+)$', views.ToolDetailView.as_view(), name='tool-detail'),
        re_path(r'^brands/$', views.BrandListView.as_view(), name='brands'),
        re_path(r'^brand/(?P<pk>\d+)$', views.BrandDetailView.as_view(), name='brand-detail'),
        re_path(r'^mytools/$', views.LoanedToolsByUserListView.as_view(), name='my-borrowed'),
        re_path(r'^all_borrowed_tools/$', views.LoanedToolsByAllListView.as_view(), name='all-borrowed'),
        re_path(r'^tool/(?P<pk>[-\w]+)/renew/$', views.renew_tool_stuff, name='renew-tool-stuff'),
        re_path(r'^tool/create/$', views.ToolCreate.as_view(), name='tool_create'),
        re_path(r'^tool/(?P<pk>\d+)/update/$', views.ToolUpdate.as_view(), name='tool_update'),
        re_path(r'^tool/(?P<pk>\d+)/delete/$', views.ToolDelete.as_view(), name='tool_delete'),
]


