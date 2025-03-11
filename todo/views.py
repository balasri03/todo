from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from todo import models
from todo.models import TODO
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
def signup(request):
    if request.method=='POST':
        fnm=request.POST.get('fnm')
        emailid=request.POST.get('email')
        password=request.POST.get('pwd')
        my_user=User.objects.create_user(fnm,emailid,password)
        my_user.save()
        return redirect('/login')
    return render(request,'signup.html')
def user_login(request):
    if request.method=='POST':
        fnm=request.POST.get('fnm')
        pwd=request.POST.get('pwd')
        print(fnm,pwd)
        user=authenticate(request,username=fnm,password=pwd)
        if user is not None:
            login(request,user)
            return redirect('/todopage')
        else:
            return redirect('/login')
    return render(request,'login.html')
@login_required(login_url='/login')
def todo(request):
    if request.method=='POST':
        title=request.POST.get('title')
        print(title)
        obj=models.TODO(title=title,user=request.user)#her user=request.user means it show the task of specific login user
        obj.save()
        res=models.TODO.objects.filter(user=request.user).order_by('date')
        return redirect('/todopage',{'res':res})
    res=models.TODO.objects.filter(user=request.user).order_by('date')
    return render(request,'todo.html',{'res':res})#curly braces means it is object
@login_required(login_url='/login')
def edit_todo(request,srno):
    if request.method=='POST':
        title=request.POST.get('title')
        print(title)
        obj=models.TODO.objects.get(srno=srno)
        obj.title=title
        obj.save()
        user=request.user
        return redirect('/todopage',{'obj':obj})
    obj=models.TODO.objects.get(srno=srno)
    return render(request,'todo.html',{'obj':obj})
@login_required(login_url='/login')
def delete_task(request,srno):
    obj=models.TODO.objects.get(srno=srno)
    obj.delete()
    return redirect('/todopage')
def signout(request):
    logout(request)
    return redirect('/login')
