from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Location, Skill
from .serializers import UserProfileSerializer, LocationSerializer, SkillSerializer, UserProfileUpdateSerializer, \
    SuccessSerializer


class UserProfileViewSet(viewsets.GenericViewSet):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    def list(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    @swagger_auto_schema(
        request_body=UserProfileUpdateSerializer,
        responses={200: SuccessSerializer()}
    )
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({})

    @swagger_auto_schema(
        query_serializer=LocationSerializer,  # noqa
    )
    @action(detail=False, methods=['get'])
    def get_coordinates(self, request):
        serializer = LocationSerializer(data=request.query_params, context={'request': request})
        serializer.is_valid(raise_exception=True)
        try:
            if city := serializer.validated_data['city']:
                serializer.save()
                return Response({'city': city})
            return Response({'error': 'Location not found.'}, status=404)
        except Exception as e:
            return Response({'error': 'Unavailable'}, status=503)


class LocationViewSet(viewsets.ModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    permission_classes = [IsAuthenticated]


class SkillViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Skill.objects.all().order_by('-experience_years')
    serializer_class = SkillSerializer
