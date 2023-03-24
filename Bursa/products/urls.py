from django.urls import path, re_path
from .views import *
from django.views.decorators.cache import cache_page



urlpatterns = [
    path('', cache_page(60)(ProductsHome.as_view()), name='home'),
    path('about/', about, name='about'),
    path('addpage/', AddPage.as_view(), name='add_page'),
    path('contact/', contact, name='contact'),
    path('login/', RegisterUser.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('post/<slug:post_slug>/', ShowPost.as_view(), name='post'),
    path('category/<slug:cat_slug>/', ProductsCategory.as_view(), name='category'),

]
