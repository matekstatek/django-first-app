from django.urls import path
from .views import PostListView, PostDetailView, PostCreateView, PostDeleteView
from . import views

urlpatterns = [
    # strona główna
    path('', PostListView.as_view(), name='social_media-home'),
    # podstrona każdego z postów nadawana jako ID postu (pk - private key)
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    # podstrona pozwalająca na usuwanie swoich postów
    path('post/<int:pk>/delete', PostDeleteView.as_view(), name='post-delete'),
    # podstrona umożliwiająca tworzenie nowych postów
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    # wyświetlanie informacji o stronie
    path('about/', views.about, name='social_media-about'),
]
