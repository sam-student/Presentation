from django.views.generic import ListView, DetailView
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from billing.models import BillingProfile
from .models import Order
from django.http import Http404


# Create your views here.


class OrderListView(LoginRequiredMixin, ListView):

    def get_queryset(self):
        return Order.objects.by_request(self.request)

class OrderDetailView(LoginRequiredMixin, DetailView):

    def get_object(self):
        qs =Order.objects.by_request(self.request).filter(order_id = self.kwargs.get('order_id'))
        if qs.count() == 1:
            return qs.first()
        raise Http404


