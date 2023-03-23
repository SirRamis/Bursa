from urllib import request

from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView

from .forms import *
from .models import *

menu = [{'title': "О сайте", 'url_name': 'about'},
        {'title': "Добавить статью", 'url_name': 'add_page'},
        {'title': "Обратная связь", 'url_name': 'contact'},
        {'title': "Войти", 'url_name': 'login'},
        ]

class ProductsHome(ListView):
    model = Products
    template_name = 'products/index.html'
    context_object_name = 'posts'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = menu
        context['title'] = 'Главная страница'
        context['cat_selected'] = 0
        return context
        #c_def = self.get_user_context(title="Главная страница")
        #return dict(list(context.items()) + list(c_def.items()))

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
    return render(request, 'products/about.html', {'menu': menu, 'title': 'О сайте'})

class AddPage(CreateView):
    form_class = AddPostForm
    template_name = 'products/addpage.html'
    success_url = reverse_lazy('home')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Добавление статьи'
        context['menu'] = menu
        return context
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
class ShowPost(DetailView):
    model = Products
    template_name = 'products/post.html'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = context['post']
        context['menu'] = menu
        return context


class ProductsCategory(ListView):
    model = Products
    template_name = 'products/index.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_queryset(self):
        return Products.objects.filter(cat__slug=self.kwargs['cat_slug'], is_published=True).select_related('cat')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = menu
        context['title'] = 'Категория - ' + str(context['posts'][0].cat)
        context['cat_selected'] = context['posts'][0].cat_id
        return context
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
