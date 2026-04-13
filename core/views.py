import csv
import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views import generic
from django.conf import settings
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponse
from django.template.loader import get_template
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.db.models import Sum, Q, Count
from django.utils import timezone
from datetime import timedelta
from io import BytesIO
from xhtml2pdf import pisa 
from django.db.models.functions import TruncDate

from .models import Service, Booking, Category, Review, ServiceCategory
from .forms import SignUpForm, UserEditForm, BookingForm, ServiceForm

# --- NEW PUBLIC VIEWS ---

def home_view(request):
    """Main Landing Page showing all available services"""
    services = Service.objects.all()
    return render(request, 'core/service_list.html', {'services': services})

def about_view(request):
    """Full information about the eGarage platform"""
    return render(request, 'core/about.html')

# --- NAVIGATION & AUTHENTICATION ---

@login_required
def dashboard_redirect(request):
    if request.user.is_superuser or request.user.role == 'admin':
        return redirect('/admin/')
    elif request.user.role == 'provider':
        return redirect('provider_dashboard')
    else:
        return redirect('customer_dashboard') # Fixed redirect to customer_dashboard

def signup_view(request):
    """Sachi rite signup karavi ne role assign karse ane login par redirect karse"""
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            # Form save karo (aa admin panel ma user create kari nakhse)
            user = form.save(commit=False)
            
            # HTML mathi role melvo (Customer/Provider)
            role = request.POST.get('role')
            if role:
                user.role = role
            
            user.save() # Have finalize save thase
            
            messages.success(request, "Registration successful! Have login karo.")
            return redirect('login') # Login page par redirect thase
        else:
            messages.error(request, "Validation error! Mahiti barobar check karo.")
    else:
        form = SignUpForm()
    
    return render(request, 'registration/signup.html', {'form': form})

@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = UserEditForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Your profile has been updated!")
            return redirect('customer_dashboard')
    else:
        form = UserEditForm(instance=request.user)
    return render(request, 'core/edit_profile.html', {'form': form})

# --- SERVICE & PRODUCT VIEWS ---

def service_list(request):
    query = request.GET.get('q')
    services = Service.objects.filter(Q(title__icontains=query) | Q(category__name__icontains=query)) if query else Service.objects.all()
    return render(request, 'core/service_list.html', {'services': services, 'query': query})

def service_detail_view(request, service_id):
    service = get_object_or_404(Service, id=service_id) 
    return render(request, 'core/service_detail.html', {'service': service})

# --- PROVIDER LOGIC ---

@login_required
def provider_dashboard(request):
    if request.user.role != 'provider':
        messages.error(request, "Access denied.")
        return redirect('home')

    bookings = Booking.objects.filter(service__provider=request.user).order_by('-booking_date')
    total_earnings = bookings.filter(is_paid=True).aggregate(total=Sum('service__price'))['total'] or 0

    # Chart Logic for last 7 days
    last_week = timezone.now() - timedelta(days=7)
    chart_data_raw = bookings.filter(booking_date__gte=last_week).annotate(date=TruncDate('booking_date')).values('date').annotate(count=Count('id')).order_by('date')
    labels = [data['date'].strftime('%d %b') for data in chart_data_raw]
    counts = [data['count'] for data in chart_data_raw]

    return render(request, 'core/provider_dashboard.html', {
        'bookings': bookings,
        'total_earnings': total_earnings,
        'chart_labels': json.dumps(labels),
        'chart_counts': json.dumps(counts),
        'active_count': bookings.count(),
    })

@login_required
def add_service(request):
    if request.user.role != 'provider': 
        return redirect('home')

    # MODEL MA ServiceCategory CHE, ETLE ANE FETCH KARO
    categories = ServiceCategory.objects.all() 

    if request.method == 'POST':
        form = ServiceForm(request.POST, request.FILES)
        if form.is_valid():
            service = form.save(commit=False)
            service.provider = request.user
            
            # HTML Dropdown mathi 'category' name vali ID melvavi
            category_id = request.POST.get('category')
            if category_id:
                # Proper model mathi object get karvo
                cat_obj = get_object_or_404(ServiceCategory, id=category_id)
                service.category = cat_obj
            
            service.save()
            messages.success(request, "Service added successfully!")
            return redirect('provider_dashboard')
        else:
            messages.error(request, "Error: Please check form data.")
    else:
        form = ServiceForm()

    return render(request, 'provider/add_service.html', {
        'form': form, 
        'categories': categories
    })
    
@login_required
def update_status(request, booking_id, new_status):
    booking = get_object_or_404(Booking, id=booking_id, service__provider=request.user)
    if new_status in ['pending', 'in_progress', 'completed']:
        booking.status = new_status
        booking.save()
        messages.success(request, f"Status updated to {new_status}.")
    return redirect('provider_dashboard')

@login_required
def export_bookings_csv(request):
    bookings = Booking.objects.filter(service__provider=request.user).order_by('-booking_date')
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="bookings.csv"'
    writer = csv.writer(response)
    writer.writerow(['Customer', 'Service', 'Date', 'Status', 'Paid'])
    for b in bookings:
        writer.writerow([b.customer.username, b.service.title, b.booking_date, b.status, b.is_paid])
    return response

# --- CUSTOMER & PAYMENT WORKFLOW ---

@login_required
def book_service(request, service_id):
    service = get_object_or_404(Service, id=service_id)
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.customer = request.user
            booking.service = service
            booking.save()
            return redirect('initiate_payment', booking_id=booking.id)
    return render(request, 'core/booking_page.html', {'service': service, 'form': BookingForm()})


@login_required
def customer_dashboard(request):
    bookings = Booking.objects.filter(customer=request.user).order_by('-booking_date')
    return render(request, 'core/dashboard.html', {'bookings': bookings})

@login_required
def service_history(request):
    """View to show the user's past booking history"""
    history = Booking.objects.filter(customer=request.user).order_by('-booking_date')
    return render(request, 'core/service_history.html', {'history': history})

@login_required
def track_service(request, booking_id):
    """View to track the real-time status of a specific booking"""
    booking = get_object_or_404(Booking, id=booking_id, customer=request.user)
    return render(request, 'core/track_service.html', {'booking': booking})

@login_required
def initiate_payment(request, booking_id):
    # ERROR FIX: 'user' ne badle 'customer' lakho
    booking = get_object_or_404(Booking, id=booking_id, customer=request.user)
    return render(request, 'core/payment_page.html', {'booking': booking})

@login_required
def payment_success_logic(request, booking_id):
    # 'user' ne badle 'customer' vapro kem ke tamara model ma customer field che
    booking = get_object_or_404(Booking, id=booking_id, customer=request.user)
    
    # Internal Simulation: Sidhu database update karo
    booking.is_paid = True
    booking.status = 'completed'
    booking.save()

    # Success message
    messages.success(request, f"Payment of ₹{booking.service.price} successful for {booking.service.title}!")
    
    # Dashboard par redirect karo
    return redirect('customer_dashboard')