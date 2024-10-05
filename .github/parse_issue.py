import sys
import pathlib
import pprint


issue_file = sys.argv[1]
issue_text = pathlib.Path(issue_file).read_text()

print("Raw issue text:")
print(issue_text)

sections = [s.strip() for s in issue_text.split("###") if s]
print("Raw issue sections:")
pprint.pprint(sections)


def tier_to_svg(value):
    return value.replace("Bronze", "\\svgunit{bronze}").replace("Silver", "\\svgunit{silver}").replace("Gold", "\\svgunit{gold}")

def parse_town_buildings(value):
    buildings = ", ".join([v[6:].strip() for v in value.split("\n") if v.startswith("- [X]")])
    return tier_to_svg(buildings)

def parse_units(value):
    units = [u[6:].strip() for u in value.split("\n") if u.startswith("- [X]")]
    latex_units = "\n  \\item ".join(units)
    return "\n  \\item " + tier_to_svg(latex_units)


def parse_bonus(value):
    if value == "_No response_":
        return "None"
    lines = value.split("\n")
    if len(lines) == 1:
        return lines[0].strip()
    output = "\n\\begin{itemize}\n"
    for line in lines:
        output += f"  \\item {line.strip()}\n"
    output += "\\end{itemize}"
    return output

scenario = {}
for section in sections:
    key, value = section.strip().split("\n\n")
    if key == "Town Buildings":
        value = parse_town_buildings(value)
    elif key == "Starting Units":
        value = parse_units(value)
    elif key == "Additional Bonus":
        value = parse_bonus(value)
    scenario[key] = value


print("Parsed scenario:")
pprint.pprint(scenario)

def open_template():
    with open("templates/default.tex") as f:
      return f.read()


template = open_template()

for key,value in scenario.items():
    template = template.replace(f"<{key}>", value)

print("Rendered template:")
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
