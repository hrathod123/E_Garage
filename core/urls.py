from django.urls import path
from . import views

urlpatterns = [
    # --- NEW PUBLIC LANDING & INFO ---
    path('', views.home_view, name='home'),
    path('about/', views.about_view, name='about'),
    
    # --- SERVICES & EXPLORE ---
    path('services/', views.service_list, name='service_list'),
    path('service/<int:service_id>/', views.service_detail_view, name='view_details'),
    path('service/pk/<int:service_id>/', views.service_detail_view, name='service_detail'),
    
    # --- PROVIDER WORKFLOW ---
    path('provider/dashboard/', views.provider_dashboard, name='provider_dashboard'),
    path('provider/add-service/', views.add_service, name='add_service'), 
    path('update-status/<int:booking_id>/<str:new_status>/', views.update_status, name='update_status'),
    path('dashboard/export/', views.export_bookings_csv, name='export_bookings_csv'),

    # --- CUSTOMER WORKFLOW ---
    path('book/<int:service_id>/', views.book_service, name='book_service'),
    path('dashboard/', views.customer_dashboard, name='customer_dashboard'), 
    path('dashboard-redirect/', views.dashboard_redirect, name='dashboard_redirect'),
    path('my-history/', views.service_history, name='service_history'),
    path('track/<int:booking_id>/', views.track_service, name='track_service'),

    # --- AUTH & PROFILE ---
    path('signup/', views.signup_view, name='signup'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),

    # ADD THESE TWO LINES:
    path('payment/initiate/<int:booking_id>/', views.initiate_payment, name='initiate_payment'),
    path('payment/success/<int:booking_id>/', views.payment_success_logic, name='payment_success_logic'),
]