from datetime import datetime
from myauth.models import UserModel


class NewMiddleware:
    def __init__(self, get_request):
        self.get_request = get_request

    def __call__(self, request):
        request = self.get_request(request)

        user = UserModel.objects.get()
        user.last_seen = datetime.now()
        user.save()
        print(user.last_seen)
        return request
