import os
import subprocess
import argparse
import git
import plantuml
import tempfile
import shutil


def generate_commit_graph(repo_path, tag, plantuml_path):
    # Проверим, существует ли репозиторий
    if not os.path.isdir(repo_path):
        print(f"Ошибка: Путь {repo_path} не является репозиторием Git.")
        return
    
    try:
        # Открываем репозиторий
        repo = git.Repo(repo_path)
    except git.exc.InvalidGitRepositoryError:
        print(f"Ошибка: Путь {repo_path} не является действительным репозиторием Git.")
        return

    # Проверяем, существует ли указанный тег
    try:
        repo.git.checkout(tag)
    except git.exc.GitCommandError:
        print(f"Ошибка: Тег {tag} не найден в репозитории.")
        return
    
    # Генерация графа коммитов
    commit_log = repo.git.log("--pretty=format:'%H %s'")
    print(f"Лог коммитов:\n{commit_log}")
    
    # Формирование содержимого для PlantUML
    plantuml_content = '@startuml\n'
    for commit in commit_log.splitlines():
        commit_hash, commit_message = commit.split(" ", 1)
        plantuml_content += f"commit {commit_hash} : {commit_message}\n"
    plantuml_content += '@enduml\n'

    # Сохранение в временный файл для передачи в PlantUML
    with tempfile.NamedTemporaryFile(delete=False, mode='w', suffix=".puml") as temp_file:
        temp_file.write(plantuml_content)
        temp_puml_file = temp_file.name

    # Запуск PlantUML
    try:
        subprocess.run(["java", "-jar", plantuml_path, temp_puml_file], check=True)
        print(f"Граф коммитов успешно сгенерирован и сохранен в {temp_puml_file}.")
    except subprocess.CalledProcessError as e:
        print(f"Ошибка при запуске PlantUML: {e}")
    finally:
        # Удаляем временный файл
        os.remove(temp_puml_file)


def main():
    parser = argparse.ArgumentParser(description="Git Commit Visualizer")
    parser.add_argument('--repo', required=True, help='Путь к репозиторию Git')
    parser.add_argument('--tag', required=True, help='Тег репозитория')
    parser.add_argument('--plantuml', required=True, help='Путь к файлу plantuml.jar')

    args = parser.parse_args()

    # Печать входных данных для отладки
    print(f"Репозиторий: {args.repo}")
    print(f"Тег: {args.tag}")
    print(f"PlantUML: {args.plantuml}")

    # Вызов функции для генерации графа
    generate_commit_graph(args.repo, args.tag, args.plantuml)


if __name__ == "__main__":
    main()
