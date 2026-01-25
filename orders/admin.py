from django.contrib import admin  # type: ignore
from .models import Service, Order, Deliverable, Testimonial


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ("name", "from_price_gbp", "active")
    list_filter = ("active",)
    search_fields = ("name",)


class DeliverableInline(admin.TabularInline):
    model = Deliverable
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("title", "service", "customer", "status", "created_at")
    list_filter = ("status", "service")
    search_fields = ("title", "brief", "customer__username", "customer__email")
    autocomplete_fields = ("customer",)
    inlines = [DeliverableInline]


@admin.register(Deliverable)
class DeliverableAdmin(admin.ModelAdmin):
    list_display = ("order", "created_at", "uploaded_by")
    search_fields = ("order__title", "order__customer__username")


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ("order", "customer", "rating", "approved", "created_at")
    list_filter = ("approved", "rating")
    search_fields = ("order__title", "customer__username", "content")