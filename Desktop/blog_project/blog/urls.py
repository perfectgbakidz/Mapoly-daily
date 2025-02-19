from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    # Authentication
    path('register/', views.register, name='register'),
    path("profile/update/", views.update_profile, name="update_profile"),
    path("password-change/", auth_views.PasswordChangeView.as_view(template_name="blog/password_change.html"), name="password_change"),
    path("password-change/done/", auth_views.PasswordChangeDoneView.as_view(template_name="blog/password_change_done.html"), name="password_change_done"),
    path('login/', auth_views.LoginView.as_view(template_name='blog/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='blog_list'), name='logout'),
    path('profile/', views.profile, name='profile'),
    path('about/', views.about, name='about'),  
    path('contact/', views.contact, name='contact'), 
    path('search/', views.search, name='search'),

    # Blog Post URLs
    path('', views.blog_list, name='blog_list'),
    path('post/new/', views.blog_create, name='blog_create'),
    path('post/<slug:slug>/', views.blog_detail, name='blog_detail'),
    path('post/<slug:slug>/edit/', views.blog_update, name='blog_update'),
    path('post/<slug:slug>/delete/', views.blog_delete, name='blog_delete'),
    path('post/<slug:slug>/like/', views.blog_like, name='blog_like'),
    path('post/<slug:slug>/comment/', views.add_comment, name='add_comment'),

    # Category Pages
    path('category/<slug:slug>/', views.category_posts, name='category_posts'),

    # User Dashboard
    path('dashboard/', views.user_dashboard, name='user_dashboard'),

    # Password Reset URLs
    path('password-reset/', 
         auth_views.PasswordResetView.as_view(template_name='blog/password_reset.html'), 
         name='password_reset'),
    
    path('password-reset/done/', 
         auth_views.PasswordResetDoneView.as_view(template_name='blog/password_reset_done.html'), 
         name='password_reset_done'),
    
    path('password-reset-confirm/<uidb64>/<token>/', 
         auth_views.PasswordResetConfirmView.as_view(template_name='blog/password_reset_confirm.html'), 
         name='password_reset_confirm'),
    
    path('password-reset-complete/', 
         auth_views.PasswordResetCompleteView.as_view(template_name='blog/password_reset_complete.html'), 
         name='password_reset_complete'),
]

