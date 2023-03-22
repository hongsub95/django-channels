from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpRequest,HttpResponse

from chat.forms import RoomForm
from chat.models import Room

# Create your views here.

def index(request):
    room_qs = Room.objects.all()
    return render(request,'chat/index.html',{
        "room_qs":room_qs
    })

def room_chat(request:HttpRequest,room_pk:str) -> HttpResponse:
    room = get_object_or_404(Room,pk = room_pk)
    return render(request,'chat/room_chat.html',{
        "room":room
    })

def room_new(request):
    if request.method == "POST":
        form = RoomForm(request.POST)
        if form.is_valid():
            created_room = form.save()
            return redirect('chat:room_chat',created_room.pk)
    else:
        form = RoomForm()
        return render(request,'chat/room_form.html',{'form':form})
    