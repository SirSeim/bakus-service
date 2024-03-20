import pytest

from addition import enums
from addition.models import Addition
from addition.views import BaseAdditionRenameSerializer


def test_base_addition_rename_serializer_update_not_implemented():
    serializer = BaseAdditionRenameSerializer()
    with pytest.raises(NotImplementedError):
        serializer.update(
            Addition(files=[], name="test", progress=1.0, state=enums.State.COMPLETED, delete=lambda: None), {}
        )
