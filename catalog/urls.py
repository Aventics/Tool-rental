from django.urls import path, re_path
from . import views

urlpatterns = [
        path('', views.catalog_main, name='catalog_main'),
        re_path(r'^tools/$', views.ToolListView.as_view(), name='tools'),
        re_path(r'^tool/(?P<pk>[0-9a-f-]+)$', views.ToolDetailView.as_view(), name='tool-detail'),
        re_path(r'^brands/$', views.BrandListView.as_view(), name='brands'),
        re_path(r'^brand/(?P<pk>\d+)$', views.BrandDetailView.as_view(), name='brand-detail'),
        re_path(r'^mytools/$', views.LoanedToolsByUserListView.as_view(), name='my-borrowed'),
        re_path(r'^all_borrowed_tools/$', views.LoanedToolsByAllListView.as_view(), name='all-borrowed'),
        re_path(r'^tool/(?P<pk>[-\w]+)/renew/$', views.renew_tool_stuff, name='renew-tool-stuff'),
        re_path(r'^tools/file_upload/$', views.tool_file_upload_view, name='tool_file_upload'),
        re_path(r'^tools/(?P<pk>[0-9a-f-]+)$', views.ToolUnitDetailView.as_view(), name='tool-unit-detail'),
        

        
        re_path(r'^tool/create/$', views.ToolCreate.as_view(), name='tool_create'),
        re_path(r'^tool/(?P<pk>\d+)/update/$', views.ToolUpdate.as_view(), name='tool_update'),
        re_path(r'^tool/(?P<pk>\d+)/delete/$', views.ToolDelete.as_view(), name='tool_delete'),
        re_path(r'^toolunit/create/$', views.ToolUnitCreate.as_view(), name='tool_unit_create'),
        re_path(r'^toolunit/(?P<pk>[0-9a-f-]+)/update/$', views.ToolUnitUpdate.as_view(), name='tool_unit_update'),
        re_path(r'^toolunit/(?P<pk>[0-9a-f-]+)/delete/$', views.ToolUnitDelete.as_view(), name='tool_unit_delete'),
        re_path(r'^brand/create/$', views.BrandCreate.as_view(), name='brand_create'),
        re_path(r'^brand/(?P<pk>\d+)/update/$', views.BrandUpdate.as_view(), name='brand_update'),
        re_path(r'^brand/(?P<pk>\d+)/delete/$', views.BrandDelete.as_view(), name='brand_delete'),

        path("search/", views.searching, name="searching"),
        
]


