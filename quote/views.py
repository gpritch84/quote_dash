from django.shortcuts import render,redirect
from .models import *
from django.contrib import messages
import bcrypt

def index(request):
    return render(request, 'index.html')

def register(request):
    if request.method == "POST":
#Check to see if register object is valid
        errors = User.objects.register_validator(request.POST)
        if len(errors) > 0:
            for k,v in errors.items():
                messages.error(request,v)
            return redirect('/')
#Check to see if email alread associated with an account
        user=User.objects.filter(email=request.POST['email'])
        if len(user) > 0:
            messages.error(request, "Email is already in use")
            return redirect('/')
        if request.POST['password'] == request.POST['con_pass']:
            hash1=bcrypt.hashpw(request.POST['password'].encode(),bcrypt.gensalt()).decode()
            User.objects.create(
                first_name=request.POST['first_name'],
                last_name=request.POST['last_name'],
                email=request.POST['email'],
                password=hash1
            )
            logged = User.objects.last()
            request.session['user_id'] = logged.id
            return redirect('/quotes')
    else:
        return redirect('/')

def login(request):
    if request.method == 'POST':
#validating the login object
        errors = User.objects.login_validator(request.POST)
        if len(errors) > 0:
            for k,v in errors.items():
                messages.error(request,v)
            return redirect('/')
#Checking if email is in database
        user=User.objects.filter(email=request.POST['login_email'])
        if len(user)==0:
            messages.error(request, "Invalid Email/Password")
            return redirect ('/')
#Checking if passwords match
        if not bcrypt.checkpw(request.POST['login_password'].encode(),user[0].password.encode()):
            messages.error(request, "Invalid Email/Password")
            return redirect ('/')
#Put UserID into session and redirect
        request.session['user_id']=user[0].id
        return redirect('/quotes')
    else:
        return redirect('/')    
    return redirect('/quotes')

def quotes(request):
    if 'user_id' not in request.session:
        return redirect('/')
    else: 
        context={
            'user' : User.objects.get(id=request.session['user_id']),
            'quotes' : Quote.objects.all()
        }
    return render(request, 'quotes.html', context)

def logout(request):
    if 'user_id' in request.session:
        del request.session['user_id']
    return redirect('/')

def user(request,id_from_route):
    context={
        'user':User.objects.get(id=id_from_route),
        'quote':Quote.objects.all()
    }
    return render(request, 'user.html', context)

def add_quote(request):
    if request.method == 'POST':
        errors = Quote.objects.quote_validator(request.POST)
        if len(errors) > 0:
            for k,v in errors.items():
                messages.error(request,v)
            return redirect('/quotes')
    user=User.objects.get(id=request.session['user_id'])
    Quote.objects.create(
        author=request.POST['author'],
        quote=request.POST['quote'],
        uploaded_by=user,
    )
    return redirect('/quotes')

def edit_account(request, id_from_route):
    context={
        'user' : User.objects.get(id=request.session['user_id'])
    }
    return render(request, 'edit_user.html',context)

def update_user(request,id_from_route):
    if request.method == 'POST':
        errors = User.objects.edit_validator(request.POST)
        if len(errors) > 0:
            for k,v in errors.items():
                messages.error(request,v)
            return redirect(f'/edit_account/{id_from_route}')
        update = User.objects.get(id=id_from_route)
        update.email = request.POST['edit_email']
        update.first_name = request.POST['edit_first_name']
        update.last_name = request.POST['edit_last_name']
        update.save()
    return redirect(f'/edit_account/{id_from_route}')

def delete_quote(request,id_from_route):
    delete = Quote.objects.get(id=id_from_route)
    delete.delete()
    return redirect('/quotes')

def like(request,quote_id,user_id):
    quote = Quote.objects.get(id=quote_id)
    user = User.objects.get(id=user_id)
    quote.users.add(user)
    return redirect('/quotes')