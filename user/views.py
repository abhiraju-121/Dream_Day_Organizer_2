from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.models import AbstractUser
from . models import User as CustomUser
from django.contrib import messages
from django.http import HttpResponseForbidden
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from . models import Event,BookEvent,ServiceAvailability,VenueBooking,Venue,TransportationBooking,TransportationService,CateringBooking,CateringService,DecorationsBooking,DecorationsService,PhotographyBooking,PhotographyService,BridalGroomService,BridalGroomServiceBooking,Payment
from datetime import datetime
from service_provider.models import  ServiceProvider
from datetime import date
import stripe
import random
import string
from django.conf import settings
# Create your views here.


stripe.api_key = settings.STRIPE_SECRET_KEY

def base(request):
    return render(request,'index.html')
def home(request):
    return render(request,'home.html')




def register_user(request):
    if request.method == "POST":
        username=request.POST.get('username')
        email=request.POST.get('email')
        password=request.POST.get('password')
        confirm_password=request.POST.get('confirm_password')
        phone=request.POST.get('phone')

        if not username or not email or not password or not confirm_password or not phone:
            messages.error(request,'All feild require')
            return redirect('user_register')
        if CustomUser.objects.filter(email=email).exists():
            messages.error(request,"Email already exists !!")
            return redirect('user_register')
        if confirm_password!=password:
            messages.error(request,"Enter passowrd properly !!")
            return redirect('user_register')
        
        if len(phone)!= 10:
            messages.error(request,"Phone number must be 10 numbers !!")
            return redirect('user_register')
        
        user=CustomUser.objects.create_user(username=username,email=email,password=password)
        user.phone=phone
        user.save()
        return redirect('user_login')
    else:
        messages.error(request,'Something went wrong ')
    return render(request,'user_register.html')

def login_user(request):
    if request.method == "POST":
        email=request.POST.get('email')
        password=request.POST.get('password')
        
        user= authenticate(request,email=email,password=password)

        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.error(request,'Invalid email or Password ')
            return redirect('user_login')
    return render(request,'user_login.html')
        

def logout_user(request):
    logout(request)
    return redirect('/')

@login_required
def user_dashboard(request):
    return render(request,'user_dashboard.html')

@login_required
def user_profile(request):
    user=request.user
    if request.method =="POST":
        user.username=request.POST.get('email',user.username)
        user.phone=request.POST.get('phone',user.phone)
        user.email=request.POST.get('username',user.email)
        user.save()
    return render(request,'user_profile.html',{'user':user})

@login_required
def user_all_bookings(request):
    return render(request,"user_all_bookings.html")

## event ## 

@login_required
def user_event_list(request):
    events = Event.objects.all()
    return render(request, "user_event_list.html", {"events": events})

@login_required
def user_book_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)

    if request.method == "POST":
        event_date = request.POST.get("event_date")
        our_service = request.POST.get("our_service")
        customize = request.POST.get("customize")

        if date.fromisoformat(event_date) < date.today():
            messages.error(request, "You cannot book an event for a past date.")
            return redirect('book_event', event_id=event.id)

        is_booked = ServiceAvailability.objects.filter(
            service_type="Event",
            service_id=event.id,
            booked_date=event_date
        ).exists()

        if is_booked:
            messages.error(request, "This event is already booked on the selected date. Please choose another date.")
        else:
            BookEvent.objects.create(
                user=request.user,
                event=event,
                our_service=our_service,
                customize=customize,
                status="Pending"
            )

            ServiceAvailability.objects.create(
                service_type='Event',
                service_id=event.id,
                booked_date=event_date,
            )
            messages.success(request, "Event booked successfully. Awaiting approval.")

        return redirect("user_event_bookings")

    return render(request, "user_book_event.html", {"event": event})

@login_required
def user_event_bookings(request):
    bookings = BookEvent.objects.filter(user=request.user)
    return render(request, "user_bookings_event.html", {"bookings": bookings})

@login_required
def event_payment(request, booking_id):
    booking = get_object_or_404(BookEvent, id=booking_id, user=request.user)

    if booking.status != "Approved":
        messages.error(request, "You can only pay for approved bookings.")
        return redirect("user_event_bookings")

    provider = booking.event.service_provider
    amount = booking.event.price

    if request.method == "POST":
        transaction_id = ''.join(random.choices(string.ascii_letters + string.digits, k=10))

        Payment.objects.create(
            user=request.user,
            service_provider=provider,
            booking_type="event",
            booking_id=booking.id,
            amount=amount,
            transaction_id=transaction_id,
            status="paid",
        )

        booking.status = "Paid"
        booking.save()

        messages.success(request, "Payment successful! Your event booking is now confirmed.")
        return redirect("user_event_bookings")

    return render(request, "event_payment.html", {"booking": booking})

@login_required
def event_payment_status(request):
    user_payments = Payment.objects.filter(user=request.user)

    service_provider = ServiceProvider.objects.filter(user=request.user).first()
    provider_payments = Payment.objects.filter(service_provider=service_provider) if service_provider else None

    return render(request, "event_payment_status.html", {
        "user_payments": user_payments,
        "provider_payments": provider_payments
    })


## venu ##

@login_required
def venue_list(request):
    venues = Venue.objects.filter(available=True)
    return render(request, "user_venue.html", {"venues": venues})

@login_required
def book_venue(request, venue_id):
    venue = get_object_or_404(Venue, id=venue_id)

    if request.method == "POST":
        event_date = request.POST.get("event_date")
        venue_customize = request.POST.get("venue_customize")

        if date.fromisoformat(event_date) < date.today():
            messages.error(request, "You cannot book a venue for a past date.")
            return redirect('book_venue', venue_id=venue_id)

        is_booked = ServiceAvailability.objects.filter(
            service_type="Venue",
            service_id=venue.id,
            booked_date=event_date
        ).exists()

        if is_booked:
            messages.error(request, "This venue is already booked on the selected date. Please choose another date.")
        else:
            VenueBooking.objects.create(
                user=request.user,
                venue=venue,
                event_date=event_date,
                venue_customize=venue_customize,
                status="Pending"
            )

            ServiceAvailability.objects.create(
                service_type='Venue',
                service_id=venue.id,
                booked_date=event_date,
            )
            messages.success(request, "Venue booked successfully. Awaiting approval.")

        return redirect("user_bookings")

    return render(request, "book_venue.html", {"venue": venue})


@login_required
def user_bookings(request):
    bookings = VenueBooking.objects.filter(user=request.user)
    return render(request, "user_venue_bookings.html", {"bookings": bookings})

@login_required
def venue_payment(request, booking_id):
    booking = get_object_or_404(VenueBooking, id=booking_id, user=request.user)

    if booking.status != "Confirmed":
        messages.error(request, "You can only pay for confirmed bookings.")
        return redirect("user_bookings")

    provider = booking.venue.provider  
    amount = booking.venue.price

    if request.method == "POST":
        transaction_id = ''.join(random.choices(string.ascii_letters + string.digits, k=10))

        Payment.objects.create(
            user=request.user,
            service_provider=provider,
            booking_type="venue",
            booking_id=booking.id,
            amount=amount,
            transaction_id=transaction_id,
            status="paid",
        )


        booking.status = "Paid"
        booking.save()

        messages.success(request, "Payment successful! Your venue booking is now confirmed.")
        return redirect("user_bookings")

    return render(request, "venue_payment.html", {"booking": booking})

@login_required
def venue_payment_status(request):
    user_payments = Payment.objects.filter(user=request.user)

    service_provider = ServiceProvider.objects.filter(user=request.user).first()
    provider_payments = Payment.objects.filter(service_provider=service_provider) if service_provider else None

    return render(request, "venue_payment_status.html", {
        "user_payments": user_payments,
        "provider_payments": provider_payments
    })


## Transportation ##

def user_transportation_list(request):
    transport_services = TransportationService.objects.filter(available=True)
    return render(request, "user_transportation_list.html", {"transport_services": transport_services})

@login_required
def book_transportation(request, service_id):
    service = get_object_or_404(TransportationService, id=service_id)

    if request.method == "POST":
        event_date = request.POST.get("event_date")
        vehicle_type = request.POST.get("vehicle_type")
        seats = request.POST.get("seats")
        rent_car = request.POST.get("rent_car") == "on"

        if date.fromisoformat(event_date) < date.today():
            messages.error(request, "You cannot book transportation for a past date.")
            return redirect('book_transportation', service_id=service_id)

        is_booked = ServiceAvailability.objects.filter(
            service_type="Transportation",
            service_id=service.id,
            booked_date=event_date
        ).exists()

        if is_booked:
            messages.error(request, "This transportation service is already booked on the selected date.")
        else:
            TransportationBooking.objects.create(
                user=request.user,
                service=service,
                event_date=event_date,
                vehicle_type=vehicle_type,
                seats=seats,
                rent_car=rent_car,
                status="Pending"
            )

            ServiceAvailability.objects.create(
                service_type='Transportation',
                service_id=service.id,
                booked_date=event_date,
            )
            messages.success(request, "Transportation booked successfully. Awaiting approval.")

        return redirect("user_transport_bookings")

    return render(request, "user_book_transportation.html", {"service": service})

@login_required
def user_transport_bookings(request):
    bookings = TransportationBooking.objects.filter(user=request.user)
    return render(request, "user_transport_bookings.html", {"bookings": bookings})

@login_required
def transport_payment(request, booking_id):
    booking = get_object_or_404(TransportationBooking, id=booking_id, user=request.user)

    if booking.status != "Confirmed":
        messages.error(request, "You can only pay for confirmed bookings.")
        return redirect("user_transport_bookings")

    provider = booking.service.provider
    amount = booking.service.price

    if request.method == "POST":
        transaction_id = ''.join(random.choices(string.ascii_letters + string.digits, k=10))

        Payment.objects.create(
            user=request.user,
            service_provider=provider,
            booking_type="transport",
            booking_id=booking.id,
            amount=amount,
            transaction_id=transaction_id,
            status="paid",
        )

        booking.status = "Paid"
        booking.save()

        messages.success(request, "Payment successful! Your transportation booking is now confirmed.")
        return redirect("user_transport_bookings")

    return render(request, "transport_payment.html", {"booking": booking})

@login_required
def transportation_payment_status(request):
    user_payments = Payment.objects.filter(user=request.user, booking_type="transport")

    service_provider = ServiceProvider.objects.filter(user=request.user).first()
    provider_payments = Payment.objects.filter(service_provider=service_provider, booking_type="transport") if service_provider else None

    return render(request, "transport_payment_status.html", {
        "user_payments": user_payments,
        "provider_payments": provider_payments
    })



## caterning ##


def user_catering_list(request):
    caterings = CateringService.objects.filter(available=True)
    return render(request, "user_catering_list.html", {"caterings": caterings})


@login_required
def book_catering(request, catering_id):
    catering = get_object_or_404(CateringService, id=catering_id)

    if request.method == "POST":
        event_date = request.POST.get("event_date")
        guests = request.POST.get("guests")
        customize_food = request.POST.get("customize_food")

        if date.fromisoformat(event_date) < date.today():
            messages.error(request, "You cannot book catering for a past date.")
            return redirect('book_catering', catering_id=catering_id)

        is_booked = ServiceAvailability.objects.filter(
            service_type="Catering",
            service_id=catering.id,
            booked_date=event_date
        ).exists()

        if is_booked:
            messages.error(request, "This catering service is already booked on the selected date. Please choose another date.")
        else:
            CateringBooking.objects.create(
                user=request.user,
                service=catering,
                event_date=event_date,
                guests=guests,
                customize_food=customize_food,
                status="Pending"
            )

            ServiceAvailability.objects.create(
                service_type="Catering",
                service_id=catering.id,
                booked_date=event_date
            )

            messages.success(request, "Catering service booked successfully. Awaiting approval.")

        return redirect("user_catering_bookings")

    return render(request, "user_book_catering.html", {"catering": catering})


@login_required
def user_catering_bookings(request):
    bookings = CateringBooking.objects.filter(user=request.user)
    return render(request, "user_catering_bookings.html", {"bookings": bookings})


@login_required
def catering_payment(request, booking_id):
    booking = get_object_or_404(CateringBooking, id=booking_id, user=request.user)

    if booking.status != "Confirmed":
        messages.error(request, "You can only pay for confirmed bookings.")
        return redirect("user_bookings")

    provider = booking.service.provider
    amount = booking.service.price

    if request.method == "POST":
        transaction_id = ''.join(random.choices(string.ascii_letters + string.digits, k=10))

        Payment.objects.create(
            user=request.user,
            service_provider=provider,
            booking_type="catering",
            booking_id=booking.id,
            amount=amount,
            transaction_id=transaction_id,
            status="paid",
        )

        booking.status = "Paid"
        booking.save()

        messages.success(request, "Payment successful! Your catering booking is now confirmed.")
        return redirect("user_catering_bookings")

    return render(request, "catering_payment.html", {"booking": booking})


@login_required
def catering_payment_status(request):
    user_payments = Payment.objects.filter(user=request.user)

    service_provider = ServiceProvider.objects.filter(user=request.user).first()
    provider_payments = Payment.objects.filter(service_provider=service_provider) if service_provider else None

    return render(request, "catering_payment_status.html", {
        "user_payments": user_payments,
        "provider_payments": provider_payments
    })

## Decoration ##

def decoration_list(request):
    decorations = DecorationsService.objects.filter(available=True)
    return render(request, "user_decorations_list.html", {"decorations": decorations})


@login_required
def book_decoration(request, decoration_id):
    decoration = get_object_or_404(DecorationsService, id=decoration_id)

    if request.method == "POST":
        event_date = request.POST.get("event_date")
        custom_service = request.POST.get("custom_service")

        if date.fromisoformat(event_date) < date.today():
            messages.error(request, "You cannot book decorations for a past date.")
            return redirect("book_decoration", decoration_id=decoration_id)

        is_booked = ServiceAvailability.objects.filter(
            service_type="Decorations",
            service_id=decoration.id,
            booked_date=event_date
        ).exists()

        if is_booked:
            messages.error(request, "This decoration service is already booked on the selected date.")
        else:
            DecorationsBooking.objects.create(
                user=request.user,
                service=decoration,
                custom_service=custom_service,
                event_date=event_date,
                status="Pending"
            )

            ServiceAvailability.objects.create(
                service_type='Decorations',
                service_id=decoration.id,
                booked_date=event_date,
            )
            messages.success(request, "Decoration booked successfully. Awaiting approval.")

        return redirect("user_decorations_bookings")

    return render(request, "user_book_decoration.html", {"decoration": decoration})


@login_required
def user_decorations_bookings(request):
    bookings = DecorationsBooking.objects.filter(user=request.user)
    return render(request, "user_decorations_bookings.html", {"bookings": bookings})


@login_required
def decoration_payment(request, booking_id):
    booking = get_object_or_404(DecorationsBooking, id=booking_id, user=request.user)

    if booking.status != "Confirmed":
        messages.error(request, "You can only pay for confirmed bookings.")
        return redirect("user_decorations_bookings")

    provider = booking.service.provider
    amount = booking.service.price

    if request.method == "POST":
        transaction_id = ''.join(random.choices(string.ascii_letters + string.digits, k=10))

        Payment.objects.create(
            user=request.user,
            service_provider=provider,
            booking_type="decoration",
            booking_id=booking.id,
            amount=amount,
            transaction_id=transaction_id,
            status="paid",
        )

        booking.status = "Paid"
        booking.save()

        messages.success(request, "Payment successful! Your decoration booking is now confirmed.")
        return redirect("user_decorations_bookings")

    return render(request, "decoration_payment.html", {"booking": booking})


@login_required
def decoration_payment_status(request):
    user_payments = Payment.objects.filter(user=request.user, booking_type="decoration")

    service_provider = ServiceProvider.objects.filter(user=request.user).first()
    provider_payments = Payment.objects.filter(service_provider=service_provider, booking_type="decoration") if service_provider else None

    return render(request, "decoration_payment_status.html", {
        "user_payments": user_payments,
        "provider_payments": provider_payments
    })


## Photo&Video graphy ##

@login_required
def photography_list(request):
    services = PhotographyService.objects.filter(available=True)
    return render(request, "user_photography_list.html", {"services": services})


@login_required
def book_photography(request, photography_id):
    service = get_object_or_404(PhotographyService, id=photography_id)

    if request.method == "POST":
        event_date = request.POST.get("event_date")
        custom_service = request.POST.get("custom_service")

        if date.fromisoformat(event_date) < date.today():
            messages.error(request, "You cannot book photography for a past date.")
            return redirect("book_photography", photography_id=photography_id)

        is_booked = ServiceAvailability.objects.filter(
            service_type="Photography",
            service_id=service.id,
            booked_date=event_date
        ).exists()

        if is_booked:
            messages.error(request, "This photography service is already booked on the selected date.")
        else:
            PhotographyBooking.objects.create(
                user=request.user,
                service=service,
                custom_service=custom_service,
                event_date=event_date,
                status="Pending"
            )

            ServiceAvailability.objects.create(
                service_type='Photography',
                service_id=service.id,
                booked_date=event_date,
            )
            messages.success(request, "Photography booked successfully. Awaiting approval.")

        return redirect("user_photography_bookings")

    return render(request, "user_book_photography.html", {"service": service})

@login_required
def user_photography_bookings(request):
    bookings = PhotographyBooking.objects.filter(user=request.user)
    return render(request, "user_photography_bookings.html", {"bookings": bookings})

@login_required
def photography_payment(request, booking_id):
    booking = get_object_or_404(PhotographyBooking, id=booking_id, user=request.user)

    if booking.status != "Confirmed":
        messages.error(request, "You can only pay for confirmed bookings.")
        return redirect("user_photography_bookings")

    provider = booking.service.provider
    amount = booking.service.price

    if request.method == "POST":
        transaction_id = ''.join(random.choices(string.ascii_letters + string.digits, k=10))

        Payment.objects.create(
            user=request.user,
            service_provider=provider,
            booking_type="photography",
            booking_id=booking.id,
            amount=amount,
            transaction_id=transaction_id,
            status="paid",
        )

        booking.status = "Paid"
        booking.save()

        messages.success(request, "Payment successful! Your photography booking is now confirmed.")
        return redirect("user_photography_bookings")

    return render(request, "photography_payment.html", {"booking": booking})

@login_required
def photography_payment_status(request):
    user_payments = Payment.objects.filter(user=request.user, booking_type="photography")

    service_provider = ServiceProvider.objects.filter(user=request.user).first()
    provider_payments = Payment.objects.filter(service_provider=service_provider, booking_type="photography") if service_provider else None

    return render(request, "photography_payment_status.html", {
        "user_payments": user_payments,
        "provider_payments": provider_payments
    })



## Bride Groom Service ##


@login_required
def bridal_groom_list(request):
    services = BridalGroomService.objects.filter(available=True)
    return render(request, "user_bridal_groom_list.html", {"services": services})


@login_required
def book_bridal_groom(request, service_id):
    service = get_object_or_404(BridalGroomService, id=service_id)

    if request.method == "POST":
        event_date = request.POST.get("event_date")
        suggest_theme = request.POST.get("suggest_theme")

        if date.fromisoformat(event_date) < date.today():
            messages.error(request, "You cannot book bridal & groom services for a past date.")
            return redirect("book_bridal_groom", service_id=service_id)

        is_booked = ServiceAvailability.objects.filter(
            service_type="BridalGroom",
            service_id=service.id,
            booked_date=event_date
        ).exists()

        if is_booked:
            messages.error(request, "This bridal & groom service is already booked on the selected date.")
        else:
            BridalGroomServiceBooking.objects.create(
                user=request.user,
                service=service,
                suggest_theme=suggest_theme,
                event_date=event_date,
                status="Pending"
            )

            ServiceAvailability.objects.create(
                service_type='BridalGroom',
                service_id=service.id,
                booked_date=event_date,
            )
            messages.success(request, "Bridal & Groom service booked successfully. Awaiting approval.")

        return redirect("user_bridal_groom_bookings")

    return render(request, "user_book_bridal_groom.html", {"service": service})


@login_required
def user_bridal_groom_bookings(request):
    bookings = BridalGroomServiceBooking.objects.filter(user=request.user)
    return render(request, "user_bridal_groom_bookings.html", {"bookings": bookings})


@login_required
def bridal_groom_payment(request, booking_id):
    booking = get_object_or_404(BridalGroomServiceBooking, id=booking_id, user=request.user)

    if booking.status != "Confirmed":
        messages.error(request, "You can only pay for confirmed bookings.")
        return redirect("user_bridal_groom_bookings")

    provider = booking.service.provider
    amount = booking.service.price

    if request.method == "POST":
        transaction_id = ''.join(random.choices(string.ascii_letters + string.digits, k=10))

        Payment.objects.create(
            user=request.user,
            service_provider=provider,
            booking_type="bride_groom",
            booking_id=booking.id,
            amount=amount,
            transaction_id=transaction_id,
            status="paid",
        )

        booking.status = "Paid"
        booking.save()

        messages.success(request, "Payment successful! Your bridal & groom booking is now confirmed.")
        return redirect("user_bridal_groom_bookings")

    return render(request, "bridal_groom_payment.html", {"booking": booking})


@login_required
def bridal_groom_payment_status(request):
    user_payments = Payment.objects.filter(user=request.user, booking_type="bride_groom")

    service_provider = ServiceProvider.objects.filter(user=request.user).first()
    provider_payments = Payment.objects.filter(service_provider=service_provider, booking_type="bride_groom") if service_provider else None

    return render(request, "bridal_groom_payment_status.html", {
        "user_payments": user_payments,
        "provider_payments": provider_payments
    })



@login_required
def whatsapp(request):
    mob_number = "918888888888"  
    message = "Chat with us" 
    whatsapp_url = f"https://wa.me/{mob_number}?text={message}"
    
    return render(request,'whatsapp.html',{'whatsapp_url':whatsapp_url})










