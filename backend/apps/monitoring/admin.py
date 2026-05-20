from django.contrib import admin

from .models import Metric
from .models import Anomaly
from .models import RCAnalysis


admin.site.register(Metric)
admin.site.register(Anomaly)
admin.site.register(RCAnalysis)