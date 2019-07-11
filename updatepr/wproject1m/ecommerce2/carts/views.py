from django.shortcuts import render, redirect
from django.http import JsonResponse
# Create your views here.
from orders.models import Order

from accessories.models import Accessories
from .models import Cart, CartItem
from accounts.models import GuestEmail
from addresses.models import Address
from accounts.forms import LoginForm, GuestForm
from billing.models import BillingProfile
from product.models import Product
# from pproducts.models import P_Product

from django.contrib.auth import authenticate, login, get_user_model
from django.contrib.auth.models import User
from django.db.models.signals import pre_save, post_save
from django.conf import settings
from addresses.forms import AddressForm

import stripe
STRIPE_SECRET_KEY = getattr(settings, "STRIPE_SECRET_KEY", "sk_test_lvSCI8hToTF8CA3KnVmq7dad00BZELOC5N")
STRIPE_PUB_KEY = getattr(settings, "STRIPE_PUB_KEY", 'pk_test_fBDdAiUQExRLqP2m8aC1GKzk00IzmzodV8')

# def cart_create(user=None):
#     cart_obj = Cart.objects.create(user=None)
#     print("New Cart created")
#     return cart_obj
#
# def cart_detail_api_view(request):
#     cart_obj, new_obj = Cart.objects.new_or_get(request)
#     product = [{"name": x.name, "price": x.price} for x in cart_obj.product.all()]
#     cart_data = {"product": product, "subtotal": cart_obj.subtotal, "total": cart_obj.total}
#     return JsonResponse(cart_data)

def cart_home(request):
    cart_obj, new_obj = Cart.objects.new_or_get(request)
    # product = cart_obj.product.all()
    # total = 0
    # for x in product:
    #     total += x.price
    # print(total)
    # cart_obj.total =total
    # cart_obj.save()

    # # request.session['cart_id'] = "12"
    # #del request.session["cart_id"]
    # cart_id = request.session.get("cart_id", None)
    # # if cart_id is None: #and isinstance(cart_id, int):
    # #     cart_obj=cart_create()
    # #     #print("create new cart")
    # #     request.session['cart_id'] = cart_obj.id
    # # else:
    #     #if isinstance(cart_id, int):
    # qs = Cart.objects.filter(id=cart_id)
    # if qs.count() == 1:
    #     # print("Cart ID exists")
    #     cart_obj = qs.first()
    #     if request.user.is_authenticated and cart_obj.user is None:
    #         cart_obj.user = request.user
    #         cart_obj.save()
    # else:
    #     cart_obj =  Cart.objects.new(user = request.user)
    #     request.session['cart_id'] = cart_obj.id
        #     print(cart_id)
        # cart_obj = Cart.objects.get(id= cart_id)
    # print(request.session)
    # print(dir(request.session))
    # request.session.set_expiry(300)
    # key=request.session.session_key
    # print (key)
    #request.session['user'] = request.user.username
    return render(request, "carts/home.html", {"cart":cart_obj})



def cart_update(request):
    # print(request.POST)
    product_id= request.POST.get('product_id')

    # accessory_id=request.POST.get('accessories_id')

    # print(accessory_id)

    if product_id is not None:
        try:
            product_obj = Product.objects.get(id = product_id )
            # accessory_obj = Accessories.objects.get(id = accessory_id )

            # product_obj = P_Product.objects.get(id = product_id )

        except Product.DoesNotExist:
            print("Show message to user, product is gone?")
            return redirect("cart:home")
        cart_obj, new_obj = Cart.objects.new_or_get(request)
        # cart_obj.product.add(product_obj)
        if product_obj in cart_obj.product.all():
            cart_obj.product.remove(product_obj)
            added = False
        # if accessory_obj in cart_obj.product.all():
        #     cart_obj.product.remove(accessory_obj)
        else:
            cart_obj.product.add(product_obj)
            added = True
        request.session['cart_items'] = cart_obj.product.count()
        if request.is_ajax():
            print("Ajax Request")
            json_data = {
                "added": added,
                "removed": not added,
                "cartItemCount": cart_obj.product.count(),
            }
            return JsonResponse(json_data)




        # return redirect(product_obj.get_absolute_url())
    return redirect("cart:home")


def checkout_home(request):
    cart_obj, cart_created = Cart.objects.new_or_get(request)
    order_obj = None
    if cart_created or cart_obj.product.count() == 0:
        return redirect("cart:home")
    # else:
    #     order_obj, new_order_obj = Order.objects.get_or_create(cart = cart_obj)

    # user = request.user
    # billing_profile = None

    login_form = LoginForm()
    guest_form = GuestForm()
    address_form = AddressForm()
    billing_address_id = request.session.get("billing_address_id", None)

    shipping_address_id = request.session.get("shipping_address_id", None)

    # billing_address_form = AddressForm

    billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)
    address_qs = None
    has_card = False

    # guest_email_id = request.session.get('guest_email_id')
    # if user.is_authenticated:
    #     'logged in user checkout; remember payment stuff'
    #     billing_profile, billing_profile_created = BillingProfile.objects.get_or_create(user=user, email=user.email)
    # elif guest_email_id is not None:
    #     'guest user checkout; auto reloads payment stuff'
    #     guest_email_obj = GuestEmail.objects.get(id=guest_email_id)
    #     billing_pr ofile, billing_guest_profile_created = BillingProfile.objects.get_or_create(email=guest_email_obj.email)
    #
    # else:
    #     pass
    if billing_profile is not None:
        if request.user.is_authenticated:
            address_qs = Address.objects.filter(billing_profile=billing_profile)
        # shipping_address_qs = address_qs.filter(address_type='shipping')
        # billing_address_qs = address_qs.filter(address_type='billing')
        order_obj, order_obj_created = Order.objects.new_or_get(billing_profile, cart_obj)
        if shipping_address_id:
            order_obj.shipping_address = Address.objects.get(id=shipping_address_id)
            del request.session["shipping_address_id"]
        if billing_address_id:
            order_obj.billing_address = Address.objects.get(id=billing_address_id)
            del request.session["billing_address_id"]
        if billing_address_id or shipping_address_id:
            order_obj.save()
        has_card = billing_profile.has_card

    if request.method == "POST":
        "check that order is done"
        is_prepared = order_obj.check_done()
        if is_prepared:
            did_charge, crg_msg = billing_profile.charge(order_obj)
            if did_charge:
                order_obj.mark_paid()
                request.session['cart_items'] = 0
                del request.session['cart_id']
                return redirect("cart:success")
            else:
                print (crg_msg)
                return redirect("cart:checkout")
        # order_qs = Order.objects.filter(cart = cart_obj, active=True)
        # if order_qs.exists():
        #     order_qs.update(active=False)
        # else:
        #     order_obj = Order.objects.create(
        #                 billing_profile=billing_profile,
        #                 cart=cart_obj)



    context = {
        "object":order_obj,
        "billing_profile": billing_profile,
        "login_form": login_form,
        "guest_form":guest_form,
        "address_form": address_form,
        "address_qs": address_qs,
        "has_card":has_card,
        "publish_key": STRIPE_PUB_KEY
        # "billing_address_form": bill
        # ing_address_form,

    }


    return render(request, "carts/checkout.html", context)




def checkout_done_view(request):
    return render(request, "carts/checkout-done.html", {})