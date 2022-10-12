from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from board.models import Board, Command
from users.views import ID_REPOSITORY, check_blank


def get_user(request):
    return ID_REPOSITORY.get(request.COOKIES.get('id'))


# Create your views here.
class ListBoard(View):  # boards/   boards
    def get(self, request):
        page = request.GET.get('page', 1)
        user = get_user(request)
        content = {}
        if user is not None:
            content["username"] = user.username

        board_list = Board.objects.order_by('-create_date')
        li = list()
        for value, board in zip(board_list.values(), board_list.all()):
            value['good'] = len(board.good.all())
            li.append(value)

        paginator = Paginator(li, 5)
        page = paginator.get_page(page)

        content['boards'] = page.object_list
        content['page_list'] = paginator.page_range
        return render(request, 'boards.html', content)


@method_decorator(csrf_exempt, name='dispatch')
class CreateBoard(View):  # boards/add/  board-add
    def get(self, request):
        user = get_user(request)
        if user is None:
            return redirect(f'/users/login/?next=/boards/add/')
        else:
            return render(request, 'item/board_create.html')

    def post(self, request):
        data = request.POST
        title = data.get("title")
        content = data.get("content")

        user = get_user(request)
        if user is None:
            return redirect(f'/users/login/?next=/boards/add/')

        b = False
        b = check_blank(title, "제목", request) or b
        b = check_blank(content, "내용", request) or b

        if b:
            return redirect(request.META['HTTP_REFERER'])
        Board.objects.create(
            title=title,
            content=content,
            user=user,
            username=user.username
        )
        return redirect('boards')


@method_decorator(csrf_exempt, name='dispatch')
class OneBoard(View):  # boards/<int:board_id>/    board-item
    def get(self, request, board_id):
        board = Board.objects.get(pk=board_id)
        user = get_user(request)

        commands = list()
        for i in board.command.all():
            login_check = (user is not None) and (user == i.user)
            commands.append({"value": i, "login_check": login_check})

        check_user = board.user == user
        context = {"board": board,
                   "good": len(board.good.all()),
                   "commands": commands,
                   "check_user": check_user}
        if (user is not None) and (user in board.good.all()):
            context["good_check"] = True
        return render(request, 'item/board_item.html', context)

    def post(self, request, board_id):
        board = Board.objects.get(pk=board_id)
        user = get_user(request)
        if user is None:
            return redirect(f'/users/login/?next=/boards/{board_id}/')
        else:
            if request.POST.get('good') is not None:
                if board in user.good.all():
                    user.good.remove(board)
                    board.good.remove(user)
                else:
                    user.good.add(board)
                    board.good.add(user)
            elif request.POST.get('command_send') is not None:
                command_value = request.POST.get('command')
                if not check_blank(command_value, '댓글 내용', request):
                    command = Command.objects.create(
                        content=command_value,
                        user=user
                    )
                    board.command.add(command)
            elif request.POST.get('command_remove') is not None:
                command_id = request.POST.get('command_id')
                Command.delete(Command.objects.get(pk=command_id))
            return redirect(request.META['HTTP_REFERER'])


@method_decorator(csrf_exempt, name='dispatch')
class EditBoard(View):  # boards/<int:board_id>/edit/    board-edit
    def get(self, request, board_id):
        board = Board.objects.get(pk=board_id)
        user = get_user(request)
        if user is None or board.user != user:
            return redirect(f'/users/login/?next=/boards/{board_id}/edit/')
        else:
            content = {
                "title": board.title,
                "content": board.content,
                "board_id": board_id
            }
            return render(request, 'item/board_edit.html', content)

    def post(self, request, board_id):
        title = request.POST.get("title")
        content = request.POST.get("content")

        b = False
        b = check_blank(title, "제목", request) or b
        b = check_blank(content, "내용", request) or b
        if b:
            return redirect(request.META['HTTP_REFERER'])
        else:
            board = Board.objects.get(pk=board_id)
            board.title = title
            board.content = content
            board.save()
            return redirect('boards')


@method_decorator(csrf_exempt, name='dispatch')
class RemoveBoard(View):  # boards/<int:board_id>/remove/    board-remove
    def get(self, request, board_id):
        user = get_user(request)
        board = Board.objects.get(pk=board_id)
        if user is not None and board.user == user:
            Board.delete(board)
            return redirect('boards')
        else:
            return redirect(f'/users/login/?next=/boards/{board_id}/')
