import uuid

from django.conf import settings
from django.contrib.auth.models import AbstractUser, Group
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


class User(AbstractUser):
    NO_REALM = 'no_realm'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    realm = models.CharField(default=NO_REALM, max_length=255)

    def __str__(self):
        return self.username


class KeycloakGroup(Group):

    def __str__(self):
        return self.name

    @classmethod
    def create_with_group_and_tag(cls, group_name):
        from umbrella.contracts.models import Tag
        keycloak_group = cls.objects.create(name=group_name)
        group = Group.objects.get(id=keycloak_group.id)
        Tag.objects.create(name=group_name, group=group, type=Tag.TagTypes.GROUP)
        return keycloak_group


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
