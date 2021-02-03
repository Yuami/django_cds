from django.urls import path

from . import views

app_name = 'cds'
urlpatterns = [
    path('', views.BandIndexView.as_view(), name='band-list'),
    path('create/', views.BandCreateView.as_view(), name='band-create'),
    path('<int:pk>/', views.BandDetailView.as_view(), name='band-detail'),
    path('<int:pk>/update', views.BandUpdateView.as_view(), name='band-update'),
    path('<int:pk>/delete', views.BandDeleteView.as_view(), name='band-delete'),
    path('cd/<int:pk>/create', views.CdCreateView.as_view(), name='cd-create'),
    path('cd/<int:pk>/update', views.CdUpdateView.as_view(), name='cd-update'),
    path('cd/<int:pk>/delete', views.CdDeleteView.as_view(), name='cd-delete'),
]
