import base64

from django import forms
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import CreateView

from offers.models import Offer, Image


def offers_feed_view(request):
    return render(request=request, template_name="offers/offer_list.html")


def offer_details_view(request, pk):
    return HttpResponse(f"todo: show offer {pk} details")


class OfferCreateForm(forms.ModelForm):
    image = forms.ImageField(required=True)

    class Meta:
        model = Offer
        exclude = ('open', 'last_bump', 'owner',    'favorites',)


class OfferCreateView(CreateView):
    template_name = 'offers/offer_create.html'
    form_class = OfferCreateForm

    def get_success_url(self):
        return reverse('offers:offers_feed_view', kwargs={})

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.owner = self.request.user
        self.object.save()

        encoded_string = base64.b64encode(self.request.FILES.get('image').file.read())
        offer_image = Image(offer=self.object, base64_dump=encoded_string)
        offer_image.save()
        return HttpResponseRedirect(self.get_success_url())
