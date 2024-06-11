from django.urls import path
from . import views

urlpatterns = [
    # Other URLs
    path('wishlist/', views.wishlist, name='wishlist'),


    path('add_to_wishlist/', views.add_to_wishlist, name='add_to_wishlist'),
    path('remove_from_wishlist/', views.remove_from_wishlist, name='remove_from_wishlist'),
    path('wishlist_to_cart/', views.wishlist_to_cart, name='wishlist_to_cart'),




    # Other URLs
]
