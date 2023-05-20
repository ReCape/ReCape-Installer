import pymsgbox
import dns.resolver
import platform
import os
current_os = platform.system()

print(current_os)

LINE_IDENTIFIER = "ADDED BY RECAPE"

try:
    hosts_file_dir = {
        "Windows": "C:\Windows\System32\drivers\etc\hosts",
        "Linux": "/etc/hosts",
        "Darwin": "/private/etc/hosts"
    }[current_os]
except KeyError:
    hosts_file_dir = "/etc/hosts"

OPTIFINE_URL = "s.optifine.net"
RECAPE_URL = "recape-server.boyne.dev"

if False: #os.path.exists(".debug"):
    RECAPE_IP = "127.0.0.1"
else:
    RECAPE_IP = dns.resolver.resolve(RECAPE_URL)[0].to_text()

def install():
    uninstall()
    try:

        with open(hosts_file_dir, "r") as hosts:
            content = hosts.readlines()
        with open(hosts_file_dir, "w") as hosts:
            content.append("\n" + RECAPE_IP + " " + OPTIFINE_URL + " #" + LINE_IDENTIFIER)
            hosts.write("".join(content))

    except PermissionError as e:

        return "Could not access your hosts file. You need to start ReCape as an administrator/root in order to do this. Do it yourself with the Do It Myself button or run this installer as an administrator, root, or superuser."

    return "Installed succesfully!"

def uninstall():
    try:
        with open(hosts_file_dir, "r") as hosts:
            content = hosts.readlines()
            for i in range(0, len(content)):
                if LINE_IDENTIFIER in content[i]:
                    content.pop(i)
                    break
        with open(hosts_file_dir, "w") as hosts:
            hosts.write("".join(content))
    except PermissionError:
        print("Access Denied")
        return "Could not access your hosts file. You need to start ReCape as an administrator/root in order to do this. Do it yourself with the Do It Myself button or run this installer as an administrator, root, or superuser."


    return "Uninstalled ReCape!"

def get_installer_text():
    return "You can install ReCape yourself by manually inputting text into your hosts file. On your system, this file should be located at \"" + hosts_file_dir + "\". On a new line, put in this text:\n" + RECAPE_IP + " " + OPTIFINE_URL + " #" + LINE_IDENTIFIER + "\nSimilarly, you can uninstall ReCape by deleting that line in the hosts file later."

while True:
    action = pymsgbox.confirm("Welcome to the ReCape installer!", "ReCape Installer", ["Install", "Uninstall", "Do It Myself", "Quit"])

    if action == "Install":
        result = install()
    elif action == "Uninstall":
        result = uninstall()
    elif action == "Do It Myself":
        result = get_installer_text()
    else:
        break

    next = pymsgbox.confirm(result, "ReCape Installer", ["Back", "Quit"])

    if next == "Quit":
        break