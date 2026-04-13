from django.contrib import admin
from django.db.models import Sum, Avg
from django.utils import timezone
from datetime import timedelta
from django.urls import reverse
from django.utils.safestring import mark_safe

# Unfold & Import-Export Imports
from unfold.admin import ModelAdmin
from unfold.sites import UnfoldAdminSite
from unfold.contrib.import_export.forms import ExportForm, ImportForm
from import_export.admin import ImportExportModelAdmin

from .models import User, Category, ServiceCategory, Service, Booking, Review

class EGarageAdminSite(UnfoldAdminSite):
    def index(self, request, extra_context=None):
        # 1. Summary Metrics
        total_revenue = Booking.objects.filter(is_paid=True).aggregate(t=Sum('service__price'))['t'] or 0
        active_bookings = Booking.objects.exclude(status='completed').count()
        total_clients = User.objects.filter(is_staff=False).count()

        # 2. Performance Chart Data (Last 12 Days)
        labels, data_gross, data_realized, data_avg = [], [], [], []
        
        for i in range(11, -1, -1):
            date = timezone.now().date() - timedelta(days=i)
            labels.append(date.strftime('%b %d'))
            
            # Gross Sales (All Bookings)
            gross = Booking.objects.filter(booking_date__date=date).aggregate(s=Sum('service__price'))['s'] or 0
            data_gross.append(float(gross))
            
            # Realized Revenue (Paid Only)
            paid = Booking.objects.filter(booking_date__date=date, is_paid=True).aggregate(s=Sum('service__price'))['s'] or 0
            data_realized.append(float(paid))
            
            # Average Value Trend
            avg_val = Booking.objects.filter(booking_date__date=date).aggregate(a=Avg('service__price'))['a'] or 0
            data_avg.append(float(avg_val))

        extra_context = extra_context or {}
        extra_context.update({
            'total_sales': f"{total_revenue:,}",
            'active_bookings': active_bookings,
            'total_customers': total_clients,
            'recent_bookings': Booking.objects.select_related('customer', 'service', 'service__category').order_by('-id')[:5],
            'labels': labels,
            'data_a': data_gross,
            'data_b': data_realized,
            'data_c': data_avg,
        })
        return super().index(request, extra_context)

admin_site = EGarageAdminSite(name='egarage_admin')

# --- Model Registrations (Full Functionality) ---

@admin.register(Booking, site=admin_site)
class BookingAdmin(ModelAdmin, ImportExportModelAdmin):
    list_display = ('id', 'customer', 'service', 'status', 'is_paid')
    list_editable = ('status', 'is_paid')
    list_filter = ('status', 'is_paid')

@admin.register(Service, site=admin_site)
class ServiceAdmin(ModelAdmin, ImportExportModelAdmin):
    list_display = ('title', 'provider', 'price', 'category')
    search_fields = ["title"]
    list_filter = ["category"]
    list_editable = ["price"]
    import_form_class = ImportForm
    export_form_class = ExportForm

@admin.register(User, site=admin_site)
class UserAdmin(ModelAdmin):
    list_display = ["username", "email", "role", "is_staff"]
    search_fields = ["username", "email"]
    list_filter = ["role", "is_staff"]

@admin.register(Category, site=admin_site)
class CategoryAdmin(ModelAdmin):
    list_display = ["name"]
    search_fields = ["name"]

@admin.register(ServiceCategory, site=admin_site)
class ServiceCategoryAdmin(ModelAdmin):
    list_display = ["name"]
    search_fields = ["name"]

@admin.register(Review, site=admin_site)
class ReviewAdmin(ModelAdmin):
    list_display = ('customer', 'rating', 'created_at')