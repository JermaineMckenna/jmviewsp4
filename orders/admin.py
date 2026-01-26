from django.contrib import admin  # type: ignore
from .models import Service, Order, Deliverable, Testimonial


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ("name", "from_price_gbp", "deposit_gbp", "active")
    list_filter = ("active",)
    search_fields = ("name",)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "service",
        "customer",
        "status",
        "deposit_paid",
        "final_paid",
        "created_at",
    )
    list_filter = ("status", "service", "deposit_paid", "final_paid")
    search_fields = ("title", "brief", "customer__username", "customer__email")
    autocomplete_fields = ("customer",)
    readonly_fields = ("stripe_deposit_session_id", "stripe_final_session_id", "created_at", "updated_at")
    fieldsets = (
        ("Order", {"fields": ("customer", "service", "title", "brief", "size", "budget_gbp", "status")}),
        ("Payments", {"fields": ("deposit_amount_gbp", "final_amount_gbp", "deposit_paid", "final_paid")}),
        ("Stripe", {"fields": ("stripe_deposit_session_id", "stripe_final_session_id")}),
        ("Timestamps", {"fields": ("created_at", "updated_at")}),
    )


@admin.register(Deliverable)
class DeliverableAdmin(admin.ModelAdmin):
    list_display = ("order", "created_at", "uploaded_by")
    search_fields = ("order__title", "note")


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ("order", "customer", "rating", "approved", "created_at")
    list_filter = ("approved", "rating")
    search_fields = ("customer__username", "content", "order__title")