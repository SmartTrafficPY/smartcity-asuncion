from rest_framework import viewsets
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from smasu.authentication import IsCreateView, IsListView, IsSameUser, IsSuperUserOrStaff
from ucusers.models import UcarpoolingProfile

from .models import UserItinerary
from .serializers import UserItinerarySerializer


class IsUcarpoolingUser(IsAuthenticated):
    def has_permission(self, request, view):
        return super().has_permission(request, view) and request.user.ucarpoolingprofile is not None


class UserItineraryView(viewsets.ModelViewSet):
    queryset = UserItinerary.objects.all()
    serializer_class = UserItinerarySerializer
    authentication_classes = (SessionAuthentication, TokenAuthentication)
    permission_classes = (
        IsSuperUserOrStaff | (IsAuthenticated & IsUcarpoolingUser) | (~(IsListView | IsCreateView) & IsSameUser),
    )

    def get_queryset(self):
        """
        For returning objects for the current authenticated user only.
        Getter of the queryset.
        """
        queryset = self.queryset

        """
        Checking if a staff member made the request.
        Only staff members can list all UserItinerary objects in the DB.
        Regular users can only list their UserItinerary.
        """
        if not self.request.user.is_staff:
            """The request was not made by a staff member"""

            """
            Filtering the queryset by the user that made the GET request
            """
            request_ucarpoolingProfile = UcarpoolingProfile.objects.get(user_id=self.request.user.pk)
            queryset = queryset.filter(ucarpoolingProfile=request_ucarpoolingProfile).order_by("-id")

        return queryset
