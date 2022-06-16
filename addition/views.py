from rest_framework import generics, serializers
from rest_framework.pagination import LimitOffsetPagination

from addition import clients, enums


class AdditionSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    state = serializers.ChoiceField(choices=enums.State, read_only=True)
    name = serializers.CharField(read_only=True)
    progress = serializers.FloatField(read_only=True)


# TODO: add filtering and sorting capabilities
class AdditionListView(generics.ListAPIView):
    pagination_class = LimitOffsetPagination
    serializer_class = AdditionSerializer

    def get_queryset(self):
        torrents = clients.Transmission.get_torrents()
        files = clients.FileSystem.get_files()
        complete = torrents + files
        complete.sort(key=lambda a: a.name)
        return complete

    def filter_queryset(self, queryset):
        # TODO: Do we really need anything functional here?
        return queryset
