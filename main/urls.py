from django.contrib import admin
from django.urls import path, include

from strawberry.django.views import GraphQLView as StrawberryView
from graphene_django.views import GraphQLView as GrapheneView
from rest_framework import routers

from strawberry_api.schema import schema as strawberry_schema
from graphene_api.schema import schema as graphene_schema
from drf_api.serializers import MovieViewSet


router = routers.DefaultRouter()
router.register(r"movies", MovieViewSet)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("strawberry-graphql/", StrawberryView.as_view(schema=strawberry_schema)),
    path(
        "graphene-graphql", GrapheneView.as_view(schema=graphene_schema, graphiql=True)
    ),
    path("drf-api/", include(router.urls)),
]
