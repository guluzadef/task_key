from django.contrib import messages
from django.contrib.auth import authenticate
from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from base_user.forms import MyUserCreationForm
from base_user.models import MyUser
from todo_app.forms import LoginForm, AddKey, ChangeKey
from todo_app.models import Key, choices
from django.core.paginator import Paginator
import logging
from .tasks import addkey_mail, deletekey_mail, updatekey_mail

# Get an instance of a logger
format_string = '%(levelname)s: %(asctime)s: %(message)s'
logging.basicConfig(filename='test.log', level=logging.DEBUG, format=format_string)


def index(request):
    context = {}
    return render(request, 'index.html')


def register(request):
    context = {}
    form = MyUserCreationForm
    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.save()
            logging.info(f'{user} is Registered')
            return redirect('index')
        else:
            logging.warning(form.errors)
            messages.error(request, form.errors)
    context['form'] = form

    return render(request, 'log-reg/register.html', context)


def login(request):
    context = {}
    form = LoginForm
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            print(user)
            if user:
                auth_login(request, user)
                logging.info(f"Loginned id:{user.id},username={user},email={user.email}")
                return redirect('/')
            else:
                messages.error(
                    request, "Username or Password inValid"
                )

    context['form'] = form
    return render(request, 'log-reg/login.html', context)


def logout_view(request):
    logging.info(f"{request.user} Logout")

    logout(request)
    return redirect("index")


@login_required
def addkey(request):
    context = {}
    context['form'] = AddKey()

    if request.method == "POST":
        form = AddKey(request.POST)
        if form.is_valid():
            article = form.save(commit=False)
            article.username = request.user
            logging.info(f'{article} added from {article.username}')
            article.save()
            addkey_mail.delay(article.username.email, article.type)

            print(article, 'SAVED')

            return redirect('/')
        else:
            messages.error(request, form.errors)
            logging.warning(form.errors)

    return render(request, 'addkey/key.html', context)


def myfiles(request, id):
    context = {}
    user = MyUser.objects.filter(id=id).last()

    context['user'] = user
    key = Key.objects.filter(username_id=user.id).all()
    pagination = Paginator(key, 5)
    context["key"] = pagination.get_page(request.GET.get('page', 1))
    context["page_range"] = pagination.page_range
    return render(request, 'myfiles/file.html', context)


def search(request):
    context = {}
    if "q" in request.GET:
        query = request.GET.get('q')
        print(query)
        results = Key.objects.filter(
                        Q(type__icontains=query) |
                        Q(host__icontains=query) |
                        Q(port__icontains=query) |
                        Q(user__icontains=query)
        )
        print(results)
        p = Paginator(results, 10)
        page_number = request.GET.get('page')
        page_obj = p.get_page(page_number)
        context["page_range"] = p.page_range

        context['key'] = page_obj
    return render(request, 'search/search.html', context)


def update_key(request, id):
    context = {}
    key = Key.objects.filter(id=id).last()
    context['key'] = key
    context['form'] = ChangeKey(instance=key)
    if request.method == 'POST':
        form = ChangeKey(request.POST, instance=key)
        if form.is_valid():
            logging.info(f"{request.user} is updated {key}")
            form.save()
            updatekey_mail.delay(key.username.email, key.type)

            return redirect('/')

        else:
            print(form.errors)

    return render(request, 'update/update.html', context)


def delete_key(request, id):
    key = Key.objects.filter(id=id).last()
    if key:
        logging.info(f'{request.user} Deleted {key}')
        key.delete()
        deletekey_mail.delay(key.username.email, key.type)
        return redirect('/')
