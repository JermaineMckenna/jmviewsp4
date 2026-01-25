from django import forms  # type: ignore
from .models import Order, Deliverable, Testimonial, Service


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ["service", "title", "brief", "size", "budget_gbp"]
        widgets = {
            "brief": forms.Textarea(attrs={"rows": 6}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Only show active services in the dropdown
        self.fields["service"].queryset = Service.objects.filter(active=True)


class DeliverableForm(forms.ModelForm):
    class Meta:
        model = Deliverable
        fields = ["file", "note"]


class TestimonialForm(forms.ModelForm):
    class Meta:
        model = Testimonial
        fields = ["rating", "content"]
        widgets = {
            "content": forms.Textarea(attrs={"rows": 5}),
        }

    def clean_rating(self):
        rating = self.cleaned_data.get("rating", 5)
        if rating < 1 or rating > 5:
            raise forms.ValidationError("Rating must be between 1 and 5.")
        return rating