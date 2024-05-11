from django.shortcuts import render, redirect
from django.contrib import messages
# Create your views here.

from .models import Room


def home(request):
    if request.method == 'POST':
        room_id = request.POST.get('room_id')
        player_name = request.POST.get('player_name')
        print(room_id, player_name)
        if not room_id:
            room = Room.objects.create()
            return redirect(f"game/{room.id}/{player_name}")
        else:
            try:
                room = Room.objects.get(pk=room_id)
                return redirect(f"game/{room_id}/{player_name}")
            except Room.DoesNotExist:
                messages.error(request, "Enter valid room_id")
    return render(request, 'home.html')


def game(request, id=None, name=None):
    room_exist = Room.objects.filter(pk=id).exists()
    print(room_exist)
    if not room_exist:
        messages.error(request, "Enter valid room_id!! You Fool!!")
        return redirect('home')
    context = {
        'name': name,
        'room_id': id,
    }
    return render(request, 'game.html', context=context)
