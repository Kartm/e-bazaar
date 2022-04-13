from django.http import HttpResponse


def offers_feed_view(request):
    return HttpResponse(f"todo: show feed")


def offer_details_view(request, pk):
    return HttpResponse(f"todo: show offer {pk} details")


def offer_create_view(request):
    return HttpResponse(f"todo: offer creator")
