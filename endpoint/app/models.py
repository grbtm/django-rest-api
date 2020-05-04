"""
    Schema definition for the database table of metrics entries using Django's object-relational mapper.

"""
from django.db import models
from django.db.models import Sum, Case, When, F


class EntryQuerySet(models.QuerySet):
    """ Subclass Queryset to extend it with method to calculate derived metric CPI (cost per install)"""

    def extend_with_derived_metric(self):
        """ CPI is calculated as cpi = spend / installs. Use conditional expression to avoid division by zero. """
        return self.model.objects.annotate(
            sum_spend=Sum('spend'),
            sum_installs=Sum('installs')
        ).annotate(
            cpi=Case(When(sum_installs=0, then=0),
                     default=1.0 * (F('sum_spend') / F('sum_installs')),
                     output_field=models.FloatField())
        )


class Entry(models.Model):
    """
    Entry Model

    Defines the attributes of a metrics entry, as imported from dataset.csv. Every Django model comes
    with a Manager which is an interface between SQL queries and Django models.
    The default Manager is extended with the additional method from EntryQuerySet class.
    """
    date = models.DateField()
    source = models.CharField(max_length=1)
    country = models.CharField(max_length=2)
    os = models.CharField(max_length=255)
    impressions = models.IntegerField()
    clicks = models.IntegerField()
    installs = models.IntegerField()
    spend = models.FloatField()
    revenue = models.FloatField()

    # Create a models.Manager instance with EntryQuerySet methods to replace the default Manager named 'objects'
    objects = EntryQuerySet.as_manager()
