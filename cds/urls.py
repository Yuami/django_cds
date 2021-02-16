from django.urls import path, include

from cds.views import views

app_name = 'cds'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index-view'),

    path('artist/', views.ArtistListView.as_view(), name='artist-list'),
    path('artist/create/', views.ArtistCreateView.as_view(), name='artist-create'),
    path('artist/<int:pk>/', views.ArtistDetailView.as_view(), name='artist-detail'),
    path('artist/<int:pk>/update', views.ArtistUpdateView.as_view(), name='artist-update'),
    path('artist/<int:pk>/delete', views.ArtistDeleteView.as_view(), name='artist-delete'),

    path('band/', views.BandIndexView.as_view(), name='band-list'),
    path('band/create/', views.BandCreateView.as_view(), name='band-create'),
    path('band/<int:pk>/', views.BandDetailView.as_view(), name='band-detail'),
    path('band/<int:pk>/update', views.BandUpdateView.as_view(), name='band-update'),
    path('band/<int:pk>/delete', views.BandDeleteView.as_view(), name='band-delete'),

    path('cd/create', views.CdCreateView.as_view(), name='cd-create'),
    path('cd/<int:pk>', views.CdDetailView.as_view(), name='cd-detail'),
    path('cd/<int:pk>/update', views.CdUpdateView.as_view(), name='cd-update'),
    path('cd/<int:pk>/delete', views.CdDeleteView.as_view(), name='cd-delete'),

    path('song/create', views.SongCreateView.as_view(), name='song-create'),
    path('song/<int:pk>', views.SongDetailView.as_view(), name='song-detail'),
    path('song/<int:pk>/update', views.SongUpdateView.as_view(), name='song-update'),
    path('song/<int:pk>/delete', views.SongDeleteView.as_view(), name='song-delete'),

    path('song/<int:pk>/json', views.SongSearchJSON.as_view(), name='song-json'),
    path('song/search/', views.SongSearchView.as_view(), name='song-search'),
]
