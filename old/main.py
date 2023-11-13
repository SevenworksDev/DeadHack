import os, pick, shutil, urllib.request, time
from pathlib import Path

def clear(): os.system('cls' if os.name == 'nt' else 'clear')

banner = """
---------=----------------------------=-----------------
---------=--------------=-::----------=-----------------
---------=------------=-..=:.:--------=-----------------
---------=----------=-..=#%#+..:------=-----------------
---------=--------=-..=#%#####+..:=---=-----------------
---------=------=-..=#%##%######+..:=-=-----------------          .==                         .==
---------==---=-..=#%%#%%*#%######=..-==----------------        ..=@@.    ::.    ..:.       ..-@@.
---------====-:.=#%%#%%*:::=#%######=..-----------------     .*@@#%@@. :##**%#: :#**#@#: .*@@##@@.
---------==-..=#%%%%%*:-*%#=:=########=..-=-------------     #@#  -@@. @@#++%@# .-++*@@+ *@%  :@@.
==========..=#%%%%%%%*:-*%#=:=#%%++#####=..-=-----------     #@%. =@@. @@#--:-- %@#::@@+ *@%. =@@.
------=-..-#%%#%%**%%%%*--:=#%%*:.::+#####=..-==-====-=-     .*@%#*%%. .*%####+ +%%*+#%= .*%%#*%%.
------..-#%%#%%*-::-#%%%%*#%%*:.=##+ :*#####=..--------:                   ..
----:.-#%###%#::*%%+:-#%#%%*-.=###+:-*#######*=.:----:::     :**.   **=                   +%*
---: =%%####%#--*%#+:=#%%*-.=#%%+::*#######***#+ .::::::     =@@:   @@*  =++++-.   :=**+- *@%  -=-
:::-: :+#####%%*-::=#%%*-.=#%%+::*%####******+: .:::::::     -@@%%%%@@*  ===+%@%  #@%+=+* *@#:#@*.
::::::. :+######%**%%*-.=#%%+::+##*********+: .:::::::::     -@@=:::@@* .+#*=*@@ :@@:     *@@%@%
::::::::. :+#######+-.-*##+::+##*********+: .:::::::::::     =@@:   @@* =@@=-*@@  #@%+=+* *@% +@@-
:::::::::-. :+###*#= :*#+::+##*********+: .:::::::::::::     .==.   -=:  -++=-==   :=+*+- :=-  :==
:::::::::---. :+##*#*-..:+##*********+: .:::::::::::::::
:::::::::-::::. :+#**#*+##*********+: .:::::::::::::::::
:::::::::-::::::. :+*************+: .:-:::::::::::::::::
:::::::::-::::::::. :+*********+- .:::--::::::::::::::::
:::::::::--:::::::-:. :+*****+- .:-:::-:::::::::::::::::
:::::::::-::::::::::::. :+*+- .:::::::::::::::::::::::::
:::::::::-::::::::::::::. :..:::::::::::::::::::::::::::
:::::::::-::::::::::::::::::::::::::::::::::::::::::::::
:::::::::-::::::::::::::::::::::::::::::::::::::::::::::
:::::::::-::::::::::::::::::::::::::::::::::::::::::::::
:::::::::-::::::::::::::::::::::::::::::::::::::::::::::
DEADHACK AND ITS CONTENTS ARE FREE SOFTWARE, IF YOU HAVE PURCHASED THIS SEPERATELY OR BUNDLED THEN YOU HAVE BEEN SCAMMED! PLEASE DELETE THIS AND DOWNLOAD A LEGIT COPY OF DEADHACK THROUGH ANY SOURCE ON SEVENWORKS.EU.ORG, THANKS!
"""
print(banner)
time.sleep(2.5)
clear()

user_home = str(Path.home())
output_directory = os.path.join(user_home, ".sevenworks") if os.name == 'posix' else os.path.join(user_home, ".sevenworks")

version = "0.1"

file_urls = [
    "https://github.com/SevenworksDev/DeadHack/raw/main/robtop-hate-gang/Proxy_Server.exe",
    "https://github.com/SevenworksDev/DeadHack/raw/main/robtop-hate-gang/Tunnel_(For_GDProxy).exe",
    "https://github.com/SevenworksDev/DeadHack/raw/main/robtop-hate-gang/Song_Server_Location_Finder.exe",
    "https://github.com/SevenworksDev/DeadHack/raw/main/robtop-hate-gang/Level_Report_Spam.exe",
    "https://github.com/SevenworksDev/DeadHack/raw/main/robtop-hate-gang/Find_All_Users.exe",
    "https://github.com/SevenworksDev/DeadHack/raw/main/robtop-hate-gang/Comment_Downloader.exe",
    "https://github.com/SevenworksDev/DeadHack/raw/main/robtop-hate-gang/Message_Spammer_(Find_User_in_Recent_Tab_Method).exe",
    "https://github.com/SevenworksDev/DeadHack/raw/main/robtop-hate-gang/Message_Spammer.exe",
    "https://github.com/SevenworksDev/DeadHack/raw/main/robtop-hate-gang/GDPS_Account_Creator.exe",
    "https://github.com/SevenworksDev/DeadHack/raw/main/robtop-hate-gang/Comment_Filter_Bypass.exe",
    "https://github.com/SevenworksDev/DeadHack/raw/main/robtop-hate-gang/Comment_Spam_(Single_Account).exe",
    "https://github.com/SevenworksDev/DeadHack/raw/main/robtop-hate-gang/GDPS_Likebot.exe",
    "https://github.com/SevenworksDev/DeadHack/raw/main/robtop-hate-gang/GD_Remote_PC.exe"
]

time.sleep(4)
clear()

def download_files(file_urls, output_directory):
    for url in file_urls:
        filename = url.split('/')[-1]
        filepath = os.path.join(output_directory, filename)
        urllib.request.urlretrieve(url, filepath)
        print(f"Downloaded: {filename}")

if not os.path.exists(output_directory):
    print(f'Welcome to deadHack {version}, One of the most badass hack menus in Geometry Dash!\n\nSince your [.sevenworks] folder is missing in your user folder, This will now install all tools as compiled executables so you dont have to install Python 3.8 or anything extra.\n\n\nPress enter to continue...')
    input()
    os.makedirs(output_directory)
    download_files(file_urls, output_directory)

def display_menu():
    files = os.listdir(output_directory)
    options = [
        filename.replace('_', ' ').replace('.exe', '') for filename in files
    ]

    title = "Select a tool:"
    picker = pick.Picker(options, title)
    tool = picker.start()

    return tool[0] if tool else None

if __name__ == "__main__":
    os.system('color 17')

    try:
        while True:
            clear()
            choice = display_menu()

            if choice is None:
                break

            selected_filename = choice.replace(' ', '_') + '.exe'
            selected_filepath = os.path.join(output_directory, selected_filename)
            os.system(selected_filepath)

        os.system('color 07')

    except KeyboardInterrupt:
        os.system("color 07")
