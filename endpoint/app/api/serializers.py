"""
    Data structure to convert model instances to Python dictionaries - to be rendered as JSON.

"""
from app.models import Entry
from rest_framework import serializers


class EntrySerializer(serializers.ModelSerializer):
    """
        Subclass ModelSerializer with explicitly definied fields.

        ModelSerializer defines a Serializer based on a given model, as specified in inner Meta class.
    """
    date = serializers.DateField(format='%Y-%m-%d', required=False)
    source = serializers.CharField(max_length=255, required=False)
    country = serializers.CharField(max_length=2, required=False)
    os = serializers.CharField(max_length=255, required=False)
    impressions = serializers.IntegerField(required=False)
    clicks = serializers.IntegerField(required=False)
    installs = serializers.IntegerField(required=False)
    spend = serializers.FloatField(required=False)
    revenue = serializers.FloatField(required=False)

    cpi = serializers.FloatField(required=False)

    class Meta:
        model = Entry
        fields = ('id', 'date', 'source', 'country', 'os', 'impressions',
                  'clicks', 'installs', 'spend', 'revenue', 'cpi')
