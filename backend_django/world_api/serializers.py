from rest_framework import serializers

from .models import City, Country, CountryLanguage


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = "__all__"
        read_only_fields = ["id"]

    def create(self, validated_data):
        # ID is not autoincremented by default, so it has to be done manually
        next_id = City.objects.order_by("-id")[0].id + 1
        city = City(id=next_id, **validated_data)
        city.save()
        return city


class CountryLanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = CountryLanguage
        fields = "__all__"


class CountrySerializer(serializers.ModelSerializer):
    cities = CitySerializer(read_only=True, many=True)
    languages = CountryLanguageSerializer(read_only=True, many=True)

    class Meta:
        model = Country
        fields = "__all__"
