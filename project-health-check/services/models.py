from uuid import uuid4

from django.db.models import (
    DateTimeField,
    ForeignKey,
    Manager,
    Model,
    QuerySet,
    SET_NULL,
    UUIDField,
)
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _


class BaseCoreModel(Model):
    id = UUIDField(
        default=uuid4, primary_key=True, editable=False, verbose_name=_("Id")
    )
    created_at = DateTimeField(auto_now_add=True, verbose_name="Created At")

    objects = Manager()

    class Meta:
        abstract = True
        ordering = [
            "-created_at",
        ]


class SoftDeletionQuerySet(QuerySet):
    def delete(self, soft=False):
        """
        Soft delete by default.
        Use soft=False for hard delete.
        """
        if soft:
            return self.update(deleted_at=now())
        return super().delete()

    def hard_delete(self):
        """
        Hard delete all records in queryset.
        """
        return super().delete()

    def restore(self):
        """
        Restore soft deleted records.
        """
        return self.update(deleted_at=None)


class SoftDeletionManager(Manager):
    """
    Default manager: returns only non-deleted records.
    """

    def get_queryset(self):
        return SoftDeletionQuerySet(self.model, using=self._db).filter(
            deleted_at__isnull=True
        )


class AllObjectsManager(Manager):
    """
    Returns all records including soft deleted ones.
    """

    def get_queryset(self):
        return SoftDeletionQuerySet(self.model, using=self._db)


class DeletedObjectsManager(Manager):
    """
    Returns only soft deleted records.
    """

    def get_queryset(self):
        return SoftDeletionQuerySet(self.model, using=self._db).filter(
            deleted_at__isnull=False
        )


class SoftDeleteModel(BaseCoreModel):
    """
    Abstract base model that provides soft delete functionality.
    """

    deleted_at = DateTimeField(verbose_name="Deleted At", null=True, blank=True)

    # Managers
    objects = SoftDeletionManager()  # Active records only
    all_objects = AllObjectsManager()  # All records
    deleted_objects = DeletedObjectsManager()  # Only deleted records

    class Meta:
        abstract = True

    def delete(self, using=None, soft=True, *args, **kwargs):
        """
        Soft delete by default.
        Pass soft=False to hard delete.
        """
        if soft:
            self.deleted_at = now()
            self.save(update_fields=["deleted_at"])
        else:
            return super().delete(using=using, *args, **kwargs)

    def hard_delete(self, using=None, *args, **kwargs):
        """
        Always perform hard delete.
        """
        return super().delete(using=using, *args, **kwargs)

    def restore(self):
        """
        Restore a soft deleted instance.
        """
        self.deleted_at = None
        self.save(update_fields=["deleted_at"])


class TimeAuditModel(BaseCoreModel):
    """To path when the record was created and last modified"""

    updated_at = DateTimeField(auto_now=True, verbose_name="Last Modified At")

    class Meta(BaseCoreModel.Meta):
        abstract = True


class UserAuditModel(TimeAuditModel):
    """To path when the record was created and last modified"""

    created_by = ForeignKey(
        "userauth.User",
        on_delete=SET_NULL,
        related_name="%(class)s_created_by",
        verbose_name="Created By",
        null=True,
    )
    updated_by = ForeignKey(
        "userauth.User",
        on_delete=SET_NULL,
        related_name="%(class)s_updated_by",
        verbose_name="Last Modified By",
        null=True,
    )

    class Meta(BaseCoreModel.Meta):
        abstract = True


class BaseAuditModel(UserAuditModel, SoftDeleteModel):
    """To path when the record was created and last modified"""

    class Meta(BaseCoreModel.Meta):
        abstract = True
