from rest_framework.authentication import TokenAuthentication


class TokenAuthenticationInQuery(TokenAuthentication):
    """
    Extend the TokenAuthentication class to support querystring authentication
    in the form of "http://www.example.com/?auth_token=<token_key>"
    """

    def authenticate(self, request):
        if "token" in request.query_params and "HTTP_AUTHORIZATION" not in request.META:
            return self.authenticate_credentials(request.query_params.get("token"))
        else:
            return super(TokenAuthenticationInQuery, self).authenticate(request)
