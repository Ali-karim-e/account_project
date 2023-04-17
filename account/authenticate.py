from .models import Account


class EmailBackend:
	def authenticate(self, request, username=None, password=None):
		try:
			user = Account.objects.get(email=username)
			if user.check_password(password):
				return user
			return None
		except Account.DoesNotExist:
			return None

	def get_user(self, user_id):
		try:
			return Account.objects.get(pk=user_id)
		except Account.DoesNotExist:
			return None