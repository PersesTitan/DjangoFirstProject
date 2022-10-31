import base64
import uuid
from re import match

from django.contrib import messages
from django.core.files import uploadedfile
from django.core.handlers.wsgi import WSGIRequest
from django.db import IntegrityError
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View

from admin import settings
from board.models import Board
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


def check_name(name: str, request: WSGIRequest):
    boolean = False
    if match("^[0-9]+$", name):
        messages.error(request, "아이디에 숫자만 존재할 수 없습니다.")
        boolean = True
    return boolean


def create_user(request: WSGIRequest, username: str, password: str, password_check: str, email: str):
    b = False
    b = check_blank(username, "아이디", request) or b
    b = check_blank(password, "비밀번호", request) or b
    b = check_blank(email, "비밀번호 확인", request) or b
    b = check_blank(email, "이메일", request) or b
    if password_check != password:
        messages.error(request, "비밀번호가 일치하지 않습니다.")
        b = b or True
    return check_password(username, password, email, request) or b


def check_password(name: str, password: str, email: str, request: WSGIRequest):
    boolean = check_name(name, request)
    password_message = "비밀번호가 취약합니다. "
    if name == password:
        messages.error(request, password_message + "(아이디와 비밀번호가 똑같습니다.)")
        boolean = True
    if len(password) < 4:
        messages.error(request, password_message + "(비밀번호 길이가 4자리 미만입니다.)")
        boolean = True
    if not match("[0-9a-zA-Z]([-_.]?[0-9a-zA-Z])*@[0-9a-zA-Z]([-_.]?[0-9a-zA-Z])*.[a-zA-Z]$", email):
        messages.error(request, "이메일 형식이 일치하지 않습니다.")
        boolean = True
    return boolean


def read_image(file: str):
    return (file.split(".")[-1].upper(), "." + settings.MEDIA_URL + file) if file else ("PNG", "image/profile.png")


def get_base(file: str):
    return base64.b64encode(open(file, 'rb').read()).decode()


############################################################################
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


# @method_decorator(csrf_exempt, name='dispatch')
class CreateUsers(View):  # users/singup/   singup
    def get(self, request: WSGIRequest):
        return render(request, 'singup.html')

    def post(self, request):
        try:
            data = request.POST
            username = data.get("id")
            password = data.get("password")
            email = data.get("email")
            password_check = data.get("password-check")

            if create_user(request, username, password, password_check, email):
                return redirect('singup')

            User.objects.create(
                username=username,
                password=password,
                email=email
            )
            return redirect('login')
        except IntegrityError as mes:
            if str(mes) == 'UNIQUE constraint failed: users_user.username':
                messages.error(request, '이미 존재하는 유저이름입니다.')
            return redirect('singup')


class EditUser(View):  # users/edit/
    def get(self, request: WSGIRequest):
        user = get_user(request)
        return redirect('/users/login/?next=/users/login/' if user is None else f'/users/edit/{user.pk}/')


# @method_decorator(csrf_exempt, name='dispatch')
class EditUsers(View):  # users/edit/<int:board_id>/
    def get(self, request: WSGIRequest, board_id):
        edit = request.GET.get("edit", "false") == "true"
        login_user: User = get_user(request)
        user: User = get_object_or_404(User, pk=board_id)

        exi, image_data = read_image(user.profile_image.name)
        context = {"user": user, "image": {"exi": exi, "data": get_base(image_data)}}
        if login_user is None or login_user.pk != user.pk:
            boards = Board.objects.filter(user=user)
            context["boards"] = boards
            context["follow_check"] = login_user in user.followers.all()
            context["follow"] = len(user.followers.all())
            return render(request, 'user_find.html', context)
        else:
            context["boards"] = Board.objects.filter(user=login_user)
            return render(request, 'user_setting_edit.html' if edit else 'user_setting.html', context)

    def post(self, request: WSGIRequest, board_id):
        follow = request.POST.get('follow', None)
        login_user: User = get_user(request)

        user: User = get_object_or_404(User, pk=board_id)
        if follow is not None:
            if login_user is None:
                return redirect(f'/users/login/?next=/users/edit/{board_id}')
            else:
                if login_user in user.followers.all():
                    user.followers.remove(login_user)
                    login_user.following.remove(user)
                else:
                    user.followers.add(login_user)
                    login_user.following.add(user)
                return redirect(request.META['HTTP_REFERER'])
        elif login_user is not None:
            data = request.POST
            if data.get('upload_file') is not None:
                profile_image: uploadedfile.InMemoryUploadedFile = request.FILES.get("files")
                user.profile_image = profile_image
                user.save()
                return redirect(request.META['HTTP_REFERER'])
            username = data.get("username")
            password = data.get("password")
            password_check = data.get("password-check")
            email = data.get("email")
            if create_user(request, username, password, password_check, email):
                return redirect(request.META['HTTP_REFERER'])
            else:
                login_user.username = username
                login_user.password = password
                login_user.email = data.get("email")
                login_user.save()
                return redirect(f"/users/edit/{board_id}")
        else:
            return redirect(f'/users/login/?next=/users/edit/{board_id}')
