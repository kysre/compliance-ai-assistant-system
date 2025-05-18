from rest_framework import serializers
from .models import Regulation


class RegulationSerializer(serializers.ModelSerializer):
    # Override date field to use CharField for initial input
    date = serializers.CharField()
    
    class Meta:
        model = Regulation
        fields = ["identifier", "title", "date", "authority", "link", "text"]

    def validate_date(self, value):
        """
        Convert date from yyyy/mm/dd to yyyy-mm-dd format
        """
        return str(value).replace("/", "-")
    
    def create(self, validated_data):
        # Create the model instance with the converted date
        return super().create(validated_data)
