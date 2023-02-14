from django.template import loader
from rest_framework.compat import coreapi, coreschema
from rest_framework.filters import BaseFilterBackend

from addition import models


class AttributeFilter(BaseFilterBackend):
    object_fields = []
    template = "filters/attribute_filter.html"
    title = "Attribute Filter"
    description = "Filter by object attribute"

    def get_fields(self, view) -> set[str]:
        if hasattr(view, "object_fields"):
            return set(view.object_fields)
        else:
            return set(self.object_fields)

    def get_filters(self, view, request) -> dict[str, list[str]]:
        fields = self.get_fields(view)
        results = {}
        for f in fields:
            filters = self.get_terms(request, f"filter_{f}")
            if filters:
                results[f] = filters
        return results

    @staticmethod
    def get_terms(request, field: str) -> list[str]:
        params = request.query_params.get(field, "")
        params = params.replace("\x00", "")  # strip null characters
        params = params.replace(",", " ")
        return params.split()

    # TODO: make this less hackish by having the filter value types align with the object field
    def filter_queryset(self, request, queryset: models.AdditionSet, view) -> models.AdditionSet:
        filters = self.get_filters(view, request)
        if not filters:
            return queryset
        return queryset.filter(**filters)

    def get_template_context(self, request, queryset: models.AdditionSet, view) -> dict:
        raw_fields = self.get_fields(view)
        filters = self.get_filters(view, request)
        fields = []
        for f in raw_fields:
            value = ""
            if filters.get(f):
                value = filters[f][0]
            fields.append((f"filter_{f}", f, value))
        return {
            "fields": fields,
        }

    def to_html(self, request, queryset, view):
        template = loader.get_template(self.template)
        context = self.get_template_context(request, queryset, view)
        return template.render(context)

    def get_schema_fields(self, view):
        assert coreapi is not None, "coreapi must be installed to use `get_schema_fields()`"
        assert coreschema is not None, "coreschema must be installed to use `get_schema_fields()`"
        return [
            coreapi.Field(
                name=f"filter_{field}",
                required=False,
                location="query",
                schema=coreschema.String(
                    title=f"{self.title}: {field}",
                    description=f"{self.description}: {field}",
                ),
            )
            for field in self.get_fields(view)
        ]

    def get_schema_operation_parameters(self, view):
        return [
            {
                "name": f"filter_{field}",
                "required": False,
                "in": "query",
                "description": f"{self.description}: {field}",
                "schema": {
                    "type": "string",
                },
            }
            for field in self.get_fields(view)
        ]
