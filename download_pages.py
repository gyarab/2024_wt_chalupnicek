#!./venv/bin/python3

# For each item in repo_list.txt download referat.md file as ./referaty/pages/[referat title].md

import httpx
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")

def get_file(repo_name, url, target_dir):
    subject = f"no_subject_{repo_name}"

    response = httpx.get(url)
    text = response.text

    # try to find subject in markdown headline
    text_lines = text.split('\n')
    for line in text_lines:
        if line.startswith("# "):
            subject = line[1:].strip()[:30]
            break

    # prepend link to original repo
    text = f"from <https://github.com/gyarab/{repo_name}>\n\n{text}"

    out_file_name = subject.replace(' ', '_')
    out_file_name = re.sub('[^a-zA-Z0-9_-]+', '', out_file_name)
    out_file_name += ".md"

    print(f"                        {out_file_name}     {subject}")

    with open(f"referaty/docs/{target_dir}/{out_file_name}", "w", encoding='utf-8') as out_file:
        out_file.write(text)


with open("repo_list.txt") as file:
    for repo_name in file.readlines():
        repo_name = repo_name.strip()
        if repo_name.startswith('#'):
            continue
        if not repo_name:
            continue
        print(f"{repo_name}")

        base_url = f"https://raw.githubusercontent.com/gyarab/{repo_name}/refs/heads/main/"

        get_file(repo_name, base_url + "referat.md", "computer_pioneers")
        get_file(repo_name, base_url + "color.md", "brands")
