import json
from .models import Customer, Product, Order, User


def cookieCart(request):
    # in order to create cart for anonymous user
    order_items = []
    order = {"get_total_order_items": 0,
             "get_total_price": 0, "shipping": False}

    try:
        cart = json.loads(request.COOKIES['cart'])
    except:
        # try to avoid error case when cookie is empty
        cart = {}

    for k, v in cart.items():
        try:
            order["get_total_order_items"] += v["quantity"]
            product = Product.objects.get(id=k)
            order["get_total_price"] += (product.price * v["quantity"])

            item = {
                "product": {
                    "id": product.id,
                    "name": product.name,
                    "price": product.price,
                    "digital": product.digital,
                    "image": product.image
                },
                "quantity": v["quantity"],
                "get_total": (product.price * v["quantity"])
            }
            order_items.append(item)

            if product.digital is False:
                order["shipping"] = True
        except:
            # if the item is in cookie and it also was deleted from DB => error case
            # this except is to avoid that case
            pass

    return {"order": order, "order_items": order_items}


def cartData(request):
    data = {}

    if request.user.is_authenticated:
        try:
            # because customer is one to one field of user model, so from user model we can refer to customer model
            customer = request.user.customer
        except:
            # make current user become customer if they are not
            user = User.objects.get(username=request.user)

            # when create new customer => it will return a tuple (<Customer: longle>, True)
            # so we need to access first element in order to actually use customer object
            customer = Customer.objects.get_or_create(
                user=user,
                name=user.username,
                email=user.email
            )[0]
        # if there is no order for current user => create a new one
        order, created = Order.objects.get_or_create(
            customer=customer, complete=False)
        # collect all order_items from oder
        order_items = order.orderitem_set.all()
    else:
        cookie_cart = cookieCart(request)

        order = cookie_cart["order"]
        order_items = cookie_cart["order_items"]

    return {"order": order, "order_items": order_items}
