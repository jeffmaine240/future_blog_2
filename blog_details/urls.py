from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views
from .forms import CustomAuthenticationForm


urlpatterns = [
    path("", views.StartingPageView.as_view(), name='home'),
    path("tag/<str:tag_caption>", views.StartingPageView.as_view(), name='post_tag'),
    path("posts/<slug:slug>/", views.PostDetailView.as_view(), name="specific"),
    path("about/", views.AboutView.as_view(), name='about'),
    path("contact/", views.ContactView.as_view(), name='contact'),
    path("create/", views.CreatePostView.as_view(), name='create'),
    path("delete/<slug:slug>", views.DeletePostView.as_view(), name='delete'),
    path("update/<slug:slug>", views.UpdatePostView.as_view(), name='update'),
    path('login/', auth_views.LoginView.as_view(authentication_form=CustomAuthenticationForm), name='login'),
    path('', include('django.contrib.auth.urls')),
    path("register/", views.RegisterView.as_view(), name='register'),


]
