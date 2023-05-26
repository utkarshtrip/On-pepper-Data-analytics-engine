from django.urls import path
from . import views

urlpatterns = [
    path('xbrl_table/', views.xbrl_table, name='xbrl_table'),
    path('submit-expression', views.submit_expression, name="submit_expression"),
]