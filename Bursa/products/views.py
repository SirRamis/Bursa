from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView

from .forms import *
from .models import *
from products.utils import DataMixin, menu


#menu = [{'title': "О сайте", 'url_name': 'about'},
#        {'title': "Добавить статью", 'url_name': 'add_page'},
 #       {'title': "Обратная связь", 'url_name': 'contact'},
 #       {'title': "Войти", 'url_name': 'login'},
 #       ]

class ProductsHome(DataMixin, ListView):
    #paginate_by = 3
    model = Products
    template_name = 'products/index.html'
    context_object_name = 'posts'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Главная страница")
        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):    # Отображает опубликованные списки
        return Products.objects.filter(is_published=True).select_related('cat')
#def index(request):
#    posts = Products.objects.all()
#    cats = Category.objects.all()
#    context = {
#        'posts': posts,
#        'cats': cats,
#        'menu': menu,
#        'title': 'Главная страница',
#        'cat_selected': 0,
#    }
#    return render(request, 'products/index.html', context=context)


def about(request):
    contact_list = Products.objects.all()
    paginator = Paginator(contact_list, 3)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'products/about.html', {'page_obj': page_obj, 'menu': menu, 'title': 'О сайте'})
class AddPage(LoginRequiredMixin, DataMixin,CreateView):
    form_class = AddPostForm
    template_name = 'products/addpage.html'
    success_url = reverse_lazy('home')
    login_url = reverse_lazy('home')
    raise_exception = True
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Добавление статьи")
        return dict(list(context.items()) + list(c_def.items()))
#def addpage(request):
 #   if request.method == 'POST':        # это дает возврат заполненных полей
 #       form = AddPostForm(request.POST, request.FILES)
 #       if form.is_valid():
#            #print(form.cleaned_data)
 #           form.save()      #автоматически заносит в базу данных
 #           return redirect('home')
 #   else:
 #       form = AddPostForm()
 #   return render(request, 'products/addpage.html', {'form': form, 'menu': menu, 'title': 'Добавление статьи'})

def contact(request):
    return render(request, 'products/contact.html', {'menu': menu, 'title': 'Мы с вами свяжемся'})


def login(request):
    return HttpResponse("Авторизация")


def pegeNotFound(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')


#def show_post(request, post_slug):
 #   post = get_object_or_404(Products, slug=post_slug)

 #   context = {
 #       'post': post,
 #       'menu': menu,
 #       'title': post.title,
 #       'cat_selected': post.cat_id,
 #   }
 #   return render(request, 'products/post.html', context=context)
class ShowPost(DataMixin, DetailView):
    model = Products
    template_name = 'products/post.html'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title=context['post'])
        return dict(list(context.items()) + list(c_def.items()))


class ProductsCategory(DataMixin, ListView):
    model = Products
    template_name = 'products/index.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_queryset(self):
        return Products.objects.filter(cat__slug=self.kwargs['cat_slug'], is_published=True).select_related('cat')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Категория - ' + str(context['posts'][0].cat),
                                      cat_selected=context['posts'][0].cat_id)
        return dict(list(context.items()) + list(c_def.items()))
#def show_category(request, cat_id):
#    posts = Products.objects.filter(cat_id=cat_id)
    # cats = Category.objects.all()
    # если пост отсутствует, выводит 404:
#    if len(posts) == 0:
 #       raise Http404()

 #   context = {
  #      'posts': posts,
        # 'cats': cats,
#        'menu': menu,
#        'title': 'Отображение по категориям',
#        'cat_selected': cat_id,
#    }

 #   return render(request, 'products/index.html', context=context)

class RegisterUser(DataMixin, CreateView):
    form_class = RegisterUserForm
    template_name = 'products/register.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Регистрация")
        return dict(list(context.items()) + list(c_def.items()))