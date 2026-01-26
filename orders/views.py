from decimal import Decimal

from django.conf import settings  # type: ignore
from django.contrib import messages  # type: ignore
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin  # type: ignore
from django.http import Http404, HttpResponse  # type: ignore
from django.shortcuts import redirect, render  # type: ignore
from django.urls import reverse_lazy  # type: ignore
from django.views.decorators.csrf import csrf_exempt  # type: ignore
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView, View  # type: ignore

import stripe  # type: ignore

from .forms import DeliverableForm, OrderForm, TestimonialForm
from .models import Deliverable, Order, Testimonial


stripe.api_key = settings.STRIPE_SECRET_KEY


class OrderListView(LoginRequiredMixin, ListView):
	template_name = "orders/order_list.html"
	context_object_name = "orders"

	def get_queryset(self):
		qs = Order.objects.select_related("service", "customer")
		if self.request.user.is_staff:
			return qs
		return qs.filter(customer=self.request.user)


class OrderDetailView(LoginRequiredMixin, DetailView):
	template_name = "orders/order_detail.html"
	context_object_name = "order"
	model = Order

	def get_object(self, queryset=None):
		obj = super().get_object(queryset)
		if self.request.user.is_staff or obj.customer == self.request.user:
			return obj
		raise Http404("Not found")


class OrderCreateView(LoginRequiredMixin, CreateView):
	template_name = "orders/order_form.html"
	form_class = OrderForm
	model = Order
	success_url = reverse_lazy("orders:order_list")

	def form_valid(self, form):
		form.instance.customer = self.request.user
		# snapshot deposit from service (editable later in admin if needed)
		form.instance.deposit_amount_gbp = form.instance.service.deposit_gbp or Decimal("0.00")
		messages.success(self.request, "Enquiry sent. You’ll see it listed in your orders.")
		return super().form_valid(form)


class OrderUpdateView(LoginRequiredMixin, UpdateView):
	template_name = "orders/order_form.html"
	form_class = OrderForm
	model = Order
	success_url = reverse_lazy("orders:order_list")

	def get_object(self, queryset=None):
		obj = super().get_object(queryset)
		if self.request.user.is_staff or obj.customer == self.request.user:
			return obj
		raise Http404("Not found")

	def form_valid(self, form):
		messages.success(self.request, "Order updated.")
		return super().form_valid(form)


class OrderDeleteView(LoginRequiredMixin, DeleteView):
	template_name = "orders/order_confirm_delete.html"
	model = Order
	success_url = reverse_lazy("orders:order_list")

	def get_object(self, queryset=None):
		obj = super().get_object(queryset)
		if self.request.user.is_staff or obj.customer == self.request.user:
			return obj
		raise Http404("Not found")

	def delete(self, request, *args, **kwargs):
		messages.success(self.request, "Order deleted.")
		return super().delete(request, *args, **kwargs)


class StaffRequiredMixin(UserPassesTestMixin):
	def test_func(self):
		return bool(self.request.user.is_staff)


class DeliverableCreateView(LoginRequiredMixin, StaffRequiredMixin, CreateView):
	template_name = "orders/deliverable_form.html"
	form_class = DeliverableForm
	model = Deliverable

	def dispatch(self, request, *args, **kwargs):
		self.order = Order.objects.select_related("customer").get(pk=kwargs["pk"])
		return super().dispatch(request, *args, **kwargs)

	def form_valid(self, form):
		form.instance.order = self.order
		form.instance.uploaded_by = self.request.user

		if self.order.status in ("new", "in_progress"):
			self.order.status = "delivered"
			self.order.save(update_fields=["status", "updated_at"])

		messages.success(self.request, "Deliverable uploaded and attached to the order.")
		return super().form_valid(form)

	def get_success_url(self):
		return reverse_lazy("orders:order_detail", kwargs={"pk": self.order.pk})


def request_revision(request, pk):
	if not request.user.is_authenticated:
		return redirect("accounts:login")

	order = Order.objects.select_related("customer").get(pk=pk)
	if not (request.user.is_staff or order.customer == request.user):
		raise Http404("Not found")

	if request.user.is_staff:
		messages.info(request, "Staff can change status in admin or the edit screen.")
		return redirect("orders:order_detail", pk=pk)

	order.status = "revision_requested"
	order.save(update_fields=["status", "updated_at"])
	messages.success(request, "Revision requested. We’ll review and update your order.")
	return redirect("orders:order_detail", pk=pk)


def mark_complete(request, pk):
	if not request.user.is_authenticated:
		return redirect("accounts:login")

	order = Order.objects.select_related("customer").get(pk=pk)
	if not (request.user.is_staff or order.customer == request.user):
		raise Http404("Not found")

	if request.user.is_staff:
		messages.info(request, "Staff can change status in admin or the edit screen.")
		return redirect("orders:order_detail", pk=pk)

	if order.status not in ("delivered", "revision_requested"):
		messages.error(request, "This order can’t be completed yet.")
		return redirect("orders:order_detail", pk=pk)

	order.status = "completed"
	order.save(update_fields=["status", "updated_at"])
	messages.success(request, "Marked as completed.")
	return redirect("orders:order_detail", pk=pk)


class TestimonialCreateView(LoginRequiredMixin, CreateView):
	template_name = "orders/testimonial_form.html"
	form_class = TestimonialForm
	model = Testimonial

	def dispatch(self, request, *args, **kwargs):
		self.order = Order.objects.select_related("customer").get(pk=kwargs["pk"])

		if not (request.user.is_staff or self.order.customer == request.user):
			raise Http404("Not found")

		if request.user.is_staff:
			messages.info(request, "Only customers can submit testimonials.")
			return redirect("orders:order_detail", pk=self.order.pk)

		if self.order.status != "completed":
			messages.error(request, "You can leave a testimonial after marking the order as completed.")
			return redirect("orders:order_detail", pk=self.order.pk)

		if hasattr(self.order, "testimonial"):
			messages.info(request, "You’ve already left a testimonial for this order.")
			return redirect("orders:order_detail", pk=self.order.pk)

		return super().dispatch(request, *args, **kwargs)

	def form_valid(self, form):
		form.instance.order = self.order
		form.instance.customer = self.request.user
		messages.success(self.request, "Thanks! Your testimonial has been submitted.")
		return super().form_valid(form)

	def get_success_url(self):
		return reverse_lazy("orders:order_detail", kwargs={"pk": self.order.pk})


def _pence(amount: Decimal) -> int:
	return int((amount * Decimal("100")).quantize(Decimal("1")))


class PayDepositView(LoginRequiredMixin, View):
	def post(self, request, pk):
		order = Order.objects.select_related("customer", "service").get(pk=pk)
		if not (request.user.is_staff or order.customer == request.user):
			raise Http404("Not found")

		if order.deposit_paid:
			messages.info(request, "Deposit is already paid.")
			return redirect("orders:order_detail", pk=order.pk)

		if order.deposit_amount_gbp <= 0:
			messages.error(request, "This service has no deposit set.")
			return redirect("orders:order_detail", pk=order.pk)

		if not settings.STRIPE_SECRET_KEY:
			messages.error(request, "Stripe is not configured. Add STRIPE_SECRET_KEY in your environment.")
			return redirect("orders:order_detail", pk=order.pk)

		session = stripe.checkout.Session.create(
			mode="payment",
			payment_method_types=["card"],
			line_items=[
				{
					"price_data": {
						"currency": settings.STRIPE_CURRENCY,
						"product_data": {"name": f"JMViews Deposit — {order.service.name} (Order #{order.pk})"},
						"unit_amount": _pence(Decimal(order.deposit_amount_gbp)),
					},
					"quantity": 1,
				}
			],
			metadata={"order_id": str(order.pk), "payment_type": "deposit"},
			success_url=f"{settings.SITE_URL}{reverse_lazy('orders:payment_success')}?order={order.pk}",
			cancel_url=f"{settings.SITE_URL}{reverse_lazy('orders:payment_cancel')}?order={order.pk}",
		)

		order.stripe_deposit_session_id = session.id
		order.save(update_fields=["stripe_deposit_session_id", "updated_at"])
		return redirect(session.url)


class PayFinalView(LoginRequiredMixin, View):
	def post(self, request, pk):
		order = Order.objects.select_related("customer", "service").get(pk=pk)
		if not (request.user.is_staff or order.customer == request.user):
			raise Http404("Not found")

		if order.final_paid:
			messages.info(request, "Final balance is already paid.")
			return redirect("orders:order_detail", pk=order.pk)

		if not order.deposit_paid and order.deposit_amount_gbp > 0:
			messages.error(request, "Please pay the deposit first.")
			return redirect("orders:order_detail", pk=order.pk)

		if not order.final_amount_gbp or order.final_amount_gbp <= 0:
			messages.error(request, "Final amount hasn’t been set yet. Staff will set it in admin.")
			return redirect("orders:order_detail", pk=order.pk)

		if not settings.STRIPE_SECRET_KEY:
			messages.error(request, "Stripe is not configured. Add STRIPE_SECRET_KEY in your environment.")
			return redirect("orders:order_detail", pk=order.pk)

		session = stripe.checkout.Session.create(
			mode="payment",
			payment_method_types=["card"],
			line_items=[
				{
					"price_data": {
						"currency": settings.STRIPE_CURRENCY,
						"product_data": {"name": f"JMViews Final Payment — {order.service.name} (Order #{order.pk})"},
						"unit_amount": _pence(Decimal(order.final_amount_gbp)),
					},
					"quantity": 1,
				}
			],
			metadata={"order_id": str(order.pk), "payment_type": "final"},
			success_url=f"{settings.SITE_URL}{reverse_lazy('orders:payment_success')}?order={order.pk}",
			cancel_url=f"{settings.SITE_URL}{reverse_lazy('orders:payment_cancel')}?order={order.pk}",
		)

		order.stripe_final_session_id = session.id
		order.save(update_fields=["stripe_final_session_id", "updated_at"])
		return redirect(session.url)


def payment_success(request):
	return render(request, "orders/payment_success.html")


def payment_cancel(request):
	return render(request, "orders/payment_cancel.html")


@csrf_exempt
def stripe_webhook(request):
	if not settings.STRIPE_WEBHOOK_SECRET:
		return HttpResponse(status=400)

	payload = request.body
	sig_header = request.META.get("HTTP_STRIPE_SIGNATURE", "")

	try:
		event = stripe.Webhook.construct_event(payload, sig_header, settings.STRIPE_WEBHOOK_SECRET)
	except Exception:
		return HttpResponse(status=400)

	if event["type"] == "checkout.session.completed":
		session = event["data"]["object"]
		if session.get("payment_status") == "paid":
			order_id = session.get("metadata", {}).get("order_id")
			payment_type = session.get("metadata", {}).get("payment_type")

			if order_id and payment_type in ("deposit", "final"):
				try:
					order = Order.objects.get(pk=int(order_id))
					if payment_type == "deposit":
						order.deposit_paid = True
					if payment_type == "final":
						order.final_paid = True
					order.save(update_fields=["deposit_paid", "final_paid", "updated_at"])
				except Exception:
					pass

	return HttpResponse(status=200)