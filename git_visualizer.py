import os
import sys
import git
import subprocess
from datetime import datetime

def generate_dependency_graph(repo_path, tag_name, plantuml_path):
    try:
        # Открыть репозиторий
        repo = git.Repo(repo_path)
        
        # Проверка на наличие тега
        if tag_name not in repo.tags:
            print(f"Tag '{tag_name}' not found.")
            return
        
        tag = repo.tags[tag_name]

        # Получаем историю коммитов начиная с тега
        commits = list(repo.iter_commits(f'{tag_name}..HEAD'))
        commits.reverse()  # Сделать их хронологическими

        # Сформировать данные для графа зависимостей в формате PlantUML
        plantuml_code = '@startuml\n'
        commit_map = {}

        for commit in commits:
            commit_map[commit.hexsha] = commit.message[:30]  # Первые 30 символов сообщения
            if commit.parents:
                for parent in commit.parents:
                    plantuml_code += f'    "{parent.hexsha[:7]}" --> "{commit.hexsha[:7]}"\n'

        plantuml_code += '@enduml\n'

        # Записать данные в .puml файл
        with open("graph.puml", "w") as f:
            f.write(plantuml_code)
        
        # Визуализировать с помощью PlantUML
        subprocess.run(["java", "-jar", plantuml_path, "-tpng", "graph.puml"])

        print("Graph visualization generated successfully.")
    
    except Exception as e:
        print(f"Error: {e}")

def main():
    if len(sys.argv) != 5:
        print("Usage: python git_visualizer.py --repo <repo_path> --tag <tag_name> --plantuml <path_to_plantuml.jar>")
        sys.exit(1)

    repo_path = sys.argv[2]
    tag_name = sys.argv[4]
    plantuml_path = sys.argv[6]

    generate_dependency_graph(repo_path, tag_name, plantuml_path)

if __name__ == '__main__':
    main()
