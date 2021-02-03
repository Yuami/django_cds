from django.urls import path

from . import views

app_name = 'cds'
urlpatterns = [
    path('', views.BandIndexView.as_view(), name='list'),
    path('create/', views.BandCreateView.as_view(), name='create'),
    path('<int:pk>/', views.BandDetailView.as_view(), name='detail'),
    path('<int:pk>/update', views.BandUpdateView.as_view(), name='update'),
    path('<int:pk>/delete', views.BandDeleteView.as_view(), name='delete'),
]
