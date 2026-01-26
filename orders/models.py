from django.conf import settings  # type: ignore
from django.core.validators import MaxValueValidator, MinValueValidator  # type: ignore
from django.db import models  # type: ignore


class Service(models.Model):
	name = models.CharField(max_length=120, unique=True)
	description = models.TextField(blank=True)
	from_price_gbp = models.DecimalField(max_digits=8, decimal_places=2, default=0)
	deposit_gbp = models.DecimalField(max_digits=8, decimal_places=2, default=0)
	active = models.BooleanField(default=True)

	class Meta:
		ordering = ["name"]

	def __str__(self):
		return self.name


class Order(models.Model):
	STATUS_CHOICES = [
		("new", "New"),
		("in_progress", "In progress"),
		("delivered", "Delivered"),
		("revision_requested", "Revision requested"),
		("completed", "Completed"),
	]

	customer = models.ForeignKey(
		settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="orders"
	)
	service = models.ForeignKey(Service, on_delete=models.PROTECT, related_name="orders")

	title = models.CharField(max_length=120)
	brief = models.TextField()
	size = models.CharField(max_length=60, blank=True)
	budget_gbp = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
	status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="new")

	# Payments
	deposit_amount_gbp = models.DecimalField(max_digits=8, decimal_places=2, default=0)
	final_amount_gbp = models.DecimalField(
		max_digits=8, decimal_places=2, null=True, blank=True
	)

	deposit_paid = models.BooleanField(default=False)
	final_paid = models.BooleanField(default=False)

	stripe_deposit_session_id = models.CharField(max_length=255, blank=True)
	stripe_final_session_id = models.CharField(max_length=255, blank=True)

	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		ordering = ["-created_at"]

	def __str__(self):
		return f"#{self.pk} {self.title}"


class Deliverable(models.Model):
	order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="deliverables")
	file = models.FileField(upload_to="deliverables/%Y/%m/")
	note = models.CharField(max_length=200, blank=True)
	uploaded_by = models.ForeignKey(
		settings.AUTH_USER_MODEL,
		on_delete=models.SET_NULL,
		null=True,
		blank=True,
		related_name="uploaded_deliverables",
	)
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ["-created_at"]

	def __str__(self):
		return f"Deliverable for Order #{self.order_id}"


class Testimonial(models.Model):
	order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name="testimonial")
	customer = models.ForeignKey(
		settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="testimonials"
	)
	rating = models.PositiveSmallIntegerField(
		default=5,
		validators=[MinValueValidator(1), MaxValueValidator(5)],
	)
	content = models.TextField()
	approved = models.BooleanField(default=False)
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ["-created_at"]

	def __str__(self):
		return f"Testimonial by {self.customer} for Order #{self.order_id}"