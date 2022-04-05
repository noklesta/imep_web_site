from django.urls import path

from . import views
from django.contrib.flatpages import views as fp_views

app_name = 'proses'

"""
    path('', views.IndexView.as_view(), name='index'),
"""

urlpatterns = [
    path('', views.index, name='index'),

    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path(r'import/', views.import_sheet, name='import'),
    path(r'explicits/', views.prose_table, name='explicit'),
    path(r'incipits/', views.prose_table, name='incipit'),
    path(r'subjects/', views.prose_table, name='subject'),
    path(r'titles/', views.prose_table, name='title'),
    path(r'volumes/', views.volume_index, name='volumes'),
    # path(r'book/', views.view_book, name='book'),

    path(r'search/', views.search),
    # path(r'volumes/', fp_views.flatpage, {'url':'/volumes/'}, name='volumes'),
    path(r'about/', fp_views.flatpage, {'url':'/about/'}, name='about'),


]