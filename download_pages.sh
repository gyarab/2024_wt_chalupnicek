#!./venv/bin/python3

# For each item in repo_list.txt download README.md file as ./referaty/pages/[README title].md

import httpx
import re

with open("url_list.txt") as file:
    for url in file.readlines():
        url = url.strip()
        if url.startswith('#'):
            continue
        if not url.startswith("http"):
            continue

        author = "no_author"
        matches = re.findall(r'/gyarab/(.*)/refs/', url)
        if matches:
            author = matches[0]
        subject = f"no_subject_{author}"

        print(f"{author}")
        response = httpx.get(url)
        text = response.text

        # try to find subject in markdown headline
        text_lines = text.split('\n')
        for line in text_lines:
            if line.startswith("# "):
                subject = line[1:].strip()[:20]
                break

        # prepend link to original repo
        text = f"from <https://github.com/gyarab/{author}>\n\n{text}"

        out_file_name = subject.replace(' ', '_')
        out_file_name = re.sub('[^a-zA-Z0-9_-]+', '', out_file_name)
        out_file_name += ".md"

        print(f"                        {out_file_name}     {subject}")

        with open(f"referaty/docs/pages/{out_file_name}", "w") as out_file:
            out_file.write(text)
