from django.db import connection
from django.test import TestCase

from .models import City, Country, CountryLanguage


def create_country(continent, region, code):
    return Country.objects.create(
        code=code,
        continent=continent,
        region=region,
        surface_area=1,
        independence_year=1,
        population=1,
        life_expectancy=1,
        gnp=1,
        gnp_old=1,
    )


def create_language(country, name):
    return CountryLanguage.objects.create(
        country=country,
        name=name,
        is_official=False,
        percentage=10
    )


def create_city(country, name):
    return City.objects.create(
        country=country,
        name=name,
        population=123,
        district="District " + name,
    )


class TestUnmanaged(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # This is required for unmanaged models
        with connection.schema_editor() as schema_editor:
            schema_editor.create_model(Country)
            schema_editor.create_model(City)
            schema_editor.create_model(CountryLanguage)

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()


class TestWorldAPI(TestUnmanaged):
    def test_there_are_7_continents(self):
        response = self.client.get("/api/")
        self.assertEqual(len(response.json()), 7)

    def test_there_are_no_regions_by_default(self):
        response = self.client.get("/api/africa/")
        self.assertEqual(len(response.json()), 0)

    def test_created_region_is_shown(self):
        create_country("Europe", "Baltic Countries", "EST")
        response = self.client.get("/api/europe/")
        self.assertEqual(len(response.json()), 1)
        self.assertEqual(response.json()[0]["name"], "Baltic Countries")

    def test_created_region_is_not_shown_in_other_continents(self):
        create_country("Europe", "Baltic Countries", "EST")
        response = self.client.get("/api/africa/")
        self.assertEqual(len(response.json()), 0)

    def test_created_city_is_shown(self):
        create_country("Europe", "Baltic Countries", "EST")
        response = self.client.get("/api/europe/baltic-countries/")
        self.assertEqual(len(response.json()), 1)
        self.assertEqual(response.json()[0]["code"], "EST")

    def test_country_details_include_languages(self):
        country = create_country("Europe", "Baltic Countries", "EST")
        create_language(country, "Estonian")

        response = self.client.get("/api/europe/baltic-countries/EST/")
        languages = response.json()["languages"]
        self.assertEqual(len(languages), 1)
        self.assertEqual(languages[0]["name"], "Estonian")

    def test_country_details_include_cities(self):
        country = create_country("Europe", "Baltic Countries", "EST")
        create_city(country, "Tallinn")

        response = self.client.get("/api/europe/baltic-countries/EST/")
        cities = response.json()["cities"]
        self.assertEqual(len(cities), 1)
        self.assertEqual(cities[0]["name"], "Tallinn")
