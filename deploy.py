import os
import sys
import argparse
import getpass
import subprocess


def run_command(command: list, env: dict = None):
    result = subprocess.run(command, env=env)
    if result.returncode != 0:
        print(f"* Ошибка при выполнении команды: {' '.join(command)}")
        print(f"* Код возврата: {result.returncode}")
        sys.exit(result.returncode)


def deploy():
    parser = argparse.ArgumentParser(description="Запуск Django-проекта")

    parser.add_argument("--path", type=str, default=os.getcwd(), help="Указать путь к папке с 'manage.py'")
    parser.add_argument("--skip-check-path", action="store_true", help="Пропустить проверку наличия 'manage.py' в папке")
    parser.add_argument("--without-requirements", action="store_true", help="Не устанавливать зависимости")
    parser.add_argument("--skip-migrations", action="store_true", help="Не применять миграции")
    parser.add_argument("--skip-create-superuser", action="store_true", help="Пропустить создание суперпользователя")
    parser.add_argument("--username", type=str, help="Имя суперпользователя")
    parser.add_argument("--email", type=str, help="Email суперпользователя")
    parser.add_argument("--password", type=str, help="Пароль суперпользователя")

    args = parser.parse_args()

    env = os.environ.copy()

    path = args.path
    if not os.path.exists(os.path.join(path, "manage.py")):
        path = env.get("DJANGO_PROJECT_ROOT", path)

    if not args.skip_check_path:
        while not os.path.exists(os.path.join(path, "manage.py")):
            os.system("cls" if os.name == "nt" else "clear")
            print(f"# Django-проект не найден в папке: {path}\n")
            path = input("> Введите путь до папки с Django-проектом: ")
        os.system("cls" if os.name == "nt" else "clear")
    os.chdir(path)

    if not args.without_requirements and os.path.exists("requirements.txt"):
        print("# Установка зависимостей\n")
        run_command([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print()

    if not args.skip_migrations:
        print("# Выполнение миграций")
        run_command([sys.executable, "manage.py", "migrate"])

    if not args.skip_create_superuser:
        try:
            if not all([args.username, args.email, args.password]):
                print("\nДля отмены нажмите Ctrl+C")

            if not args.username:
                args.username = input("> Введите имя суперпользователя: ").strip()
            if not args.email:
                args.email = input("> Введите email суперпользователя: ").strip()
            if not args.password:
                args.password = getpass.getpass("> Введите пароль суперпользователя: ").strip()

            env["DJANGO_SUPERUSER_PASSWORD"] = args.password

            run_command(
                [
                    sys.executable, "manage.py", "createsuperuser",
                    "--noinput",
                    f"--username={args.username}",
                    f"--email={args.email}"
                ],
                env=env
            )
        except KeyboardInterrupt:
            pass

    print("\n# РАЗВЕРТЫВАНИЕ УСПЕШНО ЗАВЕРШЕНО\n")


if __name__ == "__main__":
    deploy()
