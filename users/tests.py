import uuid

from django.test import TestCase
from django.test import Client

from board.models import Board
from users.models import User
from users.views import set_id, ID_REPOSITORY

client = Client(HTTP_REFERER='http://127.0.0.1:8000/')


# Create your tests here.
class CreateUserTest(TestCase):

    def print(self, text):
        print(f"   {text}")

    @classmethod
    def setUpClass(cls):
        for i in range(1, 10):
            cookie_id = 'test_id'
            user_id = f"TestUser{i}"
            data = {'id': user_id, 'password': "12345", 'password-check': "12345", "email": f"{i}@test.com"}
            client.post('/users/singup/', data)
            client.cookies['id'] = cookie_id
            set_id(cookie_id, User.objects.get(username=user_id))

            data = {'title': f"제목{i}", 'content': '내용'}
            client.post('/boards/add/', data)

    # 생성된 테스트 계정 출력
    def member_check(self):
        print(" - 생성된 맴버 출력")
        for user in User.objects.values():
            self.print(user)
        print(" - 생성된 블로그 출력")
        for blog in Board.objects.values():
            self.print(blog)

    # 유저 생성 테스트
    def member_create(self):
        username = "TestUser10"
        password = "12345"
        email = "Test10@test.com"
        before_size = len(User.objects.values())
        # 생성
        data = {'id': username, 'password': password, 'password-check': password, "email": email}
        client.post('/users/singup/', data)
        self.assertEqual(before_size + 1, len(User.objects.values()), "생성에 실패 하였습니다.")
        print(" - 생성된 유저")
        self.print(User.objects.last())  # 마지막 유저 데이터 가져오기
        return username, password, email

    # 로그인 테스트
    def member_login(self, username: str, password: str, email: str):
        print(" - 쿠키 제거 전")
        self.print(client.cookies.values())
        client.cookies.clear()
        self.assertEqual(len(client.cookies.values()), 0, "쿠키 값이 제거되지 않았음")
        print(" - 쿠키 제거 후")
        self.print(client.cookies.values())
        # 로그인 로직
        data = {'id': username, 'password': password, "email": email}
        client.post("/users/login/", data)
        login_user_id = client.cookies.get('id').value
        login_user = ID_REPOSITORY.get(login_user_id)
        self.assertEqual(login_user, User.objects.get(username=username), "로그인 값과 쿠키 값이 일치하지 않음")
        print(" - 로그인 완료")
        self.print(login_user)

    # 유저 정보 수정 테스트
    def member_logout(self):
        print(" - 로그아웃 전")
        self.print(client.cookies.values())
        client.post('/users/login/', {"logout": ""})
        print(" - 로그아웃 후")
        self.print(client.cookies.values())
        print(" - 유저 삭제")

    def member_edit(self):
        print(" - 수정 전")
        login_user_id = client.cookies.get('id').value
        login_user: User = ID_REPOSITORY.get(login_user_id)
        edit_after = User.objects.filter(pk=login_user.pk).values()[0]
        self.print(edit_after)
        print(" - 수정 후")
        data = {
            "username": "ChangeTester",
            "password": "abcdef",
            "password-check": "abcdef",
            "email": "ChangeEmail@test.com"
        }
        client.post(f"/users/edit/{login_user_id}/", data)
        edit_before = User.objects.filter(pk=login_user.pk).values()[0]
        self.print(edit_before)
        # 값이 일치하지 않으면 통과
        self.assertNotEqual(edit_after, edit_before, "값 수정 = 수정되지 않음")

    def board_create(self):
        print(" - 생성 전 갯수")
        after_board_len = len(Board.objects.values())
        self.print(after_board_len)

        user = ID_REPOSITORY.get(client.cookies.get("id").value)
        self.assertNotEqual(user, None, "로그인되어 있는 유저가 없습니다.")
        data = {"title": "추가 생성 블로그 제목", "content": "추가 생성 블로그 내용"}
        client.post('/boards/add/', data)

        print(" - 생성 후 갯수")
        before_board_len = len(Board.objects.values())
        self.print(before_board_len)
        self.assertEqual(after_board_len + 1, before_board_len, "생성에 실패하였습니다.")

        print(" - 생성한 블로그")
        self.print(list(Board.objects.values())[-1])

    def board_edit(self):
        print(" - 수정 전 정보")
        self.print(Board.objects.values())

    def test_member(self):
        print("생성된 데이터 출력 테스트")
        self.member_check()
        print("\n유저 생성 테스트")
        username, password, email = self.member_create()
        print("\n유저 로그인 테스트")
        self.member_login(username, password, email)
        print("\n유저 수정 테스트")
        self.member_edit()
        # 게시판 로직
        print("\n게시판 생성 테스트")
        self.board_create()
        print("\n게시판 수정 테스트")
        self.board_edit()
        print("\n로그아웃 테스트")
        self.member_logout()

    @classmethod
    def tearDownClass(cls):
        pass
