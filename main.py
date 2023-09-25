import os, pick

def intense_warning():
    os.system("cls && color 47")
    input("IF YOU HAVE BOUGHT THIS TOOL SEPERATELY OR AS PART OF A BUNDLE, YOU HAVE BEEN SCAMMED!\n\nTHIS TOOL IS FREE SOFTWARE, PLEASE ASK THE SELLER FOR YOUR MONEY BACK\nAND DOWNLOAD FROM AN OFFICIAL SEVENWORKS.EU.ORG SERVICE BECAUSE THE SELLER\nCOULD HAVE IMPLEMENTED A MALICIOUS SCRIPT WHICH COULD HARM YOUR DEVICE.\n\nTHANK YOU!\n\nPress enter to continue...")
    os.system("cls && color 07")

intense_warning()

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def tool1():
    input("hello there")

def tool2():
    input("hello there again")

def tool3():
    input("yuh huh!")

def display_menu():
    options = [
        "Tool 1",
        "Tool 2",
        "Tool 3"
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

            if choice == "Tool 1":
                tool1()
            elif choice == "Tool 2":
                tool2()
            elif choice == "Tool 3":
                tool3()
            
        os.system('color 07')

    except KeyboardInterrupt:
        os.system("color 07")