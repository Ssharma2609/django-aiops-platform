from django.urls import path

from .views import MetricListAPIView
from .views import RCAnalysisListAPIView


urlpatterns = [

    path(
        "",
        MetricListAPIView.as_view()
    ),

    path(
        "rca/",
        RCAnalysisListAPIView.as_view()
    ),

]