import base64
import io
import urllib

from django.views.generic import TemplateView

from offers.models import Offer
import matplotlib.pyplot as plt


class StatsView(TemplateView):
    template_name = "stats/stats_view.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        category_names = list(Offer.objects.all().values_list('subcategory__category__name', flat=True))

        counted = dict((x, category_names.count(x)) for x in set(category_names))

        labels = list(counted.keys())
        sizes = list(counted.values())

        fig1, ax1 = plt.subplots()
        ax1.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
        ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

        chart_bytes = io.BytesIO()
        plt.savefig(chart_bytes, format='png')
        chart_bytes.seek(0)
        pic_hash = base64.b64encode(chart_bytes.read())

        chart_image_uri = 'data:image/png;base64,' + urllib.parse.quote(pic_hash)

        context['chart_image'] = chart_image_uri
        return context
