from django.urls import path  # type: ignore
from . import views

app_name = "orders"

urlpatterns = [
    path("", views.OrderListView.as_view(), name="order_list"),
    path("new/", views.OrderCreateView.as_view(), name="order_create"),
    path("<int:pk>/", views.OrderDetailView.as_view(), name="order_detail"),
    path("<int:pk>/edit/", views.OrderUpdateView.as_view(), name="order_update"),
    path("<int:pk>/delete/", views.OrderDeleteView.as_view(), name="order_delete"),

    path("<int:pk>/deliverables/new/", views.DeliverableCreateView.as_view(), name="deliverable_create"),
    path("<int:pk>/testimonial/", views.TestimonialCreateView.as_view(), name="testimonial_create"),
    path("<int:pk>/request-revision/", views.request_revision, name="request_revision"),
    path("<int:pk>/mark-complete/", views.mark_complete, name="mark_complete"),

    # Payments
    path("<int:pk>/pay/deposit/", views.PayDepositView.as_view(), name="pay_deposit"),
    path("<int:pk>/pay/final/", views.PayFinalView.as_view(), name="pay_final"),
    path("payment/success/", views.payment_success, name="payment_success"),
    path("payment/cancel/", views.payment_cancel, name="payment_cancel"),
    path("stripe/webhook/", views.stripe_webhook, name="stripe_webhook"),
]