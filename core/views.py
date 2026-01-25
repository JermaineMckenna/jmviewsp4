from django.shortcuts import render  # type: ignore
from orders.models import Service, Testimonial  # type: ignore


def home(request):
    services = Service.objects.filter(active=True).order_by("name")[:4]
    testimonials = (
        Testimonial.objects.filter(approved=True)
        .select_related("order", "customer", "order__service")
        .order_by("-created_at")[:3]
    )
    return render(
        request,
        "core/home.html",
        {"services": services, "testimonials": testimonials},
    )


def services(request):
    services_qs = Service.objects.filter(active=True).order_by("name")
    return render(request, "core/services.html", {"services": services_qs})


def portfolio(request):
    testimonials = (
        Testimonial.objects.filter(approved=True)
        .select_related("order", "customer", "order__service")
        .order_by("-created_at")
    )
    return render(request, "core/portfolio.html", {"testimonials": testimonials})


# --- Portfolio collections (new pages) ---
def portfolio_visual(request):
    return render(request, "core/portfolio_visual.html")


def portfolio_aerial(request):
    return render(request, "core/portfolio_aerial.html")


def portfolio_digital(request):
    return render(request, "core/portfolio_digital.html")


def about(request):
    return render(request, "core/about.html")


def contact(request):
    return render(request, "core/contact.html")