from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from motelcasino.models import Room
import datetime

room_numbers = [102, 103, 104, 105]

style = {
    102 : "2LS",
    103 : "1LS",
    104 : "2L",
    105 : "1L"
}

score = {
    102 : 3,
    103 : 4,
    104 : 1,
    105 : 2
}

def preprocessDates(date : str, start=False):
    date = date.split('-')
    date = list(map(int, date))
    if start: return datetime.datetime(date[0], date[1], date[2], 14, 30, 0)
    return datetime.datetime(date[0], date[1], date[2], 11, 30, 0)

def make_naive(datetime):  #remove timezone from datetime
    return datetime.replace(tzinfo=None)

def fetch(room_number):
    query = Room.objects.values("checkin", "checkout").filter(room_number__exact=room_number)
    return list(map(lambda x: (x["checkin"], x["checkout"]), query))


def rooms_available(request):
    startDate = preprocessDates(request.GET["startDate"], start=True)
    endDate = preprocessDates(request.GET["endDate"], start=False)
    free = []
    for room_number in room_numbers:
        times = fetch(room_number)
        room_number_is_free = True
        for checkin, checkout in times:
            checkin, checkout = make_naive(checkin), make_naive(checkout)
            if max(startDate, checkin) < min(endDate, checkout):    #I'm checking if the interval of intersection is valid.
                room_number_is_free = False
        if room_number_is_free: free.append(room_number)
    #free = [102,103,104,105]
    response = []
    for nn in free:
        response.append({"room_number":nn, "style":style[nn], "score":score[nn]})
    return JsonResponse(response, safe=False)

def book(request):
    name, room_number, checkin, checkout = request.GET["name"], request.GET["room_number"], request.GET["checkin"], request.GET["checkout"]
    checkin, checkout = preprocessDates(checkin, start=True), preprocessDates(checkout, start=False)
    room = Room(name=name, room_number=room_number, checkin=checkin, checkout=checkout)
    room.save()
    return HttpResponse("room booked successfully")
