"""
    Specs:

    Client of this API should be able to:

    - filter by time range (date_from / date_to is enough), sources, countries, operating systems
    - group by one or more columns: date, source, country, operating system
    - sort by any column in ascending or descending order
    - see derived metric CPI (cost per install) which is calculated as cpi = spend / installs

"""
from app.models import Entry
from django.db.models import Sum, FloatField
from django.db.models.functions import Cast
from django_filters import rest_framework as filters


class EntryFilter(filters.FilterSet):
    """
        Interface to perform groupby, aggregation and filtering operations on the model.
    """

    # WHERE date <=, date >=
    date = filters.DateFromToRangeFilter(field_name='date')  # date_before: before/equal to; date_after: after/equal to

    # GROUP BY and SELECT
    groupby = filters.CharFilter(method='groupby_filter', label='groupby')

    def groupby_filter(self, queryset, name, values):
        """
            Group by method for the FilterSet. The order matters: first groupby, then select in the end.
        """
        # Get the value from the SELECT keyword
        fields = self.data['select'].split(',')

        # Since CPI is a derived metric, it needs to be computed first if necessary
        if 'cpi' in fields:
            queryset = queryset.annotate(sum_spend=Sum('spend'),
                                         sum_installs=Sum('installs')).annotate(
                cpi=(Cast('sum_spend', FloatField()) / Cast('sum_installs', FloatField())))

            fields.remove('cpi')

        # Collect the fields which represent the SELECT argument in a dictionary to be passed
        kwargs = {field: Sum(field) for field in fields}

        # The values() method corresponds to GROUP BY, annotate() according to dictionary kwargs corresponds to SELECT
        return queryset.values(*values.split(',')).annotate(**kwargs)

    class Meta:
        model = Entry
        fields = ['id', 'date', 'source', 'country', 'os', 'impressions',
                  'clicks', 'installs', 'spend', 'revenue']
