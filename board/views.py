from django.shortcuts import render
from django.views import View

from board.models import Board


# Create your views here.
class BoardList(View):  # boards/
    def get(self, request):
        board = Board.objects.values()
        print(board)
        return render(request, 'boards.html', {'boards': board})
