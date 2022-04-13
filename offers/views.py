from django import forms
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views.generic import FormView, CreateView

from offers.models import Offer


def offers_feed_view(request):
    return render(request=request, template_name="offers/offer_list.html")


def offer_details_view(request, pk):
    return HttpResponse(f"todo: show offer {pk} details")


class OfferCreateForm(forms.ModelForm):
    image = forms.ImageField(required=True)

    class Meta:
        model = Offer
        exclude = ('open', 'last_bump', 'owner',    'favorites',)

    def __init__(self, *args, **kwargs):
        # self.user = kwargs.pop('user')
        # print(kwargs)
        super(OfferCreateForm, self).__init__(*args, **kwargs)

    # def clean_title(self):
    #     title = self.cleaned_data['title']
    #     if Offer.objects.filter(user=self.user, title=title).exists():
    #         raise forms.ValidationError("You have already written a book with same title.")
    #     return title

class OfferCreateView(CreateView):
    template_name = 'offers/offer_create.html'
    form_class = OfferCreateForm

    def get_success_url(self):
        return reverse('offers:offers_feed_view', kwargs={})

    def form_valid(self, form):
        print(self.request)
        self.object = form.save(commit=False)
        self.object.owner = self.request.user
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())
    #
    # def get_initial(self, *args, **kwargs):
    #     initial = super(OfferCreateView, self).get_initial(**kwargs)
    #     initial['title'] = 'My Title'
    #     return initial
    #
    # def get_form_kwargs(self, *args, **kwargs):
    #     kwargs = super(OfferCreateView, self).get_form_kwargs(*args, **kwargs)
    #     kwargs['user'] = self.request.user
    #     return kwargs