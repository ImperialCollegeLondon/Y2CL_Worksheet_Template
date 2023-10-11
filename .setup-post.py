import json

with open(".vscode/settings.json", "r") as settings_file:
    settings = json.load(settings_file)

settings["files.exclude"]['**/setup-linux.sh'] = True
settings["files.exclude"]['**/setup-windows.ps1'] = True

with open(".vscode/settings.json", "w") as settings_file:
    json.dump(settings, settings_file, indent=4)
