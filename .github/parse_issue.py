import sys
import pathlib
import pprint


issue_file = sys.argv[1]
issue_text = pathlib.Path(issue_file).read_text()

print(issue_text)

sections = [s.strip() for s in issue_text.split("###") if s]
print(sections)

scenario = {}
for section in sections:
  key, value = section.strip().split("\n\n")
  scenario[key] = value

pprint.pprint(scenario)
