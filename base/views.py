from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
rooms =[

    {'id':1,'name':'room1'},
    {'id':2,'name':'room2'},
    {'id':3,'name':'room3'},
]


def Home(request):
    return render(request,'base/home.html',{'rooms':rooms})

def Room(request,pk):
    room=None
    for i in rooms:
        if i['id']==int(pk):
            room=i
          


    return render(request,'base/room.html',{'room':room})