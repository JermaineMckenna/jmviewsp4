from django.urls import path  # type: ignore
from . import views

app_name = "core"

urlpatterns = [
    path("", views.home, name="home"),
    path("services/", views.services, name="services"),

    # Portfolio hub + collections
    path("portfolio/", views.portfolio, name="portfolio"),
    path("portfolio/visual-photography/", views.portfolio_visual, name="portfolio_visual"),
    path("portfolio/aerial-cinematography/", views.portfolio_aerial, name="portfolio_aerial"),
    path("portfolio/digital-projects/", views.portfolio_digital, name="portfolio_digital"),

    path("about/", views.about, name="about"),
    path("contact/", views.contact, name="contact"),
]