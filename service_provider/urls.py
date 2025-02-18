from django.urls import path
from . import views

urlpatterns=[
    path('servicer_register',views.servicer_register,name='servicer_register'),
    path('servicer_login',views.servicer_login,name='servicer_login'),
    path('servicer_logout',views.servicer_logout,name='servicer_logout'),
    path('servicer_dashboard',views.service_provider_dashboard,name='servicer_dashboard'),
    path('servicer_home',views.servicer_home,name='servicer_home'),

    path('service_provider_event_list', views.provider_event_list, name='provider_event_list'),
    path('add_event', views.add_event, name='add_event'),
    path('edit_event/<int:event_id>/', views.edit_event, name='edit_event'),
    path('delete_event/<int:event_id>/', views.delete_event, name='delete_event'),
    path('manage_event_bookings',views.manage_event_bookings,name='manage_event_bookings'),
    path('manage_event_bookings/approve/<int:booking_id>/', views.approve_event_booking, name='approve_event_booking'),
    path('manage_event_bookings/reject/<int:booking_id>/', views.reject_event_booking, name='reject_event_booking'),




    path('provider_venue_list', views.provider_venue_list, name='provider_venue_list'),
    path('add_venue', views.add_venue, name='add_venue'),
    path('add_venue/edit/<int:venue_id>/', views.edit_venue, name='edit_venue'),
    path('add_venue/remove/<int:venue_id>/', views.delete_venue, name='delete_venue'),
    path('provider_bookings', views.manage_bookings, name='manage_bookings'),
    path('provider_bookings/approve/<int:booking_id>/', views.approve_booking, name='approve_booking'),
    path('provider_bookings/reject/<int:booking_id>/', views.reject_booking, name='reject_booking'),


    path('service_provider_transports_list', views.service_provider_transports_list, name='service_provider_transports_list'),
    path('service-provider/transport/add/', views.add_transport, name='add_transport'),
    path('edit_transport/<int:service_id>/',views.edit_transport,name='edit_transport'),
    path('delete_transport/remove/<int:service_id>/', views.delete_transport, name='delete_transport'),
    path('manage_transport_bookings', views.manage_transport_bookings, name='manage_transport_bookings'),
    path('manage_transport_bookings/approve/<int:booking_id>/', views.approve_transport_booking, name='approve_transport_booking'),
    path('manage_transport_bookings/reject/<int:booking_id>/', views.reject_transport_booking, name='reject_transport_booking'),



    path('provider_catering_list', views.provider_catering_list, name='provider_catering_list'),
    path('add_catering/', views.add_catering, name='add_catering'),
    path('edit_catering/<int:catering_id>/', views.edit_catering, name='edit_catering'),
    path('delete_catering/<int:catering_id>/', views.delete_catering, name='delete_catering'),
    path('provider_catering_bookings', views.manage_catering_bookings, name='manage_catering_bookings'),
    path('provider_catering_bookings/approve/<int:booking_id>/', views.approve_catering_booking, name='approve_catering_booking'),
    path('provider_catering_bookings/reject/<int:booking_id>/', views.reject_catering_booking, name='reject_catering_booking'),



    path("provider/decorations/", views.provider_decorations_list, name="provider_decorations_list"),
    path("provider/decorations/add/", views.add_decoration, name="add_decoration"),
    path("provider/decorations/edit/<int:decoration_id>/", views.edit_decoration, name="edit_decoration"),
    path("provider/decorations/delete/<int:decoration_id>/", views.delete_decoration, name="delete_decoration"),
    path("provider/decorations/bookings/", views.manage_decorations_bookings, name="manage_decorations_bookings"),
    path("provider/decorations/approve/<int:booking_id>/", views.approve_decoration_booking, name="approve_decoration_booking"),
    path("provider/decorations/reject/<int:booking_id>/", views.reject_decoration_booking, name="reject_decoration_booking"),


    path('provider/services/', views.provider_photography_list, name='provider_photography_list'),
    path('provider/add/', views.add_photography, name='add_photography'),
    path('provider/edit/<int:photography_id>/', views.edit_photography, name='edit_photography'),
    path('provider/delete/<int:photography_id>/', views.delete_photography, name='delete_photography'),
    path('provider/bookings/', views.manage_photography_bookings, name='manage_photography_bookings'),
    path('provider/bookings/approve/<int:booking_id>/', views.approve_photography_booking, name='approve_photography_booking'),
    path('provider/bookings/reject/<int:booking_id>/', views.reject_photography_booking, name='reject_photography_booking'),


    path('provider/bridal-groom/', views.provider_bridal_groom_list, name='provider_bridal_groom_list'),
    path('provider/bridal-groom/add/', views.add_bridal_groom, name='add_bridal_groom'),
    path('provider/bridal-groom/edit/<int:service_id>/', views.edit_bridal_groom, name='edit_bridal_groom'),
    path('provider/bridal-groom/delete/<int:service_id>/', views.delete_bridal_groom, name='delete_bridal_groom'),
    path('provider/bridal-groom/bookings/', views.manage_bridal_groom_bookings, name='manage_bridal_groom_bookings'),
    path('provider/bridal-groom/booking/approve/<int:booking_id>/', views.approve_bridal_groom_booking, name='approve_bridal_groom_booking'),
    path('provider/bridal-groom/booking/reject/<int:booking_id>/', views.reject_bridal_groom_booking, name='reject_bridal_groom_booking'),



]