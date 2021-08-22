from django.contrib import admin
from django.urls import path

from strawberry.django.views import GraphQLView

from strawberry_api.schema import schema as strawberry_schema

urlpatterns = [
    path("admin/", admin.site.urls),
    path("strawberry-graphql/", GraphQLView.as_view(schema=strawberry_schema)),
]
