from django.conf import settings  # type: ignore
from django.core.validators import MaxValueValidator, MinValueValidator  # type: ignore
from django.db import models  # type: ignore


class Service(models.Model):
	name = models.CharField(max_length=120, unique=True)
	description = models.TextField(blank=True)
	from_price_gbp = models.DecimalField(max_digits=8, decimal_places=2, default=0)
	active = models.BooleanField(default=True)

	class Meta:
		ordering = ["name"]

	def __str__(self) -> str:
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
		settings.AUTH_USER_MODEL,
		on_delete=models.CASCADE,
		related_name="orders",
	)
	service = models.ForeignKey(
		Service,
		on_delete=models.PROTECT,
		related_name="orders",
	)

	title = models.CharField(max_length=120)
	brief = models.TextField()
	size = models.CharField(max_length=60, blank=True)
	budget_gbp = models.DecimalField(
		max_digits=8,
		decimal_places=2,
		null=True,
		blank=True,
	)
	status = models.CharField(
		max_length=20,
		choices=STATUS_CHOICES,
		default="new",
	)

	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		ordering = ["-created_at"]

	def __str__(self) -> str:
		return f"#{self.pk} {self.title}"


class Deliverable(models.Model):
	"""
	Staff uploads final work here (or work-in-progress) and it becomes available to the customer.
	"""

	order = models.ForeignKey(
		Order,
		on_delete=models.CASCADE,
		related_name="deliverables",
	)
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

	def __str__(self) -> str:
		return f"Deliverable for Order #{self.order_id}"


class Testimonial(models.Model):
	"""Customer leaves feedback once the order is completed."""

	order = models.OneToOneField(
		Order,
		on_delete=models.CASCADE,
		related_name="testimonial",
	)
	customer = models.ForeignKey(
		settings.AUTH_USER_MODEL,
		on_delete=models.CASCADE,
		related_name="testimonials",
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

	def __str__(self) -> str:
		return f"Testimonial by {self.customer} for Order #{self.order_id}"