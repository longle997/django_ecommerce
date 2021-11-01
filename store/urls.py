from django.urls import path
from .views import (
    store,
    cart,
    checkout,
    updateItem,
    processOrder,
    detail
)

urlpatterns = [
    path('', store, name="store"),
    # In this case we use '<int:pk>' to capture the item id, which must be a specially formatted string and pass it to the view as a parameter named pk (short for primary key).
    path('detail/<int:pk>/', detail, name="detail"),
    path('cart/', cart, name="cart"),
    path('checkout/', checkout, name="checkout"),
    path('cart/update-item/', updateItem, name="update-item"),
    path('process-order/', processOrder, name="process-order"),
]
