from asc.main import cli
import click
import os
import subprocess

@cli.command("make.controller")
@click.argument('controller_name')
def generate_controller_file(controller_name):
    # Определяем путь к директории для контроллеров
    controllers_dir = os.path.join("app", "http", "controllers")
    
    # Создаем директорию для контроллера, если она не существует
    if not os.path.exists(controllers_dir):
        os.makedirs(controllers_dir)
    
    # Формируем полный путь к файлу контроллера
    controller_file = os.path.join(controllers_dir, f"{controller_name}.py")
    
    # Генерируем содержимое файла контроллера
    content = f"""
class {controller_name}():
    pass
"""
    
    # Записываем содержимое в файл
    with open(controller_file, "w") as file:
        file.write(content)
    
    print(f"Контроллер {controller_name} успешно создан по пути {controller_file}")


@cli.command("install")
def package_install():
    packages_dir = "packages"  # Путь к папке с пакетами
    for package in os.listdir(packages_dir):
        package_path = os.path.join(packages_dir, package)
        if os.path.isdir(package_path):
            setup_path = os.path.join(package_path, "setup.py")
            pyproject_path = os.path.join(package_path, "pyproject.toml")
            if os.path.exists(setup_path) or os.path.exists(pyproject_path):
                # Запуск скрипта setup.py для установки пакета
                subprocess.run(["pip", "install", package_path])
                print(f"Package {package} installed successfully.")
            else:
                print(f"Package {package} does not contain setup.py.")
