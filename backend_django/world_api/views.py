from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.utils.text import slugify

from .models import City, Country
from .serializers import CitySerializer, CountrySerializer


def find_original(slug, collection):
    return next(e for e in collection if slugify(e) == slug)


@api_view(["GET"])
def continent_list(request):
    continents = Country.CONTINENTS
    continents.sort()
    response = [{
        "name": continent, "code": slugify(continent)
    } for continent in continents]
    return Response(response)


@api_view(["GET"])
def region_list(request, continent):
    continent_name = find_original(continent, Country.CONTINENTS)
    queryset = Country.objects.filter(continent=continent_name).values_list(
        "region", flat=True
    ).distinct().order_by("region")

    regions = [
        {"name": region, "code": slugify(region)} for region in queryset
    ]
    return Response(regions)


@api_view(["GET"])
def country_list(request, continent, region):
    continent_name = find_original(continent, Country.CONTINENTS)

    regions = Country.objects.filter(continent=continent_name).values_list(
        "region", flat=True
    ).distinct()
    region_name = find_original(region, regions)

    queryset = Country.objects.filter(
        continent=continent_name, region=region_name
    ).order_by("name")

    countries = [
        {"code": country.code, "name": country.name} for country in queryset
    ]
    return Response(countries)


@api_view(["GET"])
def country(request, continent, region, code):
    country = Country.objects.get(pk=code)
    return Response(CountrySerializer(country).data)


class CityViewSet(viewsets.ModelViewSet):
    serializer_class = CitySerializer
    queryset = City.objects.all()
