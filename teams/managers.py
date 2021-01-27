from django.db.models import Manager
from django.core.exceptions import ObjectDoesNotExist


class TeamManager(Manager):
    def get_or_none(self, **kwargs):
        try:
            return self.get(**kwargs)
        except ObjectDoesNotExist:
            return None
