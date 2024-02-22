"""
python convert_nb.py
    --files <path_to_ipynb1> <path_to_ipynb2> ...
    --rh-repo <path_to_local_rh_git_folder>
"""

import os
import subprocess

from argparse import ArgumentParser
from pathlib import Path


def reformat_rst_file(
    rst_file: str,
    ipynb_file: str,
):
    print(f"Applying formatting updates to {rst_file}")

    with open(rst_file, "r") as file:
        data = file.readlines()

    # display and formatting updates
    replacements = [
        (".. code:: python", ".. code:: ipython3"),
        (
            ".. parsed-literal::\n",
            ".. parsed-literal::\n    :class: code-output\n",
        ),
    ]
    for replacement in replacements:
        data = [line.replace(replacement[0], replacement[1]) for line in data]

    # add colab badge and link out
    colab_lines = [
        ".. raw:: html\n",
        "\n",
        f'    <p><a href="https://colab.research.google.com/github/run-house/notebooks/blob/stable/{ipynb_file}">\n'
        '    <img height="20px" width="117px" src="https://colab.research.google.com/assets/colab-badge.svg" \
alt="Open In Colab"/></a></p>\n',
        "\n",
    ]

    data = data[:3] + colab_lines + data[3:]

    with open(rst_file, "w") as file:
        file.writelines(data)


def convert_to_rst(ipynb_file, dest_folder):
    subprocess.run(f"jupyter nbconvert --to rst {ipynb_file}", shell=True)

    output_path = ipynb_file.replace(".ipynb", ".rst")
    target_path = os.path.join(
        dest_folder, output_path.replace("docs/", "docs/tutorials/")
    )

    print(f"Moving rst file from {output_path} to {target_path}")
    os.rename(output_path, target_path)

    return target_path

def run_precommit(rst_file, gh_repo):
    try:
        subprocess.run(f"pre-commit run --files {rst_file}", cwd=gh_repo, shell=True)
        print("Applying pre-commit")
    except:
        print("Unable to apply pre-commit")


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument(
        "--files",
        nargs="+",
        default=None,
        help="Paths of .ipynb files to convert. If not provided, will convert all .ipynb files found in the directory.",
    )
    parser.add_argument(
        "--rh-repo",
        default="../runhouse",
        help="Path to runhouse github repo, where the formatted rst will automatically be put into the correct folder.",
    )

    args = parser.parse_args()

    files = args.files or Path(os.getcwd()).rglob("*.ipynb")
    dest_folder = args.rh_repo

    if not os.path.exists(dest_folder):
        raise ValueError(f"Please pass in a valid path for the runhouse git repo, using the --rh-repo argument.")

    for ipynb_file in files:
        ipynb_file = str(os.path.relpath(ipynb_file))
        rst_file = convert_to_rst(ipynb_file, dest_folder)
        reformat_rst_file(rst_file, ipynb_file)
        run_precommit(rst_file, dest_folder)
