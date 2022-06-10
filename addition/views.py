import os

from django.conf import settings
from rest_framework import generics, serializers
from rest_framework.pagination import LimitOffsetPagination

from addition import enums, models


class IncomingListSerializer(serializers.Serializer):
    name = serializers.CharField()


class IncomingListView(generics.ListAPIView):
    pagination_class = LimitOffsetPagination
    serializer_class = IncomingListSerializer

    def get_queryset(self):
        _items = [t for t in os.walk(settings.INCOMING_FOLDER) if t[0] != settings.INCOMING_FOLDER]
        return [{"name": os.path.basename(os.path.normpath(t[0]))} for t in _items]

    def filter_queryset(self, queryset):
        # TODO: Do we really need anything functional here?
        return queryset


class AdditionSerializer(serializers.ModelSerializer):
    content_type = serializers.ChoiceField(choices=enums.AdditionType.choices)

    class Meta:
        model = models.Addition
        fields = "__all__"


class AdditionListView(generics.ListCreateAPIView):
    queryset = models.Addition.objects.get_queryset()
    serializer_class = AdditionSerializer


class AdditionDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Addition.objects.get_queryset()
    serializer_class = AdditionSerializer
