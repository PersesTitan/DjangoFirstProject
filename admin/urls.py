"""admin URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from manage import Make

urlpatterns = [
    path('admin/', admin.site.urls),
]

urlpatterns += Make.add_path(path)

# urlpatterns += [
#     path('boards/', ListBoard.as_view(), name="boards"),
#     path('boards/add/', CreateBoard.as_view(), name="board-add"),
#     path('boards/<int:board_id>/', OneBoard.as_view(), name="board-item"),
#     path('boards/<int:board_id>/edit/', EditBoard.as_view(), name="board-edit"),
#     path('boards/<int:board_id>/remove/', RemoveBoard.as_view(), name="board-remove"),
#     path('users/login/', LoginUser.as_view(), name="login"),
#     path('users/singup/', CreateUsers.as_view(), name="singup"),
# ]
