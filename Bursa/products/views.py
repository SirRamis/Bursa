from urllib import request

from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, redirect, get_object_or_404

from .forms import *
from .models import *

menu = [{'title': "О сайте", 'url_name': 'about'},
        {'title': "Добавить статью", 'url_name': 'add_page'},
        {'title': "Обратная связь", 'url_name': 'contact'},
        {'title': "Войти", 'url_name': 'login'},
        ]


def index(request):
    posts = Products.objects.all()
    cats = Category.objects.all()
    context = {
        'posts': posts,
        'cats': cats,
        'menu': menu,
        'title': 'Главная страница',
        'cat_selected': 0,
    }
    return render(request, 'products/index.html', context=context)


def about(request):
    return render(request, 'products/about.html', {'menu': menu, 'title': 'О сайте'})

#def addpage(request):
#    if request.method == 'POST':
#        form = AddPostForm(request.POST, request.FILES)
#        if form.is_valid():
#            print(form.cleaned_data)
             #form.save()
             #return redirect('home')
#    else:
#        form = AddPostForm()
#    return render(request, 'product/addpage.html', {'form': form, 'menu': menu, 'title': 'Добавление статьи'})
def addpage(request):
    if request.method == 'POST':        # это дает возврат заполненных полей
        form = AddPostForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            try:
                Products.objects.create(**form.cleaned_data)
                return redirect('home')
            except:
                form.add_error(None, "Ошибка добавления поста")
    else:
        form = AddPostForm()
    return render(request, 'products/addpage.html', {'form': form, 'menu': menu, 'title': 'Добавление статьи'})

def contact(request):
    return render(request, 'products/contact.html', {'menu': menu, 'title': 'Мы с вами свяжемся'})


def login(request):
    return HttpResponse("Авторизация")


def pegeNotFound(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')


def show_post(request, post_slug):
    post = get_object_or_404(Products, slug=post_slug)

    context = {
        'post': post,
        'menu': menu,
        'title': post.title,
        'cat_selected': post.cat_id,
    }
    return render(request, 'products/post.html', context=context)


def show_category(request, cat_id):
    posts = Products.objects.filter(cat_id=cat_id)
    # cats = Category.objects.all()
    # если пост отсутствует, выводит 404:
    if len(posts) == 0:
        raise Http404()

    context = {
        'posts': posts,
        # 'cats': cats,
        'menu': menu,
        'title': 'Отображение по категориям',
        'cat_selected': cat_id,
    }

    return render(request, 'products/index.html', context=context)
