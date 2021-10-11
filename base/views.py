from django.shortcuts import render, redirect
from django.db.models import Q
from django.http import HttpResponse
from . import models, forms
from django.contrib.auth.models import User
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
        username=request.POST.get('username')
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
    context = {'login':page}
    return render(request, 'base/login_register.html', context)

def logout_user(request):
    logout(request)
    return redirect('home')

def Home(request):
    q = request.GET.get('q')
    # q=request.GET.get('q') if request.GET.get('q')!=None else ''
    rooms = None
    if q == None:
        rooms = models.Room.objects.all()
    else:
        # rooms = models.Room.objects.filter(topic__name=q)
        # rooms = models.Room.objects.filter(topic__name__icontains=q)
        rooms = models.Room.objects.filter(Q(topic__name__icontains=q) |
                                           Q(name__icontains=q) |
                                           Q(description__icontains=q)
                                           )
        #containts means the topic name should atleadt contain that string and i  is for to remove case sensi
    room_count = rooms.count()
    topics = models.Topic.objects.all()
    return render(request, 'base/home.html', {'rooms': rooms, 'topics': topics, 'room_count': room_count})


def Room(request, pk):
    room = models.Room.objects.get(id=pk)
    return render(request, 'base/room.html', {'room': room})

@login_required(login_url='login')
def create_room(request):
    form = forms.RoomForm()
    if request.method == 'POST':
        form = forms.RoomForm(request.POST)
        if form.is_valid():
            form.save()
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
