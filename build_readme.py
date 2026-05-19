import requests
from bs4 import BeautifulSoup
import pathlib
import re
import sys

ROOT_PATH = pathlib.Path(__file__).parent.resolve()
FEED_URL = 'https://github.com/Niketkumardheeryan/Hands-on-ML-Basic-to-Advance-'

def replace_chunk(content, marker, chunk, inline=False):
    r = re.compile(
        r"<!\-\- {} start \-\->.*<!\-\- {} end \-\->".format(marker, marker),
        re.DOTALL,
    )
    if not inline:
        chunk = "\n{}\n".format(chunk)
    chunk = "<!-- {} start -->{}<!-- {} end -->".format(marker, chunk, marker)
    return r.sub(chunk, content)

def Exract_files_names():
    try:
        req = requests.get(FEED_URL, timeout=10)
        req.raise_for_status()
    except requests.exceptions.Timeout:
        print("ERROR: Request timed out. GitHub may be rate-limiting or unreachable.")
        sys.exit(1)
    except requests.exceptions.HTTPError as e:
        print("ERROR: HTTP error occurred: {}".format(e))
        sys.exit(1)
    except requests.exceptions.ConnectionError:
        print("ERROR: Failed to connect. Check your internet connection.")
        sys.exit(1)
    except requests.exceptions.RequestException as e:
        print("ERROR: An unexpected error occurred: {}".format(e))
        sys.exit(1)

    soup = BeautifulSoup(req.text, 'html.parser')
    temp = []
    li = soup.findAll('div', class_="Box-row Box-row--focus-gray py-2 d-flex position-relative js-navigation-item")

    if not li:
        print("ERROR: Could not parse any project folders. The page structure may have changed.")
        sys.exit(1)

    for i in li:
        for x in i.findAll('a', class_="js-navigation-open Link--primary"):
            if (x.text != ".github" and x.text != "CODE_OF_CONDUCT.md" and x.text != "CONTRIBUTING_GUIDELINES.md" and x.text != ".github/workflows" and x.text != "build_readme.py" and x.text != "requirements.txt" and x.text != "README.md" and x.text != "download statistics.jpg" and x.text != "img" and x.text != "ml img.jpg"):
                temp2 = {
                    'fname': x.text,
                    'furl': x["href"].split('/')[-1]
                }
                temp.append(temp2)
    return temp

if __name__ == "__main__":
    readme = ROOT_PATH / "README.md"
    readme_contents = readme.open().read()
    file_names = Exract_files_names()
    file_md = "\n\n".join(["- {}".format(i) for i in file_names])
    file_md = "\n".join(
        ["| [{fname}]({furl}) |".format(**i) for i in file_names]
    )
    readme_contents = replace_chunk(readme_contents, "Projects", "| Content List | \n | --------------- | \n" + file_md)
    readme.open("w").write(readme_contents)
    print("README.md updated successfully.")