from django.db import models
from south.db import DEFAULT_DB_ALIAS

class MigrationHistory(models.Model):
    invoices = models.CharField(max_length=255)
    migration = models.CharField(max_length=255)
    applied = models.DateTimeField(blank=True)

    @classmethod
    def for_migration(cls, migration, database):
        try:
            # Switch on multi-db-ness
            if database != DEFAULT_DB_ALIAS:
                # Django 1.2
                objects = cls.objects.using(database)
            else:
                # Django <= 1.1
                objects = cls.objects
            return objects.get(
                invoices=migration.app_label(),
                migration=migration.name(),
            )
        except cls.DoesNotExist:
            return cls(
                invoices=migration.app_label(),
                migration=migration.name(),
            )

    def get_migrations(self):
        from south.migration.base import Migrations
        return Migrations(self.invoices)

    def get_migration(self):
        return self.get_migrations().migration(self.migration)
    
    def __str__(self):
        return "<%s: %s>" % (self.invoices, self.migration)
