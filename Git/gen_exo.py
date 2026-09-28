import os
import sys

# Découpage du texte en 18 blocs logiques et indivisibles
BLOCKS = [
    # --- Bloc 1 à 8 : Git & Git-SCM ---
    "## 1. Introduction to Git\nGit is a distributed version control software system that is capable of managing versions of source code or data. It is often used to control source code by programmers who are developing software collaboratively. It was originally created by Linus Torvalds for version control in the development of the Linux kernel.",
    "### Git is fast\nGit was built to work on the Linux kernel, meaning that it was built to handle repositories with tens of millions of lines of code from the start. Speed and performance has always been a primary design goal of Git.",
    "Git also stores repository history efficiently. As of 2025, the current version of the Linux kernel's source code is 1.7 GB. Git stores the full history of the Linux project (1.4 million commits) in only 5.5 GB.",
    "### Git is widely used\nAccording to the 2022 Stack Overflow developer survey, 96% of professional developers use Git.",
    "### Huge ecosystem of tools\nThe core Git project is just a command-line tool, but Git exploded in popularity in the early 2010s thanks to Git hosting services like GitLab, GitHub, and more.",
    "Since Git was created, many GUIs, editor integrations, and command line tools have been built to make working with Git more convenient. Your favorite developer tools might already have a built-in Git integration.",
    "### Free and Open Source\nGit is released under the GNU General Public License version 2.0, which is an open source license. The Git project chose to use GPLv2 to guarantee your freedom to share and change free software---to make sure the software is free for all its users.",
    "However, we do restrict the use of the term \"Git\" and the logos to avoid confusion. Please see our trademark policy for details.",
    # --- Bloc 9 à 13 : Théorie du README ---
    "## 2. What is a README.md?\nA README.md is an important document in a repository that introduces the project and explains its purpose, setup, and usage to help users and developers understand and contribute to it.",
    "- Uses Markdown (.md) for formatted documentation and is usually the first file users read in a project.\n- Provides a project overview, installation instructions, configuration details, and usage examples such as code or command-line commands.\n- May include license information, contributor credits, and appears well-formatted on platforms like GitHub.",
    "### Basic Structure of README.md\nA typical README.md may include the following sections:\n- **Project Title**: The name of project, usually written as a main heading in Markdown.\n- **Description**: A short explanation of what the project does and its purpose.",
    "- **Installation**: Steps required to set up and install the project locally.\n- **Usage**: Examples showing how to run or use the project.\n- **Contributing**: Guidelines for developers who want to contribute.",
    "- **License**: Information about the software license (e.g., MIT License, Apache License).\n- **Contact**: Maintainer's email or other contact information for support or queries.",
    # --- Bloc 14 à 18 : Exemple pratique & Utilité ---
    "## 3. Example of README.md\n```markdown\n# My First Project\n\n## Description\nThis project helps users manage tasks efficiently.\n```",
    "```markdown\n## Installation\n1. Clone the repository\n2. Run `npm install`\n3. Start the server with `npm start`\n\n## Usage\nVisit `http://localhost:3000` in your browser to use the application.\n```",
    "```markdown\n## Contributing\nFeel free to submit pull requests or open issues.\n\n## License\nMIT License\n\n## Contact\nEmail: example@domain.com\n```",
    "## 4. Purpose of README.md\nThe primary purpose of a README.md file is to provide essential information about the project. This includes:\n- **Project Overview**: Explains what the project is about and its main features.\n- **Installation Instructions**: Guides users on how to install and set up the project.",
    "- **Usage Instructions**: Shows how to use the project effectively.\n- **Contributing Guidelines**: Instructions for developers who want to contribute.\n- **License & Contact**: Specifies the license and how to reach the maintainer.",
]


def split_text(num_participants):
    # Répartition équilibrée des blocs
    k, m = divmod(len(BLOCKS), num_participants)
    parts = []
    start = 0
    for i in range(num_participants):
        end = start + k + (1 if i < m else 0)
        parts.append("\n\n".join(BLOCKS[start:end]))
        start = end
    return parts


def main():
    if len(sys.argv) < 2:
        print("Usage : python preparer_tp.py <nombre_de_participants>")
        print("Exemple : python preparer_tp.py 8")
        sys.exit(1)

    n = int(sys.argv[1])
    parts = split_text(n)

    # 1. Création du fichier initial pour le dépôt Git
    with open("DOCUMENT_INITIAL.md", "w", encoding="utf-8") as f:
        f.write("# Exercice\n\n")
        f.write(
            "> Ce document est incomplet. Chaque participant doit insérer sa partie à l'emplacement prévu !\n\n"
        )
        for i in range(1, n + 1):
            f.write(f"<!-- DEBUT_PARTIE_{i} -->\n")
            f.write(f"<!-- FIN_PARTIE_{i} -->\n\n")

    # 2. Création des fiches individuelles pour chaque participant
    os.makedirs("fiches_participants", exist_ok=True)
    for i, part in enumerate(parts, 1):
        filename = f"fiches_participants/participant_{i:02d}.txt"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(
                f"=== TU ES LE PARTICIPANT {i}/{n} ===\n"
                f"Consigne : Insère le texte ci-dessous entre :\n"
                f"<!-- DEBUT_PARTIE_{i} --> et <!-- FIN_PARTIE_{i} -->\n\n"
                f"{part}\n"
            )

    print(f" Succès ! {n} parts générées pour {n} participants.")
    print(" Fichier pour le repo créé : 'DOCUMENT_INITIAL.md'")
    print(f" Fiches individuelles créées dans le dossier : 'fiches_participants/'")


if __name__ == "__main__":
    main()
