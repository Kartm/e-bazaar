import base64

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import CreateView, TemplateView

from offers.models import Offer, Image, District, City, Country


#def offers_feed_view(request):
#    return render(request=request, template_name="offers/offer_list.html")

class OfferFeedView(TemplateView):
    template_name = 'offers/offer_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        offers = []

        for offer in Offer.objects.all():
            offers.append((offer, Image.objects.filter(offer=offer.pk).first()))

        context['offers'] = offers
        return context


# def offer_details_view(request, pk):
#     return render(request=request, template_name="offers/offer_detail_view.html")
# todo well details are removed now



class OfferDetailView(TemplateView):
    template_name = 'offers/offer_detail_view.html'

    def get_context_data(self, **kwargs):
        pk = self.kwargs.get('pk')
        context = super().get_context_data(**kwargs)
        offer = Offer.objects.get(pk=pk)
        images = Image.objects.filter(offer=offer.pk)
        district = District.objects.get(pk=offer.district.pk)
        city = City.objects.get(pk=district.city.pk)
        country = Country.objects.get(pk=city.country.pk)
        context['offer'] = offer
        context['images'] = images
        context['district'] = district
        context['city'] = city
        context['country'] = country
        context['isFavorite'] = context['offer'].favorites.filter(pk=self.request.user.pk).exists()
        return context

    def post(self, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        bar = self.request.POST.get('favorite', None)
        if 'favorite' in self.request.POST:
            if context['offer'].favorites.filter(pk=self.request.user.pk).exists():
                context['offer'].favorites.remove(self.request.user)
            else:
                context['offer'].favorites.add(self.request.user)
            return HttpResponseRedirect(self.request.path)
        print(self.request.POST)
        return self.render_to_response(context)


class OfferCreateForm(forms.ModelForm):
    image = forms.ImageField(required=True)

    class Meta:
        model = Offer
        exclude = ('open', 'last_bump', 'owner', 'favorites',)
        labels = {'district': 'Location', 'subcategory': 'Category'}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.enctype = 'multipart/form-data'

        self.helper.add_input(Submit('submit', 'Submit'))


class OfferCreateView(CreateView):
    template_name = 'offers/offer_create.html'
    form_class = OfferCreateForm

    def get_success_url(self):
        return reverse('offers:offers_feed_view', kwargs={})

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.owner = self.request.user
        self.object.save()

        prefix = f"data:image/{str(self.request.FILES.get('image')).split('.')[-1]};base64,"
        encoded_string = base64.b64encode(self.request.FILES.get('image').file.read()).decode('utf-8')
        offer_image = Image(offer=self.object, base64_dump=f"{prefix}{encoded_string}")
        offer_image.save()
        return HttpResponseRedirect(self.get_success_url())
