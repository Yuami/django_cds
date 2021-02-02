from django.urls import path

from . import views

app_name = 'cds'
urlpatterns = [
    path('', views.BandIndexView.as_view(), name='index'),
    # path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    # path('<int:pk>/edit', views.EditView.as_view(), name='edit'),
]
