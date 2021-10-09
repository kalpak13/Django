from django.shortcuts import render, redirect
from django.http import HttpResponse
from . import models, forms


# Create your views here.
# rooms =[

#     {'id':1,'name':'room1'},
#     {'id':2,'name':'room2'},
#     {'id':3,'name':'room3'},
# ]


def Home(request):
    rooms = models.Room.objects.all()
    return render(request, 'base/home.html', {'rooms': rooms})


def Room(request, pk):
    room = models.Room.objects.get(id=pk)
    return render(request, 'base/room.html', {'room': room})


def create_room(request):
    form = forms.RoomForm()
    if request.method == 'POST':
        form = forms.RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    context = {'form': form}
    return render(request, 'base/room_form.html', context)


def update_room(request, pk):
    room = models.Room.objects.get(id=pk)
    form = forms.RoomForm(instance=room)
    if request.method == 'POST':
        form = forms.RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')
    context = {'form': form}
    return render(request, 'base/room_form.html', context)


def delete_room(request, pk):
    room = models.Room.objects.get(id=pk)
    if request.method == 'POST':
        room.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj1': room})
