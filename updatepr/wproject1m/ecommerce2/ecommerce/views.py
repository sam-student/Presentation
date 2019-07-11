from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, get_user_model
from django.contrib.auth.models import User
from django.contrib.auth import logout

from .forms import ContactForm




def logout_view(request):
    logout(request)
    # Redirect to a success page.
    return redirect("/home")

def home_page(request):
    #print(request.session.get("first_name", "Unknown"))
    #if request.user.is_authenticated

    context = {
        "title":"Home Page",
        "content": "Description of home_page",
        "premium-content":"YEAHHH"
    }
    if request.user.is_authenticated:
        context["premium_content"] = "YEAHHHHH"
    return render(request, "home_page.html", context)

def cart_page(request):
    #print(request.session.get("first_name", "Unknown"))
    #if request.user.is_authenticated

    return render(request, "home.html")

def about_page(request):
    context = {
        "title": "About",
        "content": "Descirption of about_page"
    }
    return render(request, "about_page.html", context)

def contact_page(request):
    contact_form = ContactForm(request.POST or None)
    context = {
        "title": "Contact Us",
        "content": "Welcome to the contact_page",
        "form": contact_form,
    }

    if contact_form.is_valid():
        print(contact_form.cleaned_data)
    #if request.method == "POST":
    #    print(request.POST)
    #    print(request.POST.get("fullname"))
    #    print(request.POST.get("email"))
    #    print(request.POST.get("content"))
    return render(request, "Contact/view.html", context)

# def login_page(request):
#     form = LoginForm(request.POST or None)
#     context = {
#         "form": form
#     }
#     print("user logged in")
#     #print(request.user.is_authenticated)
#     if form.is_valid():
#         print(form.cleaned_data)
#         #context["form"] = LoginForm
#
#
#         username = form.cleaned_data.get("username")
#         password = form.cleaned_data.get("password")
#
#         user = authenticate(request, username= username , password= password)
#         print(user)
#         #print(request.user.is_authenticated)
#
#         if user is not None:
#             #print(request.user.is_authenticated)
#             login(request, user)
#             # Redirect to a success page.
#             #context['login_form'] = LoginForm()
#             return redirect("/login")
#         else:
#             # Return an 'invalid login' error message.
#             print("error")
#             #print("hello")
#     return render(request, "auth/login.html" , context)
#
# User = get_user_model()
# def register_page(request):
#     form = RegisterForm(request.POST or None)
#     context = {
#         "form": form
#     }
#
#     if form.is_valid():
#         print(form.cleaned_data)
#         username = form.cleaned_data.get("username")
#         email = form.cleaned_data.get("email")
#         password = form.cleaned_data.get("password")
#         new_user = User.objects.create_user(username, email, password)
#         print(new_user)
#     return render(request, "auth/register.html" ,context)


def home_page_old(request):
    html_ ="""
    <!doctype html>
<html lang="en">
  <head>
    <!-- Required meta tags -->
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">

    <!-- Bootstrap CSS -->
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css" integrity="sha384-MCw98/SFnGE8fJT3GXwEOngsV7Zt27NXFoaoApmYm81iuXoPkFOJwJ8ERdknLPMO" crossorigin="anonymous">

    <title>Hello, world!</title>
  </head>
  <body>
    <div class='text-center'>
    <h1>hello how are you i am fine  ok then!</h1>
    </div>
    <!-- Optional JavaScript -->
    <!-- jQuery first, then Popper.js, then Bootstrap JS -->
    <script src="https://code.jquery.com/jquery-3.3.1.slim.min.js" integrity="sha384-q8i/X+965DzO0rT7abK41JStQIAqVgRVzpbzo5smXKp4YfRvH+8abtTE1Pi6jizo" crossorigin="anonymous"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.3/umd/popper.min.js" integrity="sha384-ZMP7rVo3mIykV+2+9J3UJ46jBk0WLaUAdn689aCwoqbBJiSnjAK/l8WvCWPIPm49" crossorigin="anonymous"></script>
    <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/js/bootstrap.min.js" integrity="sha384-ChfqqxuZUCnJSK3+MXmPNIyE6ZbWh2IMqE241rYiqJxyMiZ6OW/JmZQ5stwEULTy" crossorigin="anonymous"></script>
  </body>
</html>
    """
    return HttpResponse(html_) #we can also use heading tags or css tags in this HttpResponse function