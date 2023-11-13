import os, json, subprocess
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk

class deadHack:
    def __init__(self, root):
        self.root = root
        self.root.title("SevenworksMod Tool")

        self.notebook = ttk.Notebook(root)

        self.run_tab = ttk.Frame(self.notebook)
        self.download_tab = ttk.Frame(self.notebook)

        self.notebook.add(self.run_tab, text='Run')
        self.notebook.add(self.download_tab, text='Download')

        try:
            self.init_run_tab()
        except Exception as e:
            self.show_error_and_exit("Error in initializing Run tab", e)

        self.init_download_tab()

        self.notebook.pack(expand=1, fill="both")

    def init_run_tab(self):
        label_run = tk.Label(self.run_tab, text="List of Apps:")
        label_run.pack(padx=10, pady=10)

        app_path = os.path.join(os.getenv('USERPROFILE'), '.sevenworks', 'tools')
        app_list = [d for d in os.listdir(app_path) if os.path.isdir(os.path.join(app_path, d))]

        self.app_listbox = tk.Listbox(self.run_tab, selectmode=tk.SINGLE)
        for app in app_list:
            self.app_listbox.insert(tk.END, app)
        self.app_listbox.pack(padx=10, pady=10, side=tk.LEFT)

        app_details_frame = tk.Frame(self.run_tab)
        app_details_frame.pack(padx=10, pady=10, side=tk.RIGHT)

        self.icon_label = tk.Label(app_details_frame)
        self.icon_label.grid(row=0, column=0, padx=10, pady=5)

        self.name_label = tk.Label(app_details_frame, text="Name:")
        self.name_label.grid(row=1, column=0, sticky=tk.W, padx=10, pady=5)

        self.author_label = tk.Label(app_details_frame, text="Author:")
        self.author_label.grid(row=2, column=0, sticky=tk.W, padx=10, pady=5)

        self.description_label = tk.Label(app_details_frame, text="Description:")
        self.description_label.grid(row=3, column=0, sticky=tk.W, padx=10, pady=5)

        run_button = tk.Button(app_details_frame, text="Run", command=self.run_selected_app)
        run_button.grid(row=4, column=0, padx=10, pady=10, sticky=tk.W)

        run_admin_button = tk.Button(app_details_frame, text="Run (Admin)", command=self.run_selected_app_admin)
        run_admin_button.grid(row=5, column=0, padx=10, pady=10, sticky=tk.W)

        delete_button = tk.Button(app_details_frame, text="Delete", command=self.delete_selected_app)
        delete_button.grid(row=4, column=0, padx=10, pady=10, sticky=tk.E)

        self.app_listbox.bind('<<ListboxSelect>>', self.update_app_details)

    def update_app_details(self, event):
        selected_index = self.app_listbox.curselection()

        if not selected_index:
            return

        selected_app = self.app_listbox.get(selected_index)
        app_path = os.path.join(os.getenv('USERPROFILE'), '.sevenworks', 'tools', selected_app)
        icon_path = os.path.join(app_path, 'icon.png')

        if os.path.exists(icon_path):
            icon_image = Image.open(icon_path)
            icon_image = icon_image.resize((50, 50), Image.LANCZOS)
            self.icon_tk_image = ImageTk.PhotoImage(icon_image)
            self.icon_label.config(image=self.icon_tk_image)
            self.icon_label.image = self.icon_tk_image

            info_path = os.path.join(app_path, 'info.json')
            if os.path.exists(info_path):
                with open(info_path, 'r') as f:
                    app_info = json.load(f)

                self.name_label.config(text=f"Name: {selected_app}")
                self.author_label.config(text=f"Author: {app_info.get('author', 'Unknown')}")
                self.description_label.config(text=f"Description: {app_info.get('description', 'No description')}")
            else:
                print(f"Warning: info.json not found in {app_path}")
        else:
            print("Icon path does not exist:", icon_path)

    def run_selected_app(self):
        selected_app = self.app_listbox.get(self.app_listbox.curselection())
        app_path = os.path.join(os.getenv('USERPROFILE'), '.sevenworks', 'tools', selected_app)
        info_path = os.path.join(app_path, 'info.json')

        if os.path.exists(info_path):
            with open(info_path, 'r') as f:
                app_info = json.load(f)

            exec_path = app_info.get('exec')
            if exec_path:
                exec_path = os.path.join(app_path, exec_path)
                try:
                    os.system(f'"{exec_path}"')
                except Exception as e:
                    self.show_error_and_exit(f"Error running the selected app ({selected_app})", e)
            else:
                print(f"Warning: 'exec' not defined in info.json for {selected_app}")
        else:
            print(f"Warning: info.json not found in {app_path}")

    def run_selected_app_admin(self):
        selected_app = self.app_listbox.get(self.app_listbox.curselection())
        app_path = os.path.join(os.getenv('USERPROFILE'), '.sevenworks', 'tools', selected_app)
        info_path = os.path.join(app_path, 'info.json')

        if os.path.exists(info_path):
            with open(info_path, 'r') as f:
                app_info = json.load(f)

            exec_path = app_info.get('exec')
            if exec_path:
                exec_path = os.path.join(app_path, exec_path)
                try:
                    subprocess.run(["runas", "/user:Administrator", f'"{exec_path}"'])
                except Exception as e:
                    self.show_error_and_exit(f"Error running the selected app as admin ({selected_app})", e)
            else:
                print(f"Warning: 'exec' not defined in info.json for {selected_app}")
        else:
            print(f"Warning: info.json not found in {app_path}")

    def delete_selected_app(self):
        selected_app = self.app_listbox.get(self.app_listbox.curselection())
        app_path = os.path.join(os.getenv('USERPROFILE'), '.sevenworks', 'tools', selected_app)

        try:
            import shutil
            shutil.rmtree(app_path)
            self.refresh_app_listbox()
        except Exception as e:
            self.show_error_and_exit(f"Error deleting the selected app ({selected_app})", e)

    def refresh_app_listbox(self):
        self.app_listbox.delete(0, tk.END)
        app_path = os.path.join(os.getenv('USERPROFILE'), '.sevenworks', 'tools')
        app_list = [d for d in os.listdir(app_path) if os.path.isdir(os.path.join(app_path, d))]
        for app in app_list:
            self.app_listbox.insert(tk.END, app)

    def init_download_tab(self):
        label_download = tk.Label(self.download_tab, text="Coming Soon...")
        label_download.pack(padx=10, pady=10)

    def show_error_and_exit(self, message, error):
        messagebox.showerror("Error", f"{message}\n\nError details: {error}")
        self.root.destroy()

def main():
    root = tk.Tk()
    app = deadHack(root)
    root.mainloop()

if __name__ == "__main__":
    main()