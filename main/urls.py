from django.contrib import admin
from django.urls import path

from strawberry.django.views import GraphQLView as StrawberryView
from graphene_django.views import GraphQLView as GrapheneView

from strawberry_api.schema import schema as strawberry_schema
from graphene_api.schema import schema as graphene_schema

urlpatterns = [
    path("admin/", admin.site.urls),
    path("strawberry-graphql/", StrawberryView.as_view(schema=strawberry_schema)),
    path(
        "graphene-graphql", GrapheneView.as_view(schema=graphene_schema, graphiql=True)
    ),
]
