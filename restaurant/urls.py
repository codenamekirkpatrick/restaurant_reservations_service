from django.urls import path
from restaurant.apps import RestaurantConfig
from restaurant.views import (
    MainPageView,
    AboutPageView,
    MenuPageView,
    ContactPageView,
    BookingListView,
    BookingUpdateView,
    TableSelectionView,
    BookingCreateView,
)


app_name = RestaurantConfig.name


urlpatterns = [
    path("", MainPageView.as_view(), name="index"),
    path("about/", AboutPageView.as_view(), name="about"),
    path("menu/", MenuPageView.as_view(), name="menu"),
    path("contacts/", ContactPageView.as_view(), name="contacts"),
    # booking
    path("table_list/", TableSelectionView.as_view(), name="table_list"),
    path("booking_list/", BookingListView.as_view(), name="booking_list"),
    path(
        "booking/create/<int:table_id>/<date_reserved>/<time_reserved>/",
        BookingCreateView.as_view(),
        name="booking_create",
    ),
    path("booking/update/<int:pk>", BookingUpdateView.as_view(), name="booking_update"),
]
