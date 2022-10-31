#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def get_class(pa: str, class_name: str, url: str, path, name=None):
    exec(f"from {pa}.views import {class_name}")
    if name is None:
        return eval(f"path(\'{url}\', {class_name}.as_view())")
    else:
        return eval(f"path(\'{url}\', {class_name}.as_view(), name=\"{name}\")")


class Make:
    @classmethod
    def add_INSTALLED_APPS(cls, pwd=str(os.getcwd())):
        INSTALLED_APPS_LIST = list()
        for dirs in os.listdir(pwd):
            if os.path.isdir(f'{pwd}/{dirs}') and os.path.isfile(f'{pwd}/{dirs}/apps.py'):
                file = open(f'{pwd}/{dirs}/apps.py', 'r')
                for line in file.readlines():
                    if line.strip().startswith("class"):
                        start = line.index("class") + len("class")
                        end = line.index("(")
                        INSTALLED_APPS_LIST.append(f"{dirs}.apps.{line[start:end].strip()}")
        return set(INSTALLED_APPS_LIST)

    @classmethod
    def add_path(cls, path, pwd=str(os.getcwd())):
        path_list = list()
        for dirs in os.listdir(pwd):
            if os.path.isdir(f'{dirs}') and os.path.isfile(f'{dirs}/views.py'):
                file = open(f'{dirs}/views.py', 'r')
                for line in file.readlines():
                    if line.strip().startswith("class"):
                        start = line.index("class") + len("class")
                        end = line.index("(")

                        remark = line[line.index("#") + 1:].strip().split()
                        if not remark:
                            path_list.append(get_class(dirs, line[start:end].strip(), '', path))
                        elif len(remark) == 1:
                            path_list.append(get_class(dirs, line[start:end].strip(), remark[0], path))
                        else:
                            path_list.append(get_class(dirs, line[start:end].strip(), remark[0], path, remark[1]))
        return set(path_list)


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'admin.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
