import copy

from django.contrib.auth import login
from django.contrib.auth.models import User
from knox.views import LoginView as KnoxLoginView
from rest_framework import generics, serializers
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.filters import OrderingFilter
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import AllowAny

from addition import clients, enums, models
from addition.filters import AttributeFilter


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "email", "first_name", "last_name"]


class AccountView(generics.RetrieveUpdateAPIView):
    serializer_class = AccountSerializer

    def get_object(self):
        return self.request.user


class LoginView(KnoxLoginView):
    permission_classes = [AllowAny]
    serializer_class = AuthTokenSerializer

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        login(request, user)
        return super().post(request, format=None)


class FileSerializer(serializers.Serializer):
    # read only fields
    name = serializers.CharField(read_only=True)
    file_type = serializers.ChoiceField(choices=enums.FileType, read_only=True)


class AdditionSerializer(serializers.Serializer):
    # read only fields
    id = serializers.CharField(read_only=True)
    state = serializers.ChoiceField(choices=enums.State, read_only=True)
    name = serializers.CharField(read_only=True)
    progress = serializers.FloatField(read_only=True)
    files = FileSerializer(many=True, read_only=True)

    # write only fields
    magnet_link = serializers.CharField(write_only=True)

    def create(self, validated_data):
        return clients.Transmission.add_torrent(validated_data["magnet_link"])


class AdditionListView(generics.ListCreateAPIView):
    pagination_class = LimitOffsetPagination
    serializer_class = AdditionSerializer

    filter_backends = [OrderingFilter, AttributeFilter]
    ordering_fields = models.Addition.fields()
    ordering = "name"
    object_fields = models.Addition.fields()

    DEMO_CREATE_INSTANCE = models.Addition(
        state=enums.State.DOWNLOADING,
        name="demo_addition",
        progress=0.0,
        files=[],
    )

    DEMO_LIST_INSTANCES = [
        models.Addition(state=enums.State.DOWNLOADING, name="demo_addition_1", progress=0.5, files=[]),
        models.Addition(state=enums.State.COMPLETED, name="demo_addition_2", progress=1.0, files=[]),
    ]

    def get_queryset(self) -> models.AdditionSet[models.Addition]:
        if models.get_user_settings(self.request.user).demo:
            return models.AdditionSet(self.DEMO_LIST_INSTANCES)
        return clients.Transmission.get_torrents() + clients.FileSystem.get_files()

    def perform_create(self, serializer):
        if models.get_user_settings(self.request.user).demo:
            serializer.instance = self.DEMO_CREATE_INSTANCE
            return
        super().perform_create(serializer)


class AdditionDetailView(generics.RetrieveDestroyAPIView):
    lookup_field = "id"
    serializer_class = AdditionSerializer

    DEMO_INSTANCE = models.Addition(state=enums.State.DOWNLOADING, name="demo_addition_1", progress=0.5, files=[])

    def get_queryset(self) -> models.AdditionSet[models.Addition]:
        if models.get_user_settings(self.request.user).demo:
            return models.AdditionSet([self.DEMO_INSTANCE])
        return clients.Transmission.get_torrents() + clients.FileSystem.get_files()

    def get_object(self):
        if models.get_user_settings(self.request.user).demo:
            # always return same instance for demo user
            instance = copy.deepcopy(self.DEMO_INSTANCE)
            instance.id = self.kwargs[self.lookup_field]
            return instance
        return super().get_object()

    def perform_destroy(self, instance):
        if models.get_user_settings(self.request.user).demo:
            # do nothing for demo user
            return
        super().perform_destroy(instance)
