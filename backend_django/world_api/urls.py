from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import (CityViewSet, continent_list, country, country_list,
                    region_list)

app_name = "world_api"

city_router = SimpleRouter()
city_router.register("", CityViewSet, basename="city")


urlpatterns = [
    path("cities/", include(city_router.urls)),
    path("", continent_list, name="continent-list"),
    path("<continent>/", region_list, name="region-list"),
    path("<continent>/<region>/", country_list, name="country-list"),
    path("<continent>/<region>/<code>/", country, name="country-detail"),
]
