import uuid as uuid

from django.core.exceptions import ValidationError
from django.db import models
from model_utils.models import UUIDModel


class CustomModel(UUIDModel):
    uuid = models.UUIDField(
        unique=True,
        default=uuid.uuid4,
        editable=False)

    class Meta:
        abstract = True

    @classmethod
    def create(cls, **kwargs):
        obj = cls(**kwargs)

        obj.full_clean()
        obj.save()
        return obj

    def update(self, **kwargs):
        if hasattr(self, 'EDITABLE_FIELDS'):
            for name, value in kwargs.items():
                if name not in self.EDITABLE_FIELDS:
                    raise ValidationError(f"Field {name} is not allowed for update")
                setattr(self, name, value)

        self.full_clean()
        self.save()
        return self
