from django.urls import path
from . import views
from .views import PostDeleteView, PostUpdateView, PostDetailView
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import include
from django.conf.urls import url


urlpatterns = [
    # path('', views.postpage, name="postpage"),
    path('login', views.login, name='login'),
    path('home', views.home, name='home'),
    path('otp', views.checkOtp, name="otp"),
    path('', views.checkUser, name="checkUser"),
    path('logout', views.logout, name="logout"),
    path('newpost', views.newpost, name="newpost"),
    path('postcreate', views.create, name="postcreate"),
    path('deletepost', views.delete, name="deletepost"),
    path('postpage', views.postpage, name="postpage"),
    path('profile', views.profile, name="profile"),
    path("post/<int:pk>/update/", PostUpdateView.as_view(), name="post-update"),
    path("post/<int:pk>/delete/", PostDeleteView.as_view(), name="post-delete"),
    path("post/<int:pk>/", PostDetailView.as_view(), name="post-detail"),
    # url(r'^', include('home.urls', namespace='home')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += staticfiles_urlpatterns()
