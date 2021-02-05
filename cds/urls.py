from django.urls import path

from cds.views import views

app_name = 'cds'
urlpatterns = [
    path('', views.BandIndexView.as_view(), name='band-list'),
    path('create/', views.BandCreateView.as_view(), name='band-create'),
    path('<int:pk>/', views.BandDetailView.as_view(), name='band-detail'),
    path('<int:pk>/update', views.BandUpdateView.as_view(), name='band-update'),
    path('<int:pk>/delete', views.BandDeleteView.as_view(), name='band-delete'),

    path('cd/create', views.CdCreateView.as_view(), name='cd-create'),
    path('cd/<int:pk>', views.CdDetailView.as_view(), name='cd-detail'),
    path('cd/<int:pk>/update', views.CdUpdateView.as_view(), name='cd-update'),
    path('cd/<int:pk>/delete', views.CdDeleteView.as_view(), name='cd-delete'),

    path('song/create', views.SongCreateView.as_view(), name='song-create'),
    path('song/<int:pk>', views.SongDetailView.as_view(), name='song-detail'),
    path('song/<int:pk>/update', views.SongUpdateView.as_view(), name='song-update'),
    path('song/<int:pk>/delete', views.SongDeleteView.as_view(), name='song-delete'),
]
