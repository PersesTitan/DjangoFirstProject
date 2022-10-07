import json
from django.http import JsonResponse
from django.shortcuts import render
from django.views import View

from users.models import User


# Create your views here.
class FindUsers(View):  # users/
    def get(self, request):
        print(User.objects.values())
        return JsonResponse({"user": ""}, status=200)


class CreateUsers(View):  # create-users/
    def get(self, request):
        # print(json.loads(request.body))
        return JsonResponse({"create": ""}, status=200)

    def post(self, request):
        print(request)
        data = json.loads(request.body)
        create_user = User.objects.create(
            nick_name=data["nick_name"],
            password=data["password"]
        )

        print(create_user)
        return JsonResponse({"create": ""}, status=201)


class EditUser(View):  # user/<int:user_id>/
    def post(self, request, user_id):
        print(request)
        return JsonResponse({"edit": ""}, status=200)

    def get(self, request, user_id):
        print(request)
        return JsonResponse({"edit": ""}, status=200)
