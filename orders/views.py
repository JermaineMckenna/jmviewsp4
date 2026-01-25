from django.contrib import messages # type: ignore
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin # type: ignore
from django.http import Http404 # type: ignore
from django.shortcuts import get_object_or_404, redirect # type: ignore
from django.urls import reverse_lazy # type: ignore
from django.views.decorators.http import require_POST # type: ignore
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView # type: ignore

from .forms import DeliverableForm, OrderForm, TestimonialForm
from .models import Deliverable, Order, Testimonial


class StaffRequiredMixin(UserPassesTestMixin):
	def test_func(self):
		return bool(self.request.user.is_staff)


class OrderAccessMixin:
	"""
	Staff can access any order.
	Customers can access only their own orders.
	"""

	def get_order_or_404(self) -> Order:
		order = get_object_or_404(
			Order.objects.select_related("service", "customer"),
			pk=self.kwargs["pk"],
		)
		if self.request.user.is_staff or order.customer == self.request.user:
			return order
		raise Http404("Not found")


class OrderListView(LoginRequiredMixin, ListView):
	template_name = "orders/order_list.html"
	context_object_name = "orders"

	def get_queryset(self):
		qs = Order.objects.select_related("service", "customer")
		return qs if self.request.user.is_staff else qs.filter(customer=self.request.user)


class OrderDetailView(LoginRequiredMixin, DetailView):
	template_name = "orders/order_detail.html"
	context_object_name = "order"
	model = Order

	def get_object(self, queryset=None):
		order = super().get_object(queryset)
		if self.request.user.is_staff or order.customer == self.request.user:
			return order
		raise Http404("Not found")


class OrderCreateView(LoginRequiredMixin, CreateView):
	template_name = "orders/order_form.html"
	form_class = OrderForm
	model = Order
	success_url = reverse_lazy("orders:order_list")

	def form_valid(self, form):
		form.instance.customer = self.request.user
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


class DeliverableCreateView(LoginRequiredMixin, StaffRequiredMixin, CreateView):
	"""
	Staff uploads a deliverable for an order.
	"""
	template_name = "orders/deliverable_form.html"
	form_class = DeliverableForm
	model = Deliverable

	def dispatch(self, request, *args, **kwargs):
		self.order = get_object_or_404(Order.objects.select_related("customer"), pk=kwargs["pk"])
		return super().dispatch(request, *args, **kwargs)

	def form_valid(self, form):
		form.instance.order = self.order
		form.instance.uploaded_by = self.request.user

		# Auto-mark delivered when staff uploads a deliverable
		if self.order.status in ("new", "in_progress"):
			self.order.status = "delivered"
			self.order.save(update_fields=["status", "updated_at"])

		messages.success(self.request, "Deliverable uploaded and attached to the order.")
		return super().form_valid(form)

	def get_success_url(self):
		return reverse_lazy("orders:order_detail", kwargs={"pk": self.order.pk})


@require_POST
def request_revision(request, pk):
	if not request.user.is_authenticated:
		return redirect("accounts:login")

	order = get_object_or_404(Order.objects.select_related("customer"), pk=pk)

	if request.user.is_staff:
		messages.info(request, "Staff can update status in admin or via edit.")
		return redirect("orders:order_detail", pk=pk)

	if order.customer != request.user:
		raise Http404("Not found")

	if order.status not in ("delivered", "revision_requested"):
		messages.error(request, "You can request a revision after delivery.")
		return redirect("orders:order_detail", pk=pk)

	order.status = "revision_requested"
	order.save(update_fields=["status", "updated_at"])
	messages.success(request, "Revision requested. We’ll review and update your order.")
	return redirect("orders:order_detail", pk=pk)


@require_POST
def mark_complete(request, pk):
	if not request.user.is_authenticated:
		return redirect("accounts:login")

	order = get_object_or_404(Order.objects.select_related("customer"), pk=pk)

	if request.user.is_staff:
		messages.info(request, "Staff can update status in admin or via edit.")
		return redirect("orders:order_detail", pk=pk)

	if order.customer != request.user:
		raise Http404("Not found")

	if order.status not in ("delivered", "revision_requested"):
		messages.error(request, "This order can’t be completed yet.")
		return redirect("orders:order_detail", pk=pk)

	order.status = "completed"
	order.save(update_fields=["status", "updated_at"])
	messages.success(request, "Marked as completed. You can now leave a testimonial.")
	return redirect("orders:order_detail", pk=pk)


class TestimonialCreateView(LoginRequiredMixin, CreateView):
	template_name = "orders/testimonial_form.html"
	form_class = TestimonialForm
	model = Testimonial

	def dispatch(self, request, *args, **kwargs):
		self.order = get_object_or_404(Order.objects.select_related("customer"), pk=kwargs["pk"])

		# Staff cannot create testimonials
		if request.user.is_staff:
			messages.info(request, "Only customers can submit testimonials.")
			return redirect("orders:order_detail", pk=self.order.pk)

		# Must own the order
		if self.order.customer != request.user:
			raise Http404("Not found")

		# Must be completed
		if self.order.status != "completed":
			messages.error(request, "You can leave a testimonial after marking the order as completed.")
			return redirect("orders:order_detail", pk=self.order.pk)

		# One testimonial per order
		if hasattr(self.order, "testimonial"):
			messages.info(request, "You’ve already left a testimonial for this order.")
			return redirect("orders:order_detail", pk=self.order.pk)

		return super().dispatch(request, *args, **kwargs)

	def form_valid(self, form):
		form.instance.order = self.order
		form.instance.customer = self.request.user
		messages.success(self.request, "Thanks! Your testimonial has been submitted for approval.")
		return super().form_valid(form)

	def get_success_url(self):
		return reverse_lazy("orders:order_detail", kwargs={"pk": self.order.pk})