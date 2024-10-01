import sys
import pathlib


issue_file = sys.argv[1]
issue_text = pathlib.Path(issue_file).read_text().splitlines(False)

print(issue_text)
