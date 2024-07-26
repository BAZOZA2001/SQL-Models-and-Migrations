from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Flight, Passenger

def index(request):
    return render(request, "flights/index.html", {
        "flights": Flight.objects.all()
    })

def flight(request, flight_id):
    flight = get_object_or_404(Flight, pk=flight_id)
    non_passengers = Passenger.objects.exclude(flights=flight).all()
   
    # Log non_passengers to the console
    print("Non-passengers:")
    for passenger in non_passengers:
        # Adjust the field names according to your Passenger model
        print(f"ID: {Passenger.id}, First Name: {Passenger.first}, Last Name: {Passenger.last}")
   
    return render(request, "flights/flight.html", {
        "flight": flight,
        "passengers": flight.passengers.all(),
        "non_passengers": non_passengers
    })

def book(request, flight_id):
    flight = get_object_or_404(Flight, pk=flight_id)
    
    if request.method == "POST":
        print("POST data:", request.POST)  # Debugging line
        passenger_id = request.POST.get("passenger")
        print("Passenger ID from form:", passenger_id)  # Debugging line
        
        if passenger_id:
            passenger = get_object_or_404(Passenger, pk=int(passenger_id))
            passenger.flights.add(flight)
            return redirect("flight", flight_id=flight.id)
        else:
            non_passengers = Passenger.objects.exclude(flights=flight).all()
            print("Non-passengers:", list(non_passengers))  # Debugging line
            return render(request, "flights/flight.html", {
                "flight": flight,
                "passengers": flight.passengers.all(),
                "non_passengers": non_passengers,
                "message": "No passenger selected 🤷‍♂️."
            })
    
    return redirect("flight", flight_id=flight.id)