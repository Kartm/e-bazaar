from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.utils import timezone
from django.views.generic import TemplateView

from offers.models import Offer
from .forms import NewUserForm
from django.contrib.auth import login, authenticate, logout, get_user_model
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm


def register_request(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect(".")
        messages.error(request, "Unsuccessful registration. Invalid information.")
    form = NewUserForm()
    return render(request=request, template_name="users/register.html", context={"register_form": form})


def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect(".")
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(request=request, template_name="users/login.html", context={"login_form": form})


def logout_request(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect(".")


class UserProfileView(TemplateView):
    template_name = "users/user_profile_view.html"

    def get_context_data(self, **kwargs):
        pk = self.kwargs.get('pk')
        context = super().get_context_data(**kwargs)
        user = get_user_model().objects.get(pk=pk)
        offers = Offer.objects.filter(owner_id=pk)
        context['profile_user'] = user
        context['is_profile_user_me'] = pk == self.request.user.pk
        context['profile_user_offers'] = offers
        return context

    def post(self, *args, **kwargs):
        context = self.get_context_data(**kwargs)

        if not context['is_profile_user_me']:
            return HttpResponseRedirect(self.request.path)

        if 'action' in self.request.POST and 'offer_id' in self.request.POST:
            action = self.request.POST.get('action')
            offer_id = self.request.POST.get('offer_id')

            if action == 'Bump':
                Offer.objects.filter(pk=offer_id).update(last_bump=timezone.now())
            elif action == 'Close':
                print('CLOSE')
            return HttpResponseRedirect(self.request.path)
        return self.render_to_response(context)


class FavoritesView(TemplateView):
    template_name = "users/favorites_view.html"

    def get_context_data(self, **kwargs):
        user_pk = self.request.user.pk
        context = super().get_context_data(**kwargs)

        favourites = Offer.objects.filter(favorites__pk=user_pk)
        print(user_pk)
        for fav in favourites:
            print(fav.title)
        print(favourites.all())

        context['favourites'] = favourites

        return context
