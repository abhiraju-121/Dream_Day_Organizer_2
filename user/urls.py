from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('',views.base,name='base'),
    path('home',views.home,name='home'),
    path('user_register',views.register_user,name='user_register'),
    path('login_user',views.login_user,name='user_login'),
    path('logout_user',views.logout_user,name='user_logout'),
    path('user_dashboard',views.user_dashboard,name='user_dashboard'),
    path('user_profile',views.user_profile,name='user_profile'),
    path('user_all_bookings',views.user_all_bookings,name='user_all_bookings'),


    path('view_event',views.user_event_list,name='user_event_list'),
    path('user_book_event/<int:event_id>/',views.user_book_event,name='user_book_event'),
    path('user_event_bookings/',views.user_event_bookings,name='user_event_bookings'),
    path('event_payment/<int:booking_id>/',views.event_payment,name='event_payment'),
    path('event_payment_status/<int:booking_id>/',views.event_payment_status,name='event_payment_status'),
    
    
    
    path('venues/', views.venue_list, name='venue_list'),
    path('venues/book/<int:venue_id>/', views.book_venue, name='book_venue'),
    path('user/bookings/', views.user_bookings, name='user_bookings'),
    path('venues/payment/<int:booking_id>/', views.venue_payment, name='venue_payment'),  # Fixed URL for payments
    # path('venue_payment_success/<str:transaction_id>/<int:booking_id>/', views.venue_payment_success, name='venue_payment_success'),
    path('venue_payment_status/', views.venue_payment_status, name='venue_payment_status'),

   

    path('user_transportation_list/', views.user_transportation_list, name='user_transportation_list'),
    path('transport/book/<int:service_id>/', views.book_transportation, name='book_transportation'),
    path('transport/bookings/', views.user_transport_bookings, name='user_transport_bookings'),
    path('transport/payment/<int:booking_id>/', views.transport_payment, name='transport_payment'),
    path('transportation_payment_status/', views.transportation_payment_status, name='transportation_payment_status'), 


    path('catering/', views.user_catering_list, name='user_catering_list'),
    path('catering/book/<int:catering_id>/', views.book_catering, name='book_catering'),
    path('catering/bookings/', views.user_catering_bookings, name='user_catering_bookings'),
    path('catering/payment/<int:booking_id>/', views.catering_payment, name='catering_payment'),
    path('catering_payment_status/', views.catering_payment_status, name='catering_payment_status'), 


    path("decorations/", views.decoration_list, name="decoration_list"),
    path("decorations/book/<int:decoration_id>/", views.book_decoration, name="book_decoration"),
    path("decorations/bookings/", views.user_decorations_bookings, name="user_decorations_bookings"),
    path("decorations/payment/<int:booking_id>/", views.decoration_payment, name="decoration_payment"),
    path("decorations/payment-status/", views.decoration_payment_status, name="decoration_payment_status"),


    path('photography/', views.photography_list, name='photography_list'),
    path('book_photography/<int:photography_id>/', views.book_photography, name='book_photography'),
    path('user/bookings/', views.user_photography_bookings, name='user_photography_bookings'),
    path('payment/<int:booking_id>/', views.photography_payment, name='photography_payment'),
    path('payment/status/', views.photography_payment_status, name='photography_payment_status'),

    path('bridal-groom/', views.bridal_groom_list, name='bridal_groom_list'),
    path('bridal-groom/book/<int:service_id>/', views.book_bridal_groom, name='book_bridal_groom'),
    path('bridal-groom/bookings/', views.user_bridal_groom_bookings, name='user_bridal_groom_bookings'),
    path('bridal-groom/payment/<int:booking_id>/', views.bridal_groom_payment, name='bridal_groom_payment'),
    path('bridal-groom/payment-status/', views.bridal_groom_payment_status, name='bridal_groom_payment_status'),


    path('whatsapp_url',views.whatsapp,name='whatsapp_url'),
    





    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='password_reset.html'), name='password_reset'),
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset_done/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'), name='password_reset_complete'),
]
