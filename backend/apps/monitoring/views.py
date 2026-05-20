from rest_framework import generics

from .models import Metric
from .models import RCAnalysis

from .serializers import MetricSerializer
from .serializers import RCAnalysisSerializer



class MetricListAPIView(generics.ListAPIView):

    queryset = (
        Metric.objects.all().order_by("-id")[:50]
    )

    serializer_class = MetricSerializer

class RCAnalysisListAPIView(generics.ListAPIView):

    queryset = (
        RCAnalysis.objects
        .all()
        .order_by("-created_at")[:10]
    )

    serializer_class = RCAnalysisSerializer
