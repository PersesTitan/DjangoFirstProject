import os

from django.urls import path

from manage import Make, write_file


def admin_site(dirs):
    files = list()
    if os.path.isdir(f'../{dirs}') and os.path.isfile(f'../{dirs}/models.py'):
        file = open(f'../{dirs}/models.py', 'r')
        for line in file.readlines():
            if line.strip().startswith("class"):
                start = line.index("class") + len("class")
                end = line.index("(")
                class_name = line[start:end].strip()
                print(f'from {dirs}.models import {class_name}')
                exec(f'from {dirs}.models import {class_name}')

                files.append(eval(class_name))
    return files


def set_add_min(p: str, admin):
    for item in admin_site(p):
        admin.site.register(item)


def auto_my():
    os.system('python manage.py makemigrations')
    os.system('python manage.py migrate')


if __name__ == '__main__':
    write_file("/Users/persestitan/pythonProject/DjangoCustomUser/admin/settings.py")
    print(Make.add_path(path))
    print(Make.add_INSTALLED_APPS())
