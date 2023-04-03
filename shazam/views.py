from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import Room,Topic,Message
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from .forms import Roomform
from django.db.models import Q

# Create your views here.
l=[
    {'id':1, 'name':"learn python"},
    {'id':2, 'name':"learn js"},
    {'id':3, 'name':"learn java"}

]

def home(request):
    k=request.GET.get("q") if request.GET.get('q')!=None else ''
    room=Room.objects.filter(Q(Topic__name__icontains=k)|
                             Q(name__icontains=k)|
                             Q(description__icontains=k)
                             ).order_by('-updated')
    topics=Topic.objects.all()
    
    room_count=room.count()
    chatboxes=Message.objects.filter(Q(room__Topic__name__icontains=k)).order_by("-created")
    context={'rooms':room,'topics':topics,'room_count':room_count,'chatboxes':chatboxes}
    return render(request,'shazam/home.html',context)
def profile_page(request,pk):
    users=User.objects.get(id=pk)
    rooms=users.room_set.all()
    chatboxes=users.message_set.all()
    topics=Topic.objects.all()
    context={'users':users,'rooms':rooms,'chatboxes':chatboxes,'topics':topics}
    return render (request,'shazam/profile_page.html',context)


def room(request,pk):
    room=Room.objects.get(id=pk)
    chatboxes=room.message_set.all().order_by('-updated')
    participants=room.participants.all()
    if request.method=="POST":
        chat=Message.objects.create(user=request.user,
                                    room=room,
                                    body=request.POST.get('body')
                                    
                                    )
        return redirect('room',pk=room.id)
    room.participants.add(request.user)
    context={'chatboxes':chatboxes,'room':room,'participants':participants}
    return render(request,'shazam/room.html',context)
@login_required(login_url='login_page')
def createroom(request):
    room=Roomform()
    topics=Topic.objects.all()
    if request.method == "POST":
        topic_name=request.POST.get('topic')
        topic,created=Topic.objects.get_or_create(name=topic_name)
        Room.objects.create(
            Host=request.user,
            Topic=topic,
            name=request.POST.get('name'),
            description=request.POST.get('description'),
        )
        return redirect('/')
    return render(request,'shazam/roomform.html',{'form':room,'topics':topics})
@login_required(login_url='login_page')

def updateroom(request,pk):
    update=Room.objects.get(id=pk)
    room=Roomform(instance=update) 
    if request.user!=update.Host:
        return HttpResponse("you are not allowed")
    if request.method=="POST":
        topic_name=request.POST.get('topic')
        topic,created=Topic.objects.get_or_create(name=topic_name)
        room.name=request.POST.get('name')
        room.Topic=topic
        room.description=request.POST.get('description')
        room.save()
        return redirect('/')
            
    return render(request,'shazam/roomform.html',{'room':room})
@login_required(login_url='login_page')

def delete(request,pk):
    delete=Room.objects.get(id=pk)
    if request.user != delete.Host:
        return HttpResponse("you are not allowed")
    delete.delete()
    return redirect('/')
@login_required(login_url='login_page')
def deletemsg(request,pk):
    chatroom=Message.objects.get(id=pk)
    if request.user!=chatroom.user:
        return HttpResponse("you are not allowed")
    chatroom.delete()
    return redirect('/')

def login_page(request):
    page="login"
    if request.method=="POST":
        username=request.POST.get("username").lower()
        password=request.POST.get("password")
        try:
            username=User.objects.get(username=username)
        except:
            messages.error(request, 'user not found')
        user=authenticate(request,username=username,password=password)
        print(type(user))

        if user is not None:
            login(request,user)
            return redirect('/')
        else:
            messages.error(request, 'user or password not found')
    context={'page':page}
            
            
            
    return render(request, 'shazam/login_page.html',context)
def logout_page(request):
    logout(request)
    return redirect('/')
def signup(request):
    register=UserCreationForm()
    if request.method=="POST":
        #register=UserCreationForm(commit=False)
        register=UserCreationForm(request.POST)
        if register.is_valid():
            user=register.save(commit=False)
            user.username=user.username.lower()
            user.save()
            login(request,user)
 
            return redirect('home')
        else:
            messages.error(request,"please register with valid details")
    context={'register':register}
    return render(request,'shazam/login_page.html',context)