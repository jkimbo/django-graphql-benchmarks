from django.contrib import admin
from django.urls import path, include
from django.views.decorators.csrf import csrf_exempt

from strawberry.django.views import GraphQLView as StrawberryView
from graphene_django.views import GraphQLView as GrapheneView
from rest_framework import routers

from strawberry_api.schema import schema as strawberry_schema
from strawberry_api.views import NoValidateView
from graphene_api.schema import schema as graphene_schema
from drf_api.serializers import MovieViewSet
from json_api.views import top_250


router = routers.DefaultRouter()
router.register(r"movies", MovieViewSet)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("strawberry-graphql/", StrawberryView.as_view(schema=strawberry_schema)),
    path(
        "strawberry-graphql-no-validate/",
        NoValidateView.as_view(schema=strawberry_schema),
    ),
    path(
        "graphene-graphql/",
        csrf_exempt(GrapheneView.as_view(schema=graphene_schema, graphiql=True)),
    ),
    path("drf-api/", include(router.urls)),
    path("json-api/top-250", top_250),
]
