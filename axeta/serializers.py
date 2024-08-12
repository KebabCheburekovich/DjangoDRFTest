import requests
from rest_framework import serializers

from config.settings import GEOAPIFY_API_KEY
from .models import UserProfile, Location, Skill


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ['name', 'experience_years']

    def save(self, **kwargs):
        user = self.context['request'].user
        return self.Meta.model.objects.create(
            owner=user,
            **self.validated_data

        )


class LocationSerializer(serializers.ModelSerializer):
    city = serializers.CharField(read_only=True)

    class Meta:
        model = Location
        fields = ['city', 'latitude', 'longitude']

    def validate(self, attrs):
        latitude = attrs.get('latitude')
        longitude = attrs.get('longitude')
        response = requests.get(
            url=f'https://api.geoapify.com/v1/geocode/reverse?lat={latitude}&lon={longitude}&apiKey={GEOAPIFY_API_KEY}')
        json_data = response.json()
        city = json_data['features'][0]['properties']['formatted']
        attrs['city'] = city
        return attrs

    def save(self, **kwargs):
        user = self.context['request'].user
        return self.Meta.model.objects.update_or_create(
            owner=user,
            defaults={
                'latitude': self.validated_data.get('latitude'),
                'longitude': self.validated_data.get('longitude'),
                'city': self.validated_data.get('city')
            }
        )


class UserProfileSerializer(serializers.ModelSerializer):
    skills = SkillSerializer(many=True, read_only=True, allow_null=True)
    location = LocationSerializer(read_only=True, allow_null=True)

    class Meta:
        model = UserProfile
        fields = ['name', 'avatar', 'skills', 'location']

    def validate_name(self, name):
        if not name.isalnum():
            raise serializers.ValidationError('Name contains invalid characters.')
        return name


class UserProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['name', "avatar"]


class SuccessSerializer(serializers.Serializer):
    pass
