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

def open_template():
    with open("templates/default.tex") as f:
      return f.read()


template = open_template()

for key,value in scenario.items():
  template = template.replace(f"<{key}>", value)

print(template)

def save_scenario(raw_scenario, scenario_content):
    directory = None
    match raw_scenario["Scenario type"]:
      case "Coop":
        directory = "coops"
      case "Clash":
        directory = "clash"
      case "Campaign":
        directory = "campaigns"
    file_name = raw_scenario["Scenario Title"].lower().replace(" ", "_")
    with open(f"draft-scenarios/{directory}/{file_name}.tex", "w+") as f:
        f.write(scenario_content)
    with open(f"draft-scenarios/{directory}/main.tex", "a") as f:
        f.writelines(["\n\\clearpage", f"\n\n\\input{{{directory}/{file_name}.tex}}"])

save_scenario(scenario, template)
