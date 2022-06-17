from rest_framework import generics, serializers
from rest_framework.filters import OrderingFilter
from rest_framework.pagination import LimitOffsetPagination

from addition import clients, enums, models


class AdditionSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    state = serializers.ChoiceField(choices=enums.State, read_only=True)
    name = serializers.CharField(read_only=True)
    progress = serializers.FloatField(read_only=True)


# TODO: add filtering capabilities
class AdditionListView(generics.ListAPIView):
    pagination_class = LimitOffsetPagination
    serializer_class = AdditionSerializer

    filter_backends = [OrderingFilter]
    ordering_fields = models.Addition.fields()
    ordering = "name"

    def get_queryset(self) -> models.ObjectSet[models.Addition]:
        return clients.Transmission.get_torrents() + clients.FileSystem.get_files()
