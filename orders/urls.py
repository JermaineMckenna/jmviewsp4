from django.urls import path  # type: ignore
from . import views

app_name = "orders"

urlpatterns = [
    path("", views.OrderListView.as_view(), name="order_list"),
    path("new/", views.OrderCreateView.as_view(), name="order_create"),
    path("<int:pk>/", views.OrderDetailView.as_view(), name="order_detail"),
    path("<int:pk>/edit/", views.OrderUpdateView.as_view(), name="order_update"),
    path("<int:pk>/delete/", views.OrderDeleteView.as_view(), name="order_delete"),

    # Staff: upload deliverables tied to an order
    path("<int:pk>/deliverables/new/", views.DeliverableCreateView.as_view(), name="deliverable_create"),

    # Customer: leave testimonial once completed
    path("<int:pk>/testimonial/", views.TestimonialCreateView.as_view(), name="testimonial_create"),

    # Customer: request a revision
    path("<int:pk>/request-revision/", views.request_revision, name="request_revision"),

    # Customer: mark as completed (after delivery)
    path("<int:pk>/mark-complete/", views.mark_complete, name="mark_complete"),
]