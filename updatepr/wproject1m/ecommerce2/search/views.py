from django.shortcuts import render
from django.views.generic import ListView

# Create your views here.
from product.models import Product

class SearchProductView(ListView):
    #queryset = product.objects.all()
    template_name = "search/view.html"

    def get_context_data(self, *args, **kwargs):
        context=super(SearchProductView , self).get_context_data(*args, **kwargs)
        query = self.request.GET.get("q")
        query1 = self.request.GET.get("q1")
        query2 = self.request.GET.get("q2")

        # query1 = self.request.GET.get("q2")
        context["query"] = query
        context["query1"] = query1
        context["query2"] = query2


        #SearchQuery.objects.create(query=query)

        return context

    def get_queryset(self, *args, **kwargs ):
        request = self.request
        method_dict = request.GET
        query = method_dict.get("q", None)
        query1 = method_dict.get("q1", None)
        query2 = method_dict.get("q2", None)


        #print(query)
        if query is not None:
            return Product.objects.filter(title__icontains=query)
                                          # , price__icontains = query1, processor__icontains=query2)
            # result2=product.objects.filter(memory__icontains=query2)

            # return result1
            # return product.objects.filter(price__icontains=query)
            # return product.objects.filter(memory__icontains=query)

        return Products.objects.featured()
        #return product.objects.filter(title__icontains="samsung")