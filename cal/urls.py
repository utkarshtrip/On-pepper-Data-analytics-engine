from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', views.xbrl_table, name='xbrl_table'),
    path('submit-expression', views.submit_expression, name="submit_expression"),
    path("save_expression_column", views.save_expression_column, name="save_expression_column"),
] + static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)