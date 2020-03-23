from django.db import models


class Country(models.Model):
    class Meta:
        managed = False
        db_table = "country"

    CONTINENTS = [
        "Africa",
        "Antarctica",
        "Asia",
        "Europe",
        "North America",
        "Oceania",
        "South America",
    ]

    code = models.CharField(max_length=3, primary_key=True)
    name = models.TextField()
    continent = models.TextField(
        choices=[(c, c) for c in CONTINENTS], blank=False, default="Africa"
    )
    region = models.TextField()
    surface_area = models.FloatField(db_column="surfacearea")
    independence_year = models.SmallIntegerField(db_column="indepyear")
    population = models.IntegerField()
    life_expectancy = models.FloatField(db_column="lifeexpectancy")
    gnp = models.DecimalField(max_digits=10, decimal_places=2, blank=True)
    gnp_old = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, db_column="gnpold"
    )
    local_name = models.TextField(db_column="localname")
    government_form = models.TextField(db_column="governmentform")
    head_of_state = models.TextField(db_column="headofstate", blank=True)
    capital = models.ForeignKey(
        "City", on_delete=models.SET_NULL, blank=True, null=True,
        related_name='+', db_column='capital'
    )
    iso_code = models.CharField(max_length=2, db_column="code2", unique=True)

    def __str__(self):
        return self.name


class CountryLanguage(models.Model):
    class Meta:
        managed = False
        db_table = "countrylanguage"
        unique_together = (("country", "name"),)

    country = models.ForeignKey(
        Country, related_name="languages", on_delete=models.CASCADE,
        db_column="countrycode", to_field="code"
    )
    name = models.TextField(primary_key=True, db_column="language")
    is_official = models.BooleanField(db_column="isofficial")
    percentage = models.FloatField()

    def __str__(self):
        return self.name


class City(models.Model):
    class Meta:
        managed = False
        db_table = "city"

    id = models.AutoField(primary_key=True)
    name = models.TextField()
    district = models.TextField()
    population = models.IntegerField()
    country = models.ForeignKey(
        Country, related_name="cities", on_delete=models.CASCADE,
        db_column="countrycode", to_field="code",
    )

    def __str__(self):
        return self.name
