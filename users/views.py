import uuid

from django.db import IntegrityError
from django.db.models import Q
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages

from users.models import User

ID_REPOSITORY = dict()


def get_user(request):
    return ID_REPOSITORY.get(request.COOKIES.get('id'))


def set_id(key, value):
    if len(ID_REPOSITORY) != 0 and value in list(ID_REPOSITORY.values()):
        # 존재하는 값 일때 삭제
        for k, v in ID_REPOSITORY.items():
            if ID_REPOSITORY[k] == value:
                del ID_REPOSITORY[k]
    ID_REPOSITORY[key] = value


def check_blank(li: str, kind: str, request):
    if not li.strip():
        messages.error(request, kind + " - 내용을 입력해주세요.")
        return True


# Create your views here.
# @login_required
class LoginUser(View):  # users/login/    login
    def get(self, request):
        user = get_user(request)
        content = {'user_check': user is not None, 'user': user}
        return render(request, 'login.html', content)

    def post(self, request):
        if request.POST.get('logout') is not None:
            response = redirect(request.META['HTTP_REFERER'])
            response.delete_cookie('id')
            return response
        else:
            data = request.POST
            username, password = data["id"], data["password"]
            user = User.objects.filter(Q(username=username) & Q(password=password))
            if len(user) == 0:
                messages.error(request, '아이디 또는 비밀번호가 일치하지 않습니다.')
                return redirect(request.META['HTTP_REFERER'])
            else:
                UUID = str(uuid.uuid4())
                set_id(UUID, user[0])

                url = request.GET.get('next')
                response = redirect('boards' if (url is None or not url) else url)
                response.set_cookie('id', UUID)
                return response


@method_decorator(csrf_exempt, name='dispatch')
class CreateUsers(View):  # users/singup/   singup
    def get(self, request):
        return render(request, 'singup.html')

    def post(self, request):
        try:
            data = request.POST
            username = data["id"]
            password = data["password"]
            email = data["email"]

            password_check = data["password-check"]
            b = False
            b = check_blank(username, "아이디", request) or b
            b = check_blank(password, "비밀번호", request) or b
            b = check_blank(email, "비밀번호 확인", request) or b
            b = check_blank(email, "이메일", request) or b

            if password_check != password:
                messages.error(request, "비밀번호가 일치하지 않습니다.")
                b = b or True

            if b:
                return redirect('singup')
            User.objects.create(
                username=username,
                password=password,
                email=email
            )
            return redirect('login')
        except IntegrityError as mes:
            messages.error(request, mes)
            return redirect('singup')
