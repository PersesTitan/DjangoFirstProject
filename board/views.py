from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from board.models import Board
from users.views import ID_REPOSITORY


# Create your views here.
class ListBoard(View):  # boards/   boards
    def get(self, request):
        user = ID_REPOSITORY.get(request.COOKIES.get('id'))
        content = {}
        if user is not None:
            content["username"] = user.username
        content['boards'] = Board.objects.values()
        return render(request, 'boards.html', content)


@method_decorator(csrf_exempt, name='dispatch')
class CreateBoard(View):  # boards/new/  board-new
    def get(self, request):
        user = ID_REPOSITORY.get(request.COOKIES.get('id'))
        print(request.COOKIES.get('id'))
        print(user)
        return render(request, 'item/create-board.html')
        # if user is None:
        #     return redirect('login')
        # else:
        #     return render(request, 'item/create-board.html')

    def post(self, request):
        data = request.POST
        Board.objects.create(
            title=data.get("title"),
            content=data.get("content")
        )
        return redirect('boards')
