from django.contrib import admin
from .models import Event,BookEvent,Venue,VenueBooking,TransportationBooking,CateringBooking,CateringService,Payment,PhotographyBooking,PhotographyService,TransportationService,BridalGroomService,BridalGroomServiceBooking,ServiceAvailability,User,DecorationsBooking,DecorationsService
from service_provider.models import ServiceProvider



admin.site.register(ServiceAvailability)
admin.site.register(ServiceProvider)
admin.site.register(User)
admin.site.register(Payment)
admin.site.register(Event)
admin.site.register(BookEvent)
admin.site.register(Venue)
admin.site.register(VenueBooking)
admin.site.register(TransportationService)
admin.site.register(TransportationBooking)
admin.site.register(CateringService)
admin.site.register(CateringBooking)
admin.site.register(PhotographyService)
admin.site.register(PhotographyBooking)
admin.site.register(DecorationsService)
admin.site.register(DecorationsBooking)
admin.site.register(BridalGroomService)
admin.site.register(BridalGroomServiceBooking)
