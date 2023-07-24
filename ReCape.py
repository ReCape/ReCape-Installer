# ReCape Installer
# Licensed under the MIT license

#Script Starts
import webbrowser
import customtkinter
import dns.resolver
import platform
import os
import subprocess
from PIL import Image, ImageTk, ImageDraw, ImageOps


# declare
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

if False:  # os.path.exists(".debug"):
    RECAPE_IP = "127.0.0.1"
else:
    RECAPE_IP = dns.resolver.resolve(RECAPE_URL)[0].to_text()


class App(customtkinter.CTk):
    
    def __init__(self):
        super().__init__()

        # Initialize the window
        self.title("ReCape Installer")
        self.geometry("900x450")
        self.resizable(0, 0)

        # Set the grid layout to 1x2
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # Set the icon of the window
        icon_path = os.path.join(os.path.dirname(__file__), "images", "icon_logo.ico")
        if os.path.exists(icon_path):
            self.iconbitmap(default=icon_path)

        self._generate_icons()

        self._generate_fonts()
        self._create_window()
    
    def _generate_icons(self):

        # Create the image path
        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "images")
        
        # Index of images and icons
        self.image_indexes = {
            "logo": (26, 26),
            "background": (500, 150)
        }
        self.icon_indexes = [
            "home",
            "info",
            "discord",
            "download",
            "close",
            "manual",
            "blc"
        ]
        self.icon_size = (20, 20)

        self.images = {}
        self.icons = {}

        for image in self.image_indexes.keys():
            self.images[image] = customtkinter.CTkImage( light_image=Image.open(os.path.join(image_path, image + ".png")), size=self.image_indexes[image] )
        
        for icon in self.icon_indexes:
            
            # Create light and dark sets of icons
            img_light = Image.open(os.path.join(image_path, icon + ".png"))
            img_dark = img_light.convert('RGBA')
            r, g, b, a = img_dark.split()
            r = g = b = r.point(lambda i: 255)
            img_dark = Image.merge('RGBA', (r, g, b, a))

            self.icons[icon] = customtkinter.CTkImage( light_image=img_light, dark_image=img_dark, size=self.icon_size)

    def _generate_fonts(self):

        # Create a font for the frame
        self.nav_font = customtkinter.CTkFont(size=15, weight="bold")

    def _create_window(self):
        self.frames = {}
        self.buttons = {}

        self._generate_nav_frame()
        self._generate_about_frame()
        self._generate_home_frame()

        self.select_frame_by_name("home")

    def _generate_nav_frame(self):

        # Create a frame for the list of buttons
        self.navigation_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.navigation_frame.grid(row=0, column=0, sticky="nsew")
        self.navigation_frame.grid_rowconfigure(4, weight=1)

        # Create the main logo
        self.navigation_frame_label = customtkinter.CTkLabel(
            self.navigation_frame,
            text=" ReCape!",
            image=self.images["logo"],
            compound="left",
            font=self.nav_font,
        )
        self.navigation_frame_label.grid(row=0, column=0, padx=20, pady=20)

        # Generate navigation buttons

        ## Home button
        self.home_button = customtkinter.CTkButton(
            self.navigation_frame,
            corner_radius=0,
            height=40,
            border_spacing=10,
            text="Home",
            fg_color="transparent",
            text_color=("gray10", "gray90"),
            hover_color=("gray70", "gray30"),
            image=self.icons["home"],
            anchor="w",
            command=self.home_button_event,
        )
        self.home_button.grid(row=1, column=0, sticky="ew")

        ## About button
        self.about_button = customtkinter.CTkButton(
            self.navigation_frame,
            corner_radius=0,
            height=40,
            border_spacing=10,
            text="About",
            fg_color="transparent",
            text_color=("gray10", "gray90"),
            hover_color=("gray70", "gray30"),
            image=self.icons["info"],
            anchor="w",
            command=self.about_button_event,
        )
        self.about_button.grid(row=2, column=0, sticky="ew")

        ## Discord button
        self.discord_server_button = customtkinter.CTkButton(
            self.navigation_frame,
            corner_radius=0,
            height=40,
            border_spacing=10,
            text="Discord",
            fg_color="transparent",
            text_color=("gray10", "gray90"),
            hover_color=("gray70", "gray30"),
            image=self.icons["discord"],
            anchor="w",
            command=self.discord_server_button_event,
        )
        self.discord_server_button.grid(row=3, column=0, sticky="ew")

        ## Appearance dropdown
        self.appearance_mode_menu = customtkinter.CTkOptionMenu(
            self.navigation_frame, values=["System", "Light", "Dark"], command=self.change_appearance_mode_event
        )
        self.appearance_mode_menu.grid(row=6, column=0, padx=20, pady=20, sticky="s")

    def _generate_home_frame(self):

        self.home_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.home_frame.grid_columnconfigure(0, weight=1)

        self.frames["home"] = self.home_frame
        self.buttons["home"] = self.home_button

        # Load and resize the image
        image = self.images["background"]

        # Create the label with rounded image
        self.home_frame_large_image_label = customtkinter.CTkLabel(
            self.home_frame, text="", image=image
        )
        self.home_frame_large_image_label.grid(row=0, column=0, padx=20, pady=10)

        self.status_box = customtkinter.CTkLabel(self.home_frame, text="")
        self.status_box.grid(row=1, column=0, padx=20, pady=10)

        self.custom_button = customtkinter.CTkButton(
            self.home_frame,
            text="Custom",
            image=self.icons["manual"],
            compound="left",
            command=get_installer_text,
        )
        self.custom_button.grid(row=2, column=0, padx=20, pady=10)

        self.install_button = customtkinter.CTkButton(
            self.home_frame, text="Install", image=self.icons["download"], compound="top", command=install
        )
        self.install_button.grid(row=3, column=0, padx=20, pady=10)

        self.blc_support_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=0, border_spacing=10, text="BLC Support", fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"), image=self.icons["blc"], anchor="w", command=blc_support_event
        )
        self.blc_support_button.grid(row=4, column=0, sticky="ew")

        self.uninstall_button = customtkinter.CTkButton(
            self.home_frame, text="Uninstall", image=self.icons["close"], compound="top", command=uninstall
        )
        self.uninstall_button.grid(row=4, column=0, padx=20, pady=10)

    def _generate_about_frame(self):
        self.about_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.about_frame.grid_columnconfigure(0, weight=1)

        self.frames["about"] = self.about_frame
        self.buttons["about"] = self.about_button
        
        self.about_header = customtkinter.CTkLabel(self.about_frame, text="About", font=self.nav_font)
        self.about_header.grid(row=0, column=0, padx=20, pady=10)

        self.about_info = customtkinter.CTkLabel(self.about_frame, text="ReCape Installer\nWritten by dedfishy and manthe.sh\nThank you!")
        self.about_info.grid(row=1, column=0, padx=20, pady=10)

    def select_frame_by_name(self, name):

        frames = list(self.frames.keys())

        if name in frames:

            frames.remove(name)

            self.frames[name].grid(row=0, column=1, sticky="nsew")
            self.buttons[name].configure(fg_color=("gray75", "gray25"))

            for frame in frames:
                self.frames[frame].grid_forget()
                self.buttons[frame].configure(fg_color="transparent")

    def home_button_event(self):
        self.select_frame_by_name("home")

    def about_button_event(self):
        self.select_frame_by_name("about")

    def discord_server_button_event(self):
        # Open Discord link in browser
        webbrowser.open("https://discord.gg/MY2DWCBZd4")

    def change_appearance_mode_event(self, new_appearance_mode):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def update_status_box(self, text):
        self.status_box.configure(text=text)

# Actual installer code

def install():
    try:
        with open(hosts_file_dir, "r") as hosts:
            content = hosts.readlines()
        with open(hosts_file_dir, "w") as hosts:
            content.append("\n" + RECAPE_IP + " " + OPTIFINE_URL + " #" + LINE_IDENTIFIER)
            hosts.write("".join(content))
    except PermissionError as e:
        print("Access Denied on Install")  # debug
        app.update_status_box(
            "Could not access your hosts file. \n You need to start ReCape as an administrator/root in order to do this. \n You can either Do a manual installation by yourself with the 'manual button' or \n run this installer as an administrator, root, or superuser."
        )
    else:
        status = "Installed successfully!"
        app.update_status_box(status)

def get_installer_text():
    print("Instruct has been sent")  # debug
    app.update_status_box(
        "You can install ReCape yourself by manually inputting text into your hosts file. \n On your system, this file should be located at \""
        + hosts_file_dir
        + "\". On a new line, put in this text:\n"
        + RECAPE_IP
        + " "
        + OPTIFINE_URL
        + " #"
        + LINE_IDENTIFIER
        + "\nSimilarly, you can uninstall ReCape by deleting that line in the hosts file later."
    )

def uninstall():
    try:
        with open(hosts_file_dir, "r") as hosts:
            content = hosts.readlines()
            for i in range(len(content)):
                if LINE_IDENTIFIER in content[i]:
                    content.pop(i)
                    break
        with open(hosts_file_dir, "w") as hosts:
            hosts.write("".join(content))
    except PermissionError:
        print("Access Denied on Uninstall")  # debug
        app.update_status_box(
            "Could not access your hosts file. \n You need to start ReCape as an administrator/root in order to do this. \n You can either Do a manual installation by yourself with the 'manual button' or \n run this installer as an administrator, root, or superuser."
        )
    else:
        status = "Uninstalled ReCape!"
        app.update_status_box(status)

def blc_support_event():
    if current_os != "Windows":
        app.update_status_box("Sorry, but BLC support is only available on Windows (for now).")
        return
    app.update_status_box("Running command as administrator...")
    command = 'attrib "C:\Windows\System32\drivers\etc\hosts" -s -h -r && attrib "C:\Windows\System32\drivers\etc\hosts" +s +r'
    try:
        subprocess.run(["cmd", "/c", "start", "/wait", "runas", "/user:Administrator", "cmd.exe", "/c", command])
    except Exception as e:
        app.update_status_box("Error running command: " + str(e))
    else:
        app.update_status_box("Completed successfully!")
# create and run app
app = App()
app.mainloop()