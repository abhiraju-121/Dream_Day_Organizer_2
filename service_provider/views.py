from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from . models import ServiceProvider
from user.models import User,Event,BookEvent,Venue,VenueBooking,TransportationBooking,TransportationService,CateringService,CateringBooking,DecorationsBooking,DecorationsService,PhotographyBooking,PhotographyService,BridalGroomServiceBooking,BridalGroomService
from django.contrib.auth import authenticate,login,logout


# Create your views here.



def servicer_home(request):
    return render(request,'servicer_home.html')

def servicer_register(request):
    if request.method == "POST":
        username=request.POST.get('username')
        email=request.POST.get('email')
        password=request.POST.get('password')
        confirm_password=request.POST.get('confirm_password')
        company_name=request.POST.get('company_name')
        service_type=request.POST.get('service_type')

        if User.objects.filter(email=email).exists():
            messages.error(request,"Email already exists !!")
            return redirect('servicer_register')
        if confirm_password!=password:
            messages.error(request,"Enter passowrd properly !!")
            return redirect('servicer_register')


        user=User.objects.create_user(username=username,password=password,email=email,is_service_provider=True)

        service_provider=ServiceProvider.objects.create(user=user,company_name=company_name,service_type=service_type)
        service_provider.save()
        return redirect('servicer_login')
    
    return render(request, 'servicer_register.html')


def servicer_login(request):
    if request.method == "POST":
        email=request.POST.get('email')
        password=request.POST.get('password')

        user=authenticate(request,email=email,password=password)
        
        if user is not None:
            login(request,user)
            return redirect('servicer_home')
        else:
            messages.error(request,'Invalid Username or Password !!')
            return redirect('servicer_login')
    return render(request,'servicer_login.html')

def servicer_logout(request):
    logout(request)
    return redirect('servicer_login')   
# @login_required
# def servicer_dashboard(request):
#     service_provider = get_object_or_404(ServiceProvider, user=request.user)
#     return render(request, 'servicer_dashboard.html', {'service_provider': service_provider})

@login_required
def service_provider_dashboard(request):
    service_provider = get_object_or_404(ServiceProvider,user=request.user)

    if service_provider.service_type == 'photo_videography':
        return render(request, 'dashboard_photo_videography.html', {'service_provider': service_provider})
    elif service_provider.service_type == 'event_planners':
        return render(request, 'dashboard_event_planners.html', {'service_provider': service_provider})
    elif service_provider.service_type == 'catering':
        return render(request, 'dashboard_catering.html', {'service_provider': service_provider})
    elif service_provider.service_type == 'bride_groom_service':
        return render(request, 'dashboard_bride_groom.html', {'service_provider': service_provider})
    elif service_provider.service_type == 'decoration':
        return render(request, 'dashboard_decoration.html', {'service_provider': service_provider})
    elif service_provider.service_type == 'transportation':
        return render(request, 'dashboard_transportation.html', {'service_provider': service_provider})
    elif service_provider.service_type == 'venue_planners':
        return render(request,'dashboard_venue_planners.html',{'service_provider':service_provider})
    else:
        return redirect('home') 
    

## event ##
@login_required
def provider_event_list(request):
    """Service Provider lists all their events."""
    provider = get_object_or_404(ServiceProvider, user=request.user)
    events = Event.objects.filter(service_provider=provider)
    return render(request, 'provider_event_list.html', {'events': events})

@login_required
def add_event(request):
    """Service Provider adds a new event."""
    if request.method == "POST":
        provider = get_object_or_404(ServiceProvider, user=request.user)
        name = request.POST.get("name")
        image = request.FILES.get("image")
        location = request.POST.get("location")
        price = request.POST.get("price")
        description = request.POST.get("description")

        Event.objects.create(
            service_provider=provider,
            name=name,
            image=image,
            location=location,
            price=price,
            description=description,
        )
        return redirect("provider_event_list")

    return render(request, "add_event.html")

@login_required
def edit_event(request, event_id):
    """Service Provider edits an event."""
    service_provider = get_object_or_404(ServiceProvider, user=request.user)
    event = get_object_or_404(Event, id=event_id, service_provider=service_provider)

    if request.method == "POST":
        event.name = request.POST.get("name")
        event.image = request.FILES.get("image") or event.image
        event.location = request.POST.get("location")
        event.price = request.POST.get("price")
        event.description = request.POST.get("description")
        event.save()
        return redirect("provider_event_list")

    return render(request, "edit_event.html", {"event": event})

@login_required
def delete_event(request, event_id):
    """Service Provider deletes an event."""
    service_provider = get_object_or_404(ServiceProvider, user=request.user)
    event = get_object_or_404(Event, id=event_id, service_provider=service_provider)
    event.delete()
    return redirect("provider_event_list")

@login_required
def manage_event_bookings(request):
    """Service Provider manages all event bookings."""
    provider = get_object_or_404(ServiceProvider, user=request.user)
    bookings = BookEvent.objects.filter(event__service_provider=provider)
    return render(request, "provider_event_bookings.html", {"bookings": bookings})

@login_required
def approve_event_booking(request, booking_id):
    """Service Provider approves an event booking."""
    provider = get_object_or_404(ServiceProvider, user=request.user)
    booking = get_object_or_404(BookEvent, id=booking_id, event__service_provider=provider)
    booking.status = "Approved"
    booking.save()
    return redirect("manage_event_bookings")

@login_required
def reject_event_booking(request, booking_id):
    """Service Provider rejects an event booking."""
    provider = get_object_or_404(ServiceProvider, user=request.user)
    booking = get_object_or_404(BookEvent, id=booking_id, event__service_provider=provider)
    booking.status = "Rejected"
    booking.save()
    return redirect("manage_event_bookings")




##Venu##

@login_required
def provider_venue_list(request):
    """Service Provider lists all their venues"""
    provider = get_object_or_404(ServiceProvider, user=request.user)
    venues = Venue.objects.filter(provider=provider)
    return render(request, 'venue_list.html', {'venues': venues})

@login_required
def add_venue(request):
    """Service Provider adds a new venue"""
    if request.method == "POST":
        provider = get_object_or_404(ServiceProvider, user=request.user)
        name = request.POST.get("name")
        image = request.FILES.get("image")
        location = request.POST.get("location")
        capacity = request.POST.get("capacity")
        price = request.POST.get("price")
        description = request.POST.get("description")

        Venue.objects.create(
            provider=provider,
            name=name,
            image=image,
            location=location,
            capacity=capacity,
            price=price,
            description=description,
        )
        return redirect("provider_venue_list")

    return render(request, "add_venue.html")

@login_required
def edit_venue(request, venue_id):
    service_provider = get_object_or_404(ServiceProvider, user=request.user)
    venue = get_object_or_404(Venue, id=venue_id, provider=service_provider)

    if request.method == "POST":
        venue.name = request.POST.get("name")
        venue.image = request.FILES.get("image") or venue.image
        venue.location = request.POST.get("location")
        venue.capacity = request.POST.get("capacity")
        venue.price = request.POST.get("price")
        venue.description = request.POST.get("description")
        venue.save()
        return redirect("provider_venue_list")

    return render(request, "edit_venue.html", {"venue": venue})

@login_required
def delete_venue(request, venue_id):
    service_provider = get_object_or_404(ServiceProvider, user=request.user)
    venue = get_object_or_404(Venue, id=venue_id, provider=service_provider)
    venue.delete()
    return redirect("provider_venue_list")

@login_required
def manage_bookings(request):
    provider = get_object_or_404(ServiceProvider, user=request.user)
    bookings = VenueBooking.objects.filter(venue__provider=provider)
    return render(request, "provider_booking_venue.html", {"bookings": bookings})

@login_required
def approve_booking(request, booking_id):
    provider = get_object_or_404(ServiceProvider, user=request.user)
    booking = get_object_or_404(VenueBooking, id=booking_id, venue__provider=provider)
    booking.status = "Confirmed"
    booking.save()
    return redirect("manage_bookings")

@login_required
def reject_booking(request, booking_id):
    provider = get_object_or_404(ServiceProvider, user=request.user)
    booking = get_object_or_404(VenueBooking, id=booking_id, venue__provider=provider)
    booking.status = "Rejected"
    booking.save()
    return redirect("manage_bookings")


##Transportation##

@login_required
def service_provider_transports_list(request):
    provider = get_object_or_404(ServiceProvider, user=request.user)
    transport_services = TransportationService.objects.filter(provider=provider)
    return render(request, 'provider_transport_list.html', {'transport_services': transport_services})

@login_required
def add_transport(request):
    if request.method == "POST":
        provider = get_object_or_404(ServiceProvider, user=request.user)
        name = request.POST.get("name")
        image = request.FILES.get("image")
        desc = request.POST.get("desc")
        price = request.POST.get("price")

        TransportationService.objects.create(
            provider=provider,
            name=name,
            image=image,
            desc=desc,
            price=price
        )
        return redirect("service_provider_transports_list")

    return render(request, "provider_add_transport_service.html")

@login_required
def edit_transport(request, service_id):
    service_provider = get_object_or_404(ServiceProvider, user=request.user)
    service = get_object_or_404(TransportationService, id=service_id, provider=service_provider)

    if request.method == "POST":
        service.name = request.POST.get("name")
        service.image = request.FILES.get("image") or service.image
        service.desc = request.POST.get("desc")
        service.price = request.POST.get("price")
        service.save()
        return redirect("service_provider_transports_list")

    return render(request, "provider_edit_transport_service.html", {"service": service})

@login_required
def delete_transport(request, service_id):
    service_provider = get_object_or_404(ServiceProvider, user=request.user)
    service = get_object_or_404(TransportationService, id=service_id, provider=service_provider)
    service.delete()
    return redirect("service_provider_transports_list")

@login_required
def manage_transport_bookings(request):
    provider = get_object_or_404(ServiceProvider, user=request.user)
    bookings = TransportationBooking.objects.filter(service__provider=provider)
    return render(request, "provider_transport_bookings.html", {"bookings": bookings})

@login_required
def approve_transport_booking(request, booking_id):
    provider = get_object_or_404(ServiceProvider, user=request.user)
    booking = get_object_or_404(TransportationBooking, id=booking_id, service__provider=provider)
    booking.status = "Confirmed"
    booking.save()
    return redirect("manage_transport_bookings")

@login_required
def reject_transport_booking(request, booking_id):
    provider = get_object_or_404(ServiceProvider, user=request.user)
    booking = get_object_or_404(TransportationBooking, id=booking_id, service__provider=provider)
    booking.status = "Rejected"
    booking.save()
    return redirect("manage_transport_bookings")


## caterning ##


@login_required
def provider_catering_list(request):
    provider = get_object_or_404(ServiceProvider, user=request.user)
    caterings = CateringService.objects.filter(provider=provider)
    return render(request, 'provider_catering_list.html', {'caterings': caterings})


@login_required
def add_catering(request):
    if request.method == "POST":
        provider = get_object_or_404(ServiceProvider, user=request.user)
        menu_name = request.POST.get("menu_name")
        desc = request.POST.get("desc")
        images = request.FILES.get("images")
        price = request.POST.get("price")

        CateringService.objects.create(
            provider=provider,
            menu_name=menu_name,
            desc=desc,
            images=images,
            price=price
        )
        return redirect("provider_catering_list")

    return render(request, "provider_add_catering.html")


@login_required
def edit_catering(request, catering_id):
    provider = get_object_or_404(ServiceProvider, user=request.user)
    catering = get_object_or_404(CateringService, id=catering_id, provider=provider)

    if request.method == "POST":
        catering.menu_name = request.POST.get("menu_name")
        catering.desc = request.POST.get("desc")
        catering.images = request.FILES.get("images") or catering.images
        catering.price = request.POST.get("price")
        catering.save()
        return redirect("provider_catering_list")

    return render(request, "provider_edit_catering.html", {"catering": catering})


@login_required
def delete_catering(request, catering_id):
    provider = get_object_or_404(ServiceProvider, user=request.user)
    catering = get_object_or_404(CateringService, id=catering_id, provider=provider)
    catering.delete()
    return redirect("provider_catering_list")


@login_required
def manage_catering_bookings(request):
    provider = get_object_or_404(ServiceProvider, user=request.user)
    bookings = CateringBooking.objects.filter(service__provider=provider)
    return render(request, "provider_booking_catering.html", {"bookings": bookings})


@login_required
def approve_catering_booking(request, booking_id):
    provider = get_object_or_404(ServiceProvider, user=request.user)
    booking = get_object_or_404(CateringBooking, id=booking_id, service__provider=provider)
    booking.status = "Confirmed"
    booking.save()
    return redirect("manage_catering_bookings")


@login_required
def reject_catering_booking(request, booking_id):
    provider = get_object_or_404(ServiceProvider, user=request.user)
    booking = get_object_or_404(CateringBooking, id=booking_id, service__provider=provider)
    booking.status = "Rejected"
    booking.save()
    return redirect("manage_catering_bookings")



## Decoration ##

@login_required
def provider_decorations_list(request):
    provider = get_object_or_404(ServiceProvider, user=request.user)
    decorations = DecorationsService.objects.filter(provider=provider)
    return render(request, 'provider_decorations_list.html', {'decorations': decorations})


@login_required
def add_decoration(request):
    if request.method == "POST":
        provider = get_object_or_404(ServiceProvider, user=request.user)
        name = request.POST.get("name")
        theme_options = request.POST.get("theme_options")
        desc = request.POST.get("desc")
        image = request.FILES.get("image")
        price = request.POST.get("price")

        DecorationsService.objects.create(
            provider=provider,
            name=name,
            theme_options=theme_options,
            desc=desc,
            image=image,
            price=price,
        )
        return redirect("provider_decorations_list")

    return render(request, "provider_add_decoration.html")


@login_required
def edit_decoration(request, decoration_id):
    service_provider = get_object_or_404(ServiceProvider, user=request.user)
    decoration = get_object_or_404(DecorationsService, id=decoration_id, provider=service_provider)

    if request.method == "POST":
        decoration.name = request.POST.get("name")
        decoration.theme_options = request.POST.get("theme_options")
        decoration.desc = request.POST.get("desc")
        decoration.image = request.FILES.get("image") or decoration.image
        decoration.price = request.POST.get("price")
        decoration.save()
        return redirect("provider_decorations_list")

    return render(request, "provider_edit_decoration.html", {"decoration": decoration})


@login_required
def delete_decoration(request, decoration_id):
    service_provider = get_object_or_404(ServiceProvider, user=request.user)
    decoration = get_object_or_404(DecorationsService, id=decoration_id, provider=service_provider)
    decoration.delete()
    return redirect("provider_decorations_list")


@login_required
def manage_decorations_bookings(request):
    provider = get_object_or_404(ServiceProvider, user=request.user)
    bookings = DecorationsBooking.objects.filter(service__provider=provider)
    return render(request, "provider_bookings_decorations.html", {"bookings": bookings})


@login_required
def approve_decoration_booking(request, booking_id):
    provider = get_object_or_404(ServiceProvider, user=request.user)
    booking = get_object_or_404(DecorationsBooking, id=booking_id, service__provider=provider)
    booking.status = "Confirmed"
    booking.save()
    return redirect("manage_decorations_bookings")


@login_required
def reject_decoration_booking(request, booking_id):
    provider = get_object_or_404(ServiceProvider, user=request.user)
    booking = get_object_or_404(DecorationsBooking, id=booking_id, service__provider=provider)
    booking.status = "Rejected"
    booking.save()
    return redirect("manage_decorations_bookings")


## Photography & VIdeography ##

@login_required
def provider_photography_list(request):
    provider = get_object_or_404(ServiceProvider, user=request.user)
    services = PhotographyService.objects.filter(provider=provider)
    return render(request, 'provider_photography_list.html', {'services': services})

@login_required
def add_photography(request):
    if request.method == "POST":
        provider = get_object_or_404(ServiceProvider, user=request.user)
        package_name = request.POST.get("package_name")
        desc = request.POST.get("desc")
        image = request.FILES.get("image")
        price = request.POST.get("price")
        includes_video = request.POST.get("includes_video") == "on"

        PhotographyService.objects.create(
            provider=provider,
            package_name=package_name,
            desc=desc,
            image=image,
            price=price,
            includes_video=includes_video
        )
        return redirect("provider_photography_list")

    return render(request, "provider_add_photography.html")

@login_required
def edit_photography(request, photography_id):
    service_provider = get_object_or_404(ServiceProvider, user=request.user)
    service = get_object_or_404(PhotographyService, id=photography_id, provider=service_provider)

    if request.method == "POST":
        service.package_name = request.POST.get("package_name")
        service.desc = request.POST.get("desc")
        service.image = request.FILES.get("image") or service.image
        service.price = request.POST.get("price")
        service.includes_video = request.POST.get("includes_video") == "on"
        service.save()
        return redirect("provider_photography_list")

    return render(request, "provider_edit_photography.html", {"service": service})

@login_required
def delete_photography(request, photography_id):
    service_provider = get_object_or_404(ServiceProvider, user=request.user)
    service = get_object_or_404(PhotographyService, id=photography_id, provider=service_provider)
    service.delete()
    return redirect("provider_photography_list")

@login_required
def manage_photography_bookings(request):
    provider = get_object_or_404(ServiceProvider, user=request.user)
    bookings = PhotographyBooking.objects.filter(service__provider=provider)
    return render(request, "provider_bookings_photography.html", {"bookings": bookings})

@login_required
def approve_photography_booking(request, booking_id):
    provider = get_object_or_404(ServiceProvider, user=request.user)
    booking = get_object_or_404(PhotographyBooking, id=booking_id, service__provider=provider)
    booking.status = "Confirmed"
    booking.save()
    return redirect("manage_photography_bookings")

@login_required
def reject_photography_booking(request, booking_id):
    provider = get_object_or_404(ServiceProvider, user=request.user)
    booking = get_object_or_404(PhotographyBooking, id=booking_id, service__provider=provider)
    booking.status = "Rejected"
    booking.save()
    return redirect("manage_photography_bookings")

## bride and groom ##

@login_required
def provider_bridal_groom_list(request):
    provider = get_object_or_404(ServiceProvider, user=request.user)
    services = BridalGroomService.objects.filter(provider=provider)
    return render(request, 'provider_bridal_groom_list.html', {'services': services})

 
@login_required
def add_bridal_groom(request):
    if request.method == "POST":
        provider = get_object_or_404(ServiceProvider, user=request.user)
        package_name = request.POST.get("package_name")
        package_details = request.POST.get("package_details")
        desc = request.POST.get("desc")
        image = request.FILES.get("image")
        price = request.POST.get("price")

        BridalGroomService.objects.create(
            provider=provider,
            package_name=package_name,
            package_details=package_details,
            desc=desc,
            image=image,
            price=price,
        )
        return redirect("provider_bridal_groom_list")

    return render(request, "provider_add_bridal_groom.html")


@login_required
def edit_bridal_groom(request, service_id):
    service_provider = get_object_or_404(ServiceProvider, user=request.user)
    service = get_object_or_404(BridalGroomService, id=service_id, provider=service_provider)

    if request.method == "POST":
        service.package_name = request.POST.get("package_name")
        service.package_details = request.POST.get("package_details")
        service.desc = request.POST.get("desc")
        service.image = request.FILES.get("image") or service.image
        service.price = request.POST.get("price")
        service.save()
        return redirect("provider_bridal_groom_list")

    return render(request, "provider_edit_bridal_groom.html", {"service": service})


@login_required
def delete_bridal_groom(request, service_id):
    service_provider = get_object_or_404(ServiceProvider, user=request.user)
    service = get_object_or_404(BridalGroomService, id=service_id, provider=service_provider)
    service.delete()
    return redirect("provider_bridal_groom_list")


@login_required
def manage_bridal_groom_bookings(request):
    provider = get_object_or_404(ServiceProvider, user=request.user)
    bookings = BridalGroomServiceBooking.objects.filter(service__provider=provider)
    return render(request, "provider_bookings_bridal_groom.html", {"bookings": bookings})


@login_required
def approve_bridal_groom_booking(request, booking_id):
    provider = get_object_or_404(ServiceProvider, user=request.user)
    booking = get_object_or_404(BridalGroomServiceBooking, id=booking_id, service__provider=provider)
    booking.status = "Confirmed"
    booking.save()
    return redirect("manage_bridal_groom_bookings")


@login_required
def reject_bridal_groom_booking(request, booking_id):

    provider = get_object_or_404(ServiceProvider, user=request.user)
    booking = get_object_or_404(BridalGroomServiceBooking, id=booking_id, service__provider=provider)
    booking.status = "Rejected"
    booking.save()
    return redirect("manage_bridal_groom_bookings")







# @login_required
# def provider_venue_list(request):
#     service_provider = ServiceProvider.objects.get(user=request.user)
#     venues = Venue.objects.filter(provider=service_provider)
#     return render(request, 'venue_list.html', {'venues': venues})

# @login_required
# def add_venue(request):
#     service_provider = get_object_or_404(ServiceProvider, user=request.user)

#     if request.method == "POST":
#         name = request.POST.get('name')
#         image = request.FILES.get('image')
#         location = request.POST.get('location')
#         capacity = request.POST.get('capacity')
#         description = request.POST.get('description')
#         available = request.POST.get('available', False) == 'on'

#         Venue.objects.create(
#             provider=service_provider,
#             name=name,
#             image=image,
#             location=location,
#             capacity=capacity,
#             description=description,
#             available=available
#         )
#         messages.success(request, "Venue added successfully!")
#         return redirect('venue_list')

#     return render(request, 'add_venue.html')

# @login_required
# def edit_venue(request, venue_id):
#     service_provider = get_object_or_404(ServiceProvider, user=request.user)
#     venue = get_object_or_404(Venue, id=venue_id, provider=service_provider)

#     if request.method == "POST":
#         venue.name = request.POST['name']
#         if 'image' in request.FILES:
#             venue.image = request.FILES.get('image')
#         venue.location = request.POST.get('location')
#         venue.capacity = request.POST.get('capacity')
#         venue.description = request.POST.get('description')
#         venue.available = request.POST.get('available', False) == 'on'
#         venue.save()

#         messages.success(request, "Venue updated successfully!")
#         return redirect('venue_list')

#     return render(request, 'edit_venue.html', {'venue': venue})

# @login_required
# def delete_venue(request, venue_id):
#     """ Delete a venue """
#     venue = get_object_or_404(Venue, id=venue_id, provider=request.user)
#     venue.delete()
#     messages.success(request, "Venue deleted successfully!")
#     return redirect('venue_list')



# @login_required
# def provider_bookings(request):
#     service_provider=get_object_or_404(ServiceProvider,user=request.user)
#     bookings = VenueBooking.objects.filter(venue__provider=service_provider)
#     return render(request, 'provider_booking_venue.html', {'bookings': bookings})

# @login_required
# def approve_booking(request, booking_id):
#     service_provider=get_object_or_404(ServiceProvider,user=request.user)
#     booking = get_object_or_404(VenueBooking, id=booking_id, venue__provider=service_provider)
#     booking.status = "Confirmed"
#     booking.save()
#     messages.success(request, "Booking approved successfully!")
#     return redirect('provider_bookings')

# @login_required
# def reject_booking(request, booking_id):
#     service_provider=get_object_or_404(ServiceProvider,user=request.user)
#     booking = get_object_or_404(VenueBooking, id=booking_id, venue__provider=service_provider)
#     booking.status = "Rejected"
#     booking.save()
#     messages.error(request, "Booking rejected.")
#     return redirect('provider_bookings')




# @login_required
# def service_provider_transports(request):
#     service_provider=get_object_or_404(ServiceProvider,user=request.user)
#     transports = TransportationService.objects.filter(provider=service_provider)
#     return render(request, 'transport_provider_list.html', {'transports': transports})

# @login_required
# def add_transport(request):
#     service_provider=get_object_or_404(ServiceProvider,user=request.user)
#     if request.method == "POST":
#         name = request.POST.get("name")
#         image = request.FILES.get("image")
#         desc=request.POST.get('desc')
#         available = request.POST.get('available', False) == 'on'

#         TransportationService.objects.create(
#             provider=service_provider,
#             name=name,
#             image=image,
#             desc=desc,
#             available=available
#         )

#         messages.success(request, "Transport service added successfully.")
#         return redirect('service_provider_transports')

#     return render(request, 'provider_add_transport.html')


# @login_required
# def edit_transport(request, service_id):
#     service_provider = get_object_or_404(ServiceProvider, user=request.user)
#     transport = get_object_or_404(TransportationService, id=service_id, provider=service_provider)

#     if request.method == "POST":
#         transport.name = request.POST.get('name')
#         transport.desc = request.POST.get('desc')
#         transport.available = request.POST.get('available', False) == 'on'

#         if 'image' in request.FILES:
#             transport.image = request.FILES.get('image')

#         transport.save()
#         messages.success(request, "Transport updated successfully!")
#         return redirect('service_provider_transports')

#     return render(request, 'edit_transport.html', {'transport': transport})


# @login_required
# def provider_manage_trans_bookings(request):
#     service_provider=get_object_or_404(ServiceProvider,user=request.user)
#     bookings = TransportationBooking.objects.filter(service__provider=service_provider)
#     return render(request, 'provider_manage_trans_booking.html', {'bookings': bookings})

# @login_required
# def update_booking_status(request, booking_id, status):
#     service_provider=get_object_or_404(ServiceProvider,user=request.user)
#     booking = get_object_or_404(TransportationBooking, id=booking_id, service__provider=service_provider)

#     if status in ['Confirmed', 'Completed']:
#         booking.status = status
#         booking.save()
#         messages.success(request, f"Booking status updated to {status}.")
#     elif status == 'Rejected':
#         booking.delete()
#         messages.success(request, "Booking rejected and removed.")
#     return redirect('provider_manage_trans_bookings')





# @login_required
# def provider_catering_services_list(request):
#     provider = get_object_or_404(ServiceProvider, user=request.user)
#     services = CateringService.objects.filter(provider=provider)
#     return render(request, 'provider_catering_list.html', {'services': services})

# @login_required
# def add_catering_service(request):
#     provider = get_object_or_404(ServiceProvider, user=request.user)

#     if request.method == 'POST':
#         menu_name = request.POST.get('menu_name')
#         desc = request.POST.get('desc')
#         image = request.FILES.get('image')
#         available = request.POST.get('available') == 'on'

#         if not menu_name or not desc or not image:
#             messages.error(request, "All fields are required!")
#             return redirect('add_catering_service')

#         CateringService.objects.create(
#             provider=provider,
#             menu_name=menu_name,
#             desc=desc,
#             images=image,
#             available=available
#         )
#         messages.success(request, "Catering service added successfully!")
#         return redirect('provider_catering_services_list')
#     return render(request, 'provider_add_catering_service.html')

# @login_required
# def edit_catering_service(request, service_id):
#     provider = get_object_or_404(ServiceProvider, user=request.user)
#     service = get_object_or_404(CateringService, id=service_id, provider=provider)

#     if request.method == 'POST':
#         service.menu_name = request.POST.get('menu_name')
#         service.desc = request.POST.get('desc')
#         if request.FILES.get('image'):
#             service.images = request.FILES.get('image')
#         service.available = request.POST.get('available') == 'on'
#         service.save()

#         messages.success(request, "Catering service updated successfully!")
#         return redirect('provider_catering_services')

#     return render(request, 'provider_edit_catering_service.html', {'service': service})

# @login_required
# def delete_catering_service(request, service_id):
#     provider = get_object_or_404(ServiceProvider, user=request.user)
#     service = get_object_or_404(CateringService, id=service_id, provider=provider)
#     service.delete()
#     messages.success(request, "Catering service deleted successfully!")
#     return redirect('provider_catering_services')

# @login_required
# def provider_catering_bookings(request):
#     provider = get_object_or_404(ServiceProvider, user=request.user)
#     bookings = CateringBooking.objects.filter(service__provider=provider)
#     return render(request, 'provider_catering_bookings.html', {'bookings': bookings})


# @login_required
# def manage_catering_booking_status(request, booking_id):
#     provider = get_object_or_404(ServiceProvider, user=request.user)
#     booking = get_object_or_404(CateringBooking, id=booking_id, service__provider=provider)

#     if request.method == 'POST':
#         new_status = request.POST.get('status')
#         if new_status in ['Pending', 'Confirmed', 'Completed']:
#             booking.status = new_status
#             booking.save()
#             messages.success(request, f"Booking status updated to {new_status}!")
#         else:
#             messages.error(request, "Invalid status selection!")

#     return redirect('provider_catering_bookings')
