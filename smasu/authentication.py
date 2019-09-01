from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import BasePermission, IsAuthenticated


class IsListView(BasePermission):
    def has_permission(self, request, view):
        return view.action == "list"


class IsCreateView(BasePermission):
    def has_permission(self, request, view):
        return view.action == "create"


class IsSuperUserOrStaff(IsAuthenticated):
    def has_permission(self, request, view):
        user = request.user
        return super().has_permission(request, view) and user.is_active and (user.is_superuser or user.is_staff)


class IsSameUser(IsAuthenticated):
    def has_permission(self, request, view):
        return super().has_permission(request, view) and view.kwargs.get("pk") == format(request.user.pk)


class TokenAuthenticationInQuery(TokenAuthentication):
    """
    Extend the TokenAuthentication class to support querystring authentication
    in the form of "http://www.example.com/?auth_token=<token_key>"
    """

    def authenticate(self, request):
        if "token" in request.query_params and "HTTP_AUTHORIZATION" not in request.META:
            return self.authenticate_credentials(request.query_params.get("token"))
        else:
            return super().authenticate(request)
