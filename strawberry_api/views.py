from django.http import HttpResponseNotAllowed
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from strawberry.django.views import GraphQLView, TemporalHttpResponse


class NoValidateView(GraphQLView):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        if not self.is_request_allowed(request):
            return HttpResponseNotAllowed(
                ["GET", "POST"], "GraphQL only supports GET and POST requests."
            )

        if self.should_render_graphiql(request):
            return self._render_graphiql(request)

        request_data = self.get_request_data(request)

        sub_response = TemporalHttpResponse()
        context = self.get_context(request, response=sub_response)

        result = self.schema.execute_sync(
            request_data.query,
            root_value=self.get_root_value(request),
            variable_values=request_data.variables,
            context_value=context,
            operation_name=request_data.operation_name,
            validate_queries=False,
        )

        response_data = self.process_result(request=request, result=result)

        return self._create_response(
            response_data=response_data, sub_response=sub_response
        )
