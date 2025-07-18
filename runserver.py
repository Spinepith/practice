import os
import sys
import argparse
import subprocess


def runserver():
    parser = argparse.ArgumentParser(description="Запуск Django-проекта")

    parser.add_argument("--path", type=str, default=os.getcwd(), help="Указать путь к папке с 'manage.py'")
    parser.add_argument("--skip-check-path", action="store_true", help="Пропустить проверку наличия 'manage.py' в папке")

    args = parser.parse_args()

    path = args.path
    if not os.path.exists(os.path.join(path, "manage.py")):
        env = os.environ.copy()
        path = env.get("DJANGO_PROJECT_ROOT", path)

    if not args.skip_check_path:
        while not os.path.exists(os.path.join(path, "manage.py")):
            os.system("cls" if os.name == "nt" else "clear")
            print(f"# Django-проект не найден в папке: {path}\n")
            path = input("> Введите путь до папки с Django-проектом: ")
        os.system("cls" if os.name == "nt" else "clear")
    os.chdir(path)

    result = subprocess.run([sys.executable, "manage.py", "runserver"])
    if result.returncode != 0:
        print(f"* Код возврата: {result.returncode}")
        sys.exit(result.returncode)


if __name__ == "__main__":
    runserver()
