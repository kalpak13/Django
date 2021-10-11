from django.shortcuts import render, redirect
from django.db.models import Q
from django.http import HttpResponse
from . import models, forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth  import authenticate, login,logout
from django.contrib.auth.decorators import login_required



# Create your views here.
# rooms =[

#     {'id':1,'name':'room1'},
#     {'id':2,'name':'room2'},
#     {'id':3,'name':'room3'},
# ]
##user auth
def login_page(request):
    page='login'
    if request.user.is_authenticated:
        return redirect('home')



    if request.method=='POST':
        username=request.POST.get('username').lower()
        password=request.POST.get('password')
        try:
            user=User.objects.get(username=username)
            user=authenticate(request,username=username,password=password)
            if user is not None:
                login(request,user)
                return redirect('home')
            else:
                messages.error(request, 'invalid Credentials')
        except:
            messages.error(request, 'user does not exist')
    context = {'page':page}
    return render(request, 'base/login_register.html', context)

def logout_user(request):
    logout(request)
    return redirect('home')

def register_user(request):
    page='register'
    form=UserCreationForm()
    if request.method=='POST':
        form=UserCreationForm(request.POST)
        if form.is_valid():
            user=form.save(commit=False)
            user.username=user.username.lower()
            user.save()
            login(request,user)
            return redirect('home')
        else:
            messages.error(request,'registration failed...try sometime later')
            
    context={'page':page,'form':form}
    return render(request,'base/login_register.html',context)

def Home(request):
    # q = request.GET.get('q')
    q=request.GET.get('q') if request.GET.get('q')!=None else ''
    #q is topic name therfore we need to match it with topic name only
    # rooms = None
  
    # if q == None:
    #     rooms = models.Room.objects.all()
        
        
    # else:
    #     # rooms = models.Room.objects.filter(topic__name=q)
    #     # rooms = models.Room.objects.filter(topic__name__icontains=q)
    #     rooms = models.Room.objects.filter(Q(topic__name__icontains=q) |
    #                                        Q(name__icontains=q) |
    #                                        Q(description__icontains=q)
    #                                        )
                                         
        #containts means the topic name should atleadt contain that string and i  is for to remove case sensi
    rooms = models.Room.objects.filter(Q(topic__name__icontains=q) |
                                       Q(name__icontains=q) |
                                       Q(description__icontains=q)
                                      )
    room_count = rooms.count()
    topics = models.Topic.objects.all()
    # room_messages=models.Message.objects.all()
    room_messages=models.Message.objects.filter(Q(room__topic__name__icontains=q))
    return render(request, 'base/home.html', {'rooms': rooms, 'topics': topics, 'room_count': room_count,'room_messages':room_messages})


def Room(request, pk):
    room = models.Room.objects.get(id=pk)
    # messages=models.Message.objects.filter(room=room)
    messages=room.message_set.all().order_by('-created')
    #to query the child models we specify the name of the child models_set.all() to get the all of the child models
    participants=room.participants.all()
    if request.method=='POST':
        messgage=models.Message.objects.create(user=request.user,
                                               room=room,
                                               body=request.POST.get('body')
                                               )
        room.participants.add(request.user)
        return redirect('room',pk=room.id)#because it is post request therfore we need to get back to the page with a get request
                            
    
    return render(request, 'base/room.html', {'room': room,'room_messages':messages,'participants':participants})


def user_profile(request,pk):
    user=models.User.objects.get(id=pk)
    room_messages=user.message_set.all()
    topics=models.Topic.objects.all()
    rooms=user.room_set.all()
    context={'user':user,'rooms':rooms,'room_messages':room_messages,'topics':topics}
    return render(request,'base/profile.html',context)

@login_required(login_url='login')
def create_room(request):
    form = forms.RoomForm()
    if request.method == 'POST':
        form = forms.RoomForm(request.POST)
        if form.is_valid():
            room=form.save(commit=False)
            room.host=request.user
            # room.participants.add(request.user)
            room.save()     
            
           
            return redirect('home')
    context = {'form': form}
    return render(request, 'base/room_form.html', context)

@login_required(login_url='login')
def update_room(request, pk):
    room = models.Room.objects.get(id=pk)
    form = forms.RoomForm(instance=room)
    if request.user !=room.host:
        return HttpResponse("you are not allowed here!!")



    if request.method == 'POST':
        form = forms.RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')
    context = {'form': form}
    return render(request, 'base/room_form.html', context)

@login_required(login_url='login')
def delete_room(request, pk):
    room = models.Room.objects.get(id=pk)
    if request.user !=room.host:
        return HttpResponse("you are not allowed here!!")

    if request.method == 'POST':
        room.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj1': room})


@login_required(login_url='login')
def delete_comment(request, pk):
    message = models.Message.objects.get(id=pk)
    if request.user !=message.user:
        return HttpResponse("you are not allowed here!!")

    if request.method == 'POST':
        message.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj1': message})