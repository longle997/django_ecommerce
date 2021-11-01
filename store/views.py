import json

from datetime import datetime
from django.http.response import Http404
from django.shortcuts import render
from django.http import JsonResponse

from .models import Customer, ShippingAddress, OrderItem, Product, Order
from .utils import cartData, cookieCart


def store(request):
    products = Product.objects.all()
    data = cartData(request)
    order = data["order"]

    context = {
        "products": products,
        "order": order,
    }
    return render(
        request, 'store/store.html', context
    )


def cart(request):
    data = cartData(request)

    order = data["order"]
    order_items = data["order_items"]

    context = {
        "order": order,
        "order_items": order_items,
    }
    return render(
        request, 'store/cart.html', context
    )


def checkout(request):
    data = cartData(request)

    order = data["order"]
    order_items = data["order_items"]

    context = {
        "order": order,
        "order_items": order_items,
    }
    return render(
        request, 'store/checkout.html', context
    )


def updateItem(request):
    '''
    update order table base on action from user
    add action => increase order_item quantity
    remove action => decrease order_item quantity
    '''
    request_json = json.load(request)

    product = Product.objects.get(id=request_json["productId"])
    action = request_json["action"]
    customer = request.user.customer

    order, created = Order.objects.get_or_create(
        customer=customer, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(
        product=product, order=order)

    if action == "add":
        orderItem.quantity += 1
    elif action == "remove":
        orderItem.quantity -= 1

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    # In order to allow non-dict objects to be serialized set the safe parameter to False
    return JsonResponse("Update Item view", safe=False)


def processOrder(request):
    '''
    this view was called from checkout.html
    in order to save order to DB with all necessary infomation
    '''
    transaction_id = datetime.now().timestamp()
    # receive data from checkout.html -> submitFormData function
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        # get current order
        order, created = Order.objects.get_or_create(
            customer=customer, complete=False)
        # checkout.html -> 'form':userFormData
        total = float(data['form']['total'])
        order.transaction_id = transaction_id

        # compare "total" from request and "total" from DB
        if total == order.get_total_order_items:
            order.complete = True

        # after modify any attribute of order object => use save method to save change to DB
        order.save()

        # check if there are any order item with "digital" = True
        if order.shipping is True:
            ShippingAddress.objects.get_or_create(
                customer=customer,
                order=order,
                address=data['shipping']['address'],
                city=data['shipping']['city'],
                state=data['shipping']['state'],
                zipcode=data['shipping']['zipcode'],
            )
    else:
        print('User is not logged in')

        print('COOKIES:', request.COOKIES)

        # get data from data form (checkout.html)
        name = data["form"]["name"]
        email = data["form"]["email"]

        # get data from cookie
        cookieData = cookieCart(request)
        order_items = cookieData["order_items"]

        # only create a customer, not a user
        # if anonymous visit our page multiple time, we already have customer profile for them
        customer, created = Customer.objects.get_or_create(email=email)
        customer.name = name
        customer.save()

        # we use create instead of get_or_create because we haven't create any order until this time
        order = Order.objects.create(
            customer=customer,
            complete=False
        )

        for item in order_items:
            # get product from DB
            product = Product.objects.get(id=item["product"]["id"])

            order_item = OrderItem.objects.create(
                product=product,
                order=order,
                quantity=item["quantity"]
            )

        order.transaction_id = transaction_id
        total = float(data['form']['total'])

        # compare total from data form with total from DB
        if total == order.get_total_order_items:
            order.complete = True

        order.save()

        # check if there are any order item with "digital" = True
        if order.shipping is True:
            ShippingAddress.objects.get_or_create(
                customer=customer,
                order=order,
                address=data['shipping']['address'],
                city=data['shipping']['city'],
                state=data['shipping']['state'],
                zipcode=data['shipping']['zipcode'],
            )

    return JsonResponse('Payment submitted..', safe=False)


def detail(request, pk):
    try:
        product = Product.objects.get(pk=pk)
    except Product.DoesNotExist:
        raise Http404(f"product with  id {pk} does not exist!")

    return render(request, template_name="store/product_detail.html", context={"product": product})
