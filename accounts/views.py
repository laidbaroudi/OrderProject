from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.db.models import Sum
from django.utils import timezone
from rest_framework import status, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from calls.models import Call
from orders.models import Order

from .models import AISetting, ShopSetting, TeamMember, UserProfile
from .serializers import AISettingSerializer, ShopSettingSerializer, TeamMemberSerializer


def _user_payload(user):
    profile = getattr(user, "profile", None)
    return {
        "id": user.id,
        "email": user.email,
        "full_name": profile.full_name if profile else (user.first_name or ""),
        "role": profile.role if profile else "",
    }


class SignUpView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = (request.data.get("email") or "").strip().lower()
        password = request.data.get("password") or ""
        confirm_password = request.data.get("confirm_password") or ""
        role = (request.data.get("role") or "").strip()
        full_name = (request.data.get("full_name") or "").strip()

        if not email:
            return Response({"detail": "Email is required."}, status=status.HTTP_400_BAD_REQUEST)
        try:
            validate_email(email)
        except ValidationError:
            return Response({"detail": "Enter a valid email address."}, status=status.HTTP_400_BAD_REQUEST)
        if len(password) < 8:
            return Response({"detail": "Password must be at least 8 characters."}, status=status.HTTP_400_BAD_REQUEST)
        if password != confirm_password:
            return Response({"detail": "Passwords do not match."}, status=status.HTTP_400_BAD_REQUEST)
        if role not in ("seller", "customer"):
            return Response({"detail": "Role must be 'seller' or 'customer'."}, status=status.HTTP_400_BAD_REQUEST)
        if User.objects.filter(username__iexact=email).exists() or User.objects.filter(email__iexact=email).exists():
            return Response({"detail": "A user with this email already exists."}, status=status.HTTP_400_BAD_REQUEST)

        user = User(username=email, email=email, first_name=full_name)
        user.set_password(password)
        user.save()
        UserProfile.objects.create(user=user, role=role, full_name=full_name)
        token, _ = Token.objects.get_or_create(user=user)
        return Response({"token": token.key, "user": _user_payload(user)}, status=status.HTTP_201_CREATED)


class SignInView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = (request.data.get("email") or "").strip().lower()
        password = request.data.get("password") or ""
        if not email or not password:
            return Response({"detail": "Email and password are required."}, status=status.HTTP_400_BAD_REQUEST)
        user = authenticate(request, username=email, password=password)
        if user is None:
            # Email is case-insensitive; fall back for accounts stored with mixed case.
            username = User.objects.filter(email__iexact=email).values_list("username", flat=True).first()
            if username and username != email:
                user = authenticate(request, username=username, password=password)
        if user is None:
            return Response({"detail": "Invalid email or password"}, status=status.HTTP_401_UNAUTHORIZED)
        token, _ = Token.objects.get_or_create(user=user)
        return Response({"token": token.key, "user": _user_payload(user)})


class SignOutView(APIView):
    def post(self, request):
        Token.objects.filter(user=request.user).delete()
        return Response({"detail": "Signed out"})


class MeView(APIView):
    def get(self, request):
        return Response(_user_payload(request.user))


class AISettingView(APIView):
    def _get(self, user):
        obj, _ = AISetting.objects.get_or_create(owner=user)
        return obj

    def get(self, request):
        return Response(AISettingSerializer(self._get(request.user)).data)

    def put(self, request):
        obj = self._get(request.user)
        serializer = AISettingSerializer(obj, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class ShopSettingView(APIView):
    def _get(self, user):
        obj, _ = ShopSetting.objects.get_or_create(owner=user)
        return obj

    def get(self, request):
        return Response(ShopSettingSerializer(self._get(request.user)).data)

    def put(self, request):
        obj = self._get(request.user)
        serializer = ShopSettingSerializer(obj, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class TeamMemberViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = TeamMemberSerializer

    def get_queryset(self):
        return TeamMember.objects.filter(owner=self.request.user)


class DashboardView(APIView):
    def get(self, request):
        today = timezone.localdate()
        calls_today = Call.objects.filter(owner=request.user, created_at__date=today).count()
        awaiting_approval = Order.objects.filter(owner=request.user, status=Order.Status.APPROVAL).count()
        sent_to_packing = Order.objects.filter(owner=request.user, status=Order.Status.PACKING).count()
        revenue_saved = (
            Order.objects.filter(owner=request.user, status=Order.Status.PACKING).aggregate(s=Sum("total_price"))["s"]
            or 0
        )
        return Response(
            {
                "calls_today": calls_today,
                "awaiting_approval": awaiting_approval,
                "sent_to_packing": sent_to_packing,
                "revenue_saved": revenue_saved,
                "daily_limit": 850,
                "daily_max": 1000,
            }
        )
