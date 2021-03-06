import base64

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import CreateView, TemplateView
from django.contrib.auth import get_user_model

from offers.models import Offer, Image, District, City, Country, Category, Subcategory
from users.models import Contact


#def offers_feed_view(request):
#    return render(request=request, template_name="offers/offer_list.html")

class OfferFeedView(TemplateView):
    template_name = 'offers/offer_list.html'

    sortFunction = {
        #'relevance': (???),
        'asc': (lambda item: item[0].price),
        'desc': (lambda item: -item[0].price)
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        offers = []

        for offer in Offer.active_offer_objects.all():
            offers.append((offer, Image.objects.filter(offer=offer.pk).first()))

        context['offers'] = offers
        context['categories'] = Category.objects.all()
        return context

    def get(self, *args, **kwargs):
        context = self.get_context_data(**kwargs)

        # filters
        low = float(self.request.GET.get('low', '0') or '0') - 0.05
        high = float(self.request.GET.get('high', 'inf') or 'inf')
        search = self.request.GET.get('search', '')

        #print(self.request.GET.getlist('interest[]', 'Nothing here'))
        category_list = self.request.GET.getlist('category[]', None)
        if category_list:
            checked_category_pks = [category.pk for category in Category.objects.filter(name__in=category_list)]
            checked_subcategory_pks = [subcategory.pk for subcategory in Subcategory.objects.filter(category__in=checked_category_pks)]

        context['offers'] = list(filter(
            lambda item: low <= item[0].price <= high and search.lower() in item[0].title.lower() and
                         (not category_list or item[0].subcategory.pk in checked_subcategory_pks),
            context['offers']))

        # sorting
        sortby = self.request.GET.get('sortby', None)
        if sortby in self.sortFunction.keys():
            context['offers'].sort(key=self.sortFunction[sortby])

        return self.render_to_response(context)


class OfferDetailView(TemplateView):
    template_name = 'offers/offer_detail_view.html'

    def get_context_data(self, **kwargs):
        offer_pk = self.kwargs.get('pk')
        context = super().get_context_data(**kwargs)
        offer = Offer.active_offer_objects.get(pk=offer_pk)
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
        try:
            context['contact_info'] = get_user_model().objects.get(pk=offer.owner.pk).contact.info
        except Contact.DoesNotExist:
            context['contact_info'] = "No contact info"
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
    images = forms.FileField(required=True, widget=forms.ClearableFileInput(attrs={'multiple': True}))

    class Meta:
        model = Offer
        exclude = ('open', 'last_bump', 'owner', 'favorites',)
        labels = {'district': 'Location', 'subcategory': 'Category'}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()


class OfferCreateView(CreateView):
    template_name = 'offers/offer_create.html'
    form_class = OfferCreateForm

    def get_success_url(self):
        return reverse('offers:offers_feed_view', kwargs={})

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.owner = self.request.user
        self.object.save()

        for image in self.request.FILES.getlist('images'):
            prefix = f"data:image/{str(image).split('.')[-1]};base64,"
            encoded_string = base64.b64encode(image.file.read()).decode('utf-8')
            Image.objects.create(offer=self.object, base64_dump=f"{prefix}{encoded_string}")

        return HttpResponseRedirect(self.get_success_url())
