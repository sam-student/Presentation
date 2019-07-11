from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.shortcuts import reverse
from rate.models import Review
from product.models import Product
from rate.form import ReviewForm
import datetime

def review_detail(request, review_id):
    review = get_object_or_404(Review, pk=review_id)
    return render(request, 'review_detail.html', {'review': review})


def wine_list(request):
    wine_list = Product.objects.order_by('-title')
    context = {'wine_list':wine_list}
    return render(request, 'wine_list.html', context)


def wine_detail(request, wine_id):
    wine = get_object_or_404(Product, pk=wine_id)
    form = ReviewForm()
    return render(request, 'wine_detail.html', {'wine': wine, 'form': form})


def add_review(request, wine_id):
    wine = get_object_or_404(Product, pk=wine_id)
    form = ReviewForm(request.POST)
    if form.is_valid():
       # rating = request.POST['rating']
        comment = request.POST['comment']
        user_name = request.POST['user_name']
        review = Review()
        review.wine = wine
        review.user_name = user_name
        #review.rating = rating
        review.comment = comment
        review.pub_date = datetime.datetime.now()
        review.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # templates hits the Back button.
        return HttpResponseRedirect(reverse('wine_detail', args=(wine.id,)))

    return render(request, 'wine_detail.html', {'wine': wine, 'form': form})


