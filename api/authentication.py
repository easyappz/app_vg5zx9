from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.authtoken.models import Token
from .models import Member


class MemberTokenAuthentication(TokenAuthentication):
    """Custom token authentication for Member model"""

    def authenticate_credentials(self, key):
        try:
            token = Token.objects.select_related('user').get(key=key)
        except Token.DoesNotExist:
            raise AuthenticationFailed('Invalid token')

        try:
            member = Member.objects.get(id=token.user_id)
        except Member.DoesNotExist:
            raise AuthenticationFailed('User not found')

        member.update_last_seen()

        return (member, token)
