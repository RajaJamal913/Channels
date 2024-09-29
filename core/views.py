from django.shortcuts import render

def room(request, room_name):
    return render(request, 'templates/room.html', {
        'room_name': room_name
    })
