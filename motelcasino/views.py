from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from motelcasino.models import Room
from django.views.decorators.csrf import csrf_exempt
import datetime, json

room_numbers = [102, 103, 104, 105]

style = {
    102 : "2 Simple Beds",
    103 : "1 Simple Bed",
    104 : "2 QueenSize Bed",
    105 : "1 QueenSize Bed"
}

score = {
    102 : "***",
    103 : "****",
    104 : "*",
    105 : "**"
}

def preprocessDates(date : str, start=False):
    date = date.split('-')
    date = list(map(int, date))
    if start: return datetime.datetime(date[0], date[1], date[2], 14, 30, 0)
    return datetime.datetime(date[0], date[1], date[2], 11, 30, 0)

def fetch(room_number):
    query = Room.objects.values("checkin", "checkout", "id").filter(room_number__exact=room_number)
    return list(map(lambda x: (x["checkin"], x["checkout"]), query))

def check_free_rooms(startDate, endDate, nBeds):
    free = []
    response = []
    for room_number in room_numbers:
        times = fetch(room_number)
        room_number_is_free = True
        for checkin, checkout in times:
            if max(startDate, checkin) < min(endDate, checkout):    #I'm checking if the interval of intersection is valid.
                room_number_is_free = False
        if room_number_is_free: free.append(room_number)
    free = list(filter(lambda x:int(style[x][0]) == int(nBeds), free))
    ids = list(range(len(free)))
    free = list(zip(free, ids))
    for nn,id in free:
        response.append({"room_number":nn, "style":style[nn], "score":score[nn], "id":id})
    response.sort(reverse=False, key=lambda x:len(x["score"]))
    return response

def rooms_available(request):
    startDate = preprocessDates(request.GET["startDate"], start=True)
    endDate = preprocessDates(request.GET["endDate"], start=False)
    nBeds = request.GET["nBeds"]
    response = check_free_rooms(startDate, endDate, nBeds)
    return JsonResponse(response, safe=False)

@csrf_exempt
def book(request):
    data = json.loads(request.body.decode('utf-8'))
    name, room_number = data["name"], int(data["roomNumber"])
    checkin, checkout = preprocessDates(data["startDate"], start=True), preprocessDates(data["endDate"], start=False)

    freeRooms_JSON = check_free_rooms(checkin, checkout)
    available_rooms = list(map(lambda x:x["room_number"], freeRooms_JSON))

    if room_number in available_rooms:
        room = Room(name=name,room_number=room_number,checkin=checkin,checkout=checkout)
        room.save()
    else:
        return HttpResponse("Room is already full.")

    return HttpResponse("Room Booked Successfully.")

@csrf_exempt
def rooms_booked(request):
    today = datetime.datetime.today()
    query = Room.objects.values("id","room_number").filter(checkin__lte=today, checkout__gte=today)
    query = list(map(lambda x:(int(x["room_number"]),x["id"]), query))
    response = []
    for nn,id in query:
        response.append({"room_number":nn, "style":style[nn], "score":score[nn], "id":id})
    return JsonResponse(response, safe=False)


@csrf_exempt
def delete(request):
    data = json.loads(request.body.decode('utf-8'))
    id = int(data["id"])
    try:
        Room.objects.all().filter(id__exact=id).delete()
        return HttpResponse("Room freed successfully.")
    except:
        return HttpResponse("Something went wrong here.")
