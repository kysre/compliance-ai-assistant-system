from rest_framework import serializers

from compliance.models import Regulation


class RegulationSerializer(serializers.ModelSerializer):
    # Override date field to use CharField for initial input
    date = serializers.CharField()

    class Meta:
        model = Regulation
        fields = ["identifier", "title", "date", "authority", "link", "text"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        context = kwargs.get("context", {})
        if not context.get("include_text", True):
            self.fields.pop("text", None)

    def validate_date(self, value):
        """
        Convert date from yyyy/mm/dd to yyyy-mm-dd format
        """
        return str(value).replace("/", "-")

    def create(self, validated_data):
        # Create the model instance with the converted date
        return super().create(validated_data)
