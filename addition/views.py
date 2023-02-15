import copy

from django.contrib.auth import login
from django.contrib.auth.models import User
from knox.views import LoginView as KnoxLoginView
from rest_framework import generics, serializers, status
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.filters import OrderingFilter
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from addition import clients, enums, errors, models
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


class AdditionViewMixin:
    DEMO_LIST_INSTANCES = [
        models.Addition(
            state=enums.State.DOWNLOADING, name="demo_addition_1", progress=0.5, files=[], delete=lambda: None
        ),
        models.Addition(
            state=enums.State.COMPLETED, name="demo_addition_2", progress=1.0, files=[], delete=lambda: None
        ),
    ]

    def is_demo_user(self) -> bool:
        return models.get_user_settings(self.request.user).demo

    def get_queryset(self) -> models.AdditionSet[models.Addition]:
        if self.is_demo_user():
            return models.AdditionSet(self.DEMO_LIST_INSTANCES)
        return clients.Transmission.get_torrents() + clients.FileSystem.get_files()


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


class AdditionListView(AdditionViewMixin, generics.ListCreateAPIView):
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
        delete=lambda: None,
    )

    def perform_create(self, serializer):
        if self.is_demo_user():
            serializer.instance = self.DEMO_CREATE_INSTANCE
            return
        super().perform_create(serializer)


class AdditionDetailView(AdditionViewMixin, generics.RetrieveDestroyAPIView):
    lookup_field = "id"
    serializer_class = AdditionSerializer

    DEMO_INSTANCE = models.Addition(
        state=enums.State.DOWNLOADING, name="demo_addition_1", progress=0.5, files=[], delete=lambda: None
    )

    def get_object(self):
        if self.is_demo_user():
            # always return same instance for demo user
            instance = copy.deepcopy(self.DEMO_INSTANCE)
            instance.id = self.kwargs[self.lookup_field]
            return instance
        return super().get_object()

    def perform_destroy(self, instance):
        if self.is_demo_user():
            # do nothing for demo user
            return
        super().perform_destroy(instance)


class RenameFileSerializer(serializers.Serializer):
    current_name = serializers.CharField()
    new_name = serializers.CharField()


class AdditionRenameMovieSerializer(serializers.Serializer):
    title = serializers.CharField()
    delete_rest = serializers.BooleanField(default=False)
    files = RenameFileSerializer(many=True, allow_empty=False, min_length=1)

    # because instance is attached in view, update is called instead of create
    def update(self, instance: models.Addition, validated_data):
        if instance.state != enums.State.COMPLETED:
            raise errors.InvalidCompleteAddition()

        renames = []
        for file in validated_data["files"]:
            renames.append(
                models.RenameFile(
                    current_name=file["current_name"],
                    new_name=file["new_name"],
                )
            )
        clients.FileSystem.rename_and_move_movie(instance.name, validated_data["title"], renames)
        # with renames done, delete everything else if requested
        if validated_data["delete_rest"]:
            instance.delete()

        # return input data as this serializer is for the rename payload
        return validated_data


class AdditionRenameMovieView(AdditionViewMixin, generics.CreateAPIView):
    lookup_field = "id"
    serializer_class = AdditionRenameMovieSerializer

    DEMO_INSTANCE = models.Addition(
        state=enums.State.COMPLETED, name="demo_addition_1", progress=1.0, files=[], delete=lambda: None
    )

    def get_object(self):
        if self.is_demo_user():
            # always return same instance for demo user
            instance = copy.deepcopy(self.DEMO_INSTANCE)
            instance.id = self.kwargs[self.lookup_field]
            return instance
        return super().get_object()

    def perform_create(self, serializer):
        if self.is_demo_user():
            # do nothing for demo user
            # set serializer instance to input data as .update would
            serializer.instance = serializer.validated_data
            return
        super().perform_create(serializer)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Attach current instance to serializer, so it has everything it needs
        serializer.instance = self.get_object()

        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK, headers=headers)
