import sys
import pathlib


issue_file = sys.argv[1]
issue_text = pathlib.Path(issue_file).read_text()

print(issue_text)

sections = issue_text.split("###")
print(sections)
