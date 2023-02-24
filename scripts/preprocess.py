import re
import os
from pathlib import Path
import logging

regex = (
    # opening tag and any whitespace
    r"{%\s*"
    # include-markdown literal and more whitespace
    r"include-markdown\s*"
    # the path in double-quotes (unvalidated)
    r'\"(.*)\"'
    # more whitespace and closing tag
    r"\s*%}"
)


for root, dirs, files in os.walk("docs"):
    for file in files:
        # only process md files
        if re.fullmatch(r".*\.md", file):
            with open(Path(root) / file, "r") as f:
                current_text = f.read()
            if re.search(regex, current_text):
                # if we have an include tag, replace text and overwrite
                include_path = re.search(regex, current_text).group(1)
                try:
                    with open(Path(root) / include_path) as f_inc:
                        include_text = f_inc.read()
                        new_text = re.sub(regex, include_text, current_text)
                        with open(Path(root) / file, "w") as f:
                            f.write(new_text)
                # if we can't find include file then warn but carry on
                except FileNotFoundError as e:
                    logging.warning(f"Couldn't find specified include file: {e}")
