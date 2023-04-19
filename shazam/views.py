from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse

from .models import Room,Topic,Message,User,privatechat
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from .forms import Roomform,updateuser,MyUserCreationForm
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.core import serializers

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
    topics=Topic.objects.all()[0:5]
    
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

@login_required(login_url='login_page')
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
    if request.user!=None:
        room.participants.add(request.user)
    context={'chatboxes':chatboxes,'room':room,'participants':participants}
    return render(request,'shazam/room.html',context)
def inbox(request,pk):
    users=User.objects.get(id=pk)
    context={'participants':users}
    return render(request,'shazam/chat.html',context)
def direct(request,pk):
    user=User.objects.get(id=pk)
    #chatboxes=user.privatechat__set.all().orderby('-updated')
    
    if request.method=="POST":
        chat=privatechat.objects.create(user=user,
                                    Host=request.user,
                                    body=request.POST.get('body')
                                    
                                    )
        return redirect('direct',pk=pk)
    chatboxes = privatechat.objects.filter((Q(user=user) & Q(Host=request.user)) | (Q(user=request.user) & Q(Host=user))).order_by('updated')
    context={'chatboxes':chatboxes,'user':user}
    return render(request,'shazam/chat.html',context)
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
    topics=Topic.objects.all()
    if request.user!=update.Host:
        return HttpResponse("you are not allowed")
    if request.method=="POST":
        topic_name=request.POST.get('topic')
        topic,created=Topic.objects.get_or_create(name=topic_name)
        update.name=request.POST.get('name')
        update.Topic=topic
        update.description=request.POST.get('description')
        update.save()
        return redirect('/')
            
    return render(request,'shazam/roomform.html',{'room':update,'form':room,'topics':topics})
def followToggle(request, author):
    authorObj = User.objects.get(username=author)
    currentUserObj = User.objects.get(username=request.user.username)
    following = authorObj.following.all()

    if author != currentUserObj.username:
        if currentUserObj in following:
            authorObj.following.remove(currentUserObj.id)
        else:
            authorObj.following.add(currentUserObj.id)

    return HttpResponseRedirect(reverse(profile_page, args=[authorObj.id]))
@login_required(login_url='login_page')

def delete(request,pk):
    delete=Room.objects.get(id=pk)
    if request.user != delete.Host:
        return HttpResponse("you are not allowed")
    if request.method == 'POST':
        delete.delete()
        return redirect('home')
    return render(request,'shazam/delete.html',{'obj':delete})
@login_required(login_url='login_page')
def deletemsg(request,pk):
    chatroom=Message.objects.get(id=pk)
    if request.user!=chatroom.user:
        return HttpResponse("you are not allowed")
    if request.method == 'POST':
        chatroom.delete()
        return redirect('home')
  
    return render(request,'shazam/delete.html',{'obj':chatroom})

@login_required(login_url='login_page')
def deletechat(request,pk):
    chatroom=privatechat.objects.get(id=pk)
    if request.user!=chatroom.Host:
        return HttpResponse("you are not allowed")
    
    chatroom.delete()
    return redirect('inbox/'+str(chatroom.user.id))
  
    #return render(request,'shazam/delete.html',{'obj':chatroom})

    

def login_page(request):
    page="login"
    if request.method=="POST":
        username=request.POST.get("email").lower()
        password=request.POST.get("password")
        print(username,password)
        try:
            username=User.objects.get(username=username)
        except:
            messages.error(request, '')
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
    register=MyUserCreationForm()
    if request.method=="POST":
        #register=UserCreationForm(commit=False)
        register=MyUserCreationForm(request.POST)
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
@login_required(login_url='login_page')
def updateUser(request):
    user=request.user
    form= updateuser(instance=user)
    if request.method == 'POST':
        form=updateuser(request.POST,request.FILES,instance=user)
        if form.is_valid():
            form.save()
            return redirect('profile_page',pk=user.id)
        
    return render(request,'shazam/update-user.html',{'form':form})
def topics(request):
    k=request.GET.get("q") if request.GET.get('q')!=None else ''

    topics=Topic.objects.filter(
                             Q(name__icontains=k)
                             
                             )
    return render(request,'shazam/topics.html',{'topics':topics})
def activity(request):
    chatboxes=Message.objects.all()
    return render(request,'shazam/activity.html',{'chatboxes':chatboxes})

def more(request):
    return render(request,'shazam/more.html')