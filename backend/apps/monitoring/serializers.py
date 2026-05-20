from rest_framework import serializers

from .models import Metric
from .models import RCAnalysis

class MetricSerializer(serializers.ModelSerializer):

    class Meta:

        model = Metric

        fields = "__all__"

class RCAnalysisSerializer(serializers.ModelSerializer):

    class Meta:

        model = RCAnalysis

        fields = "__all__"
