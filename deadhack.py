import os, json, subprocess, requests, zipfile
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk

class deadHack:
    apps_data = []

    def __init__(self, root):
        self.root = root
        self.root.title("deadHack")
        self.root.geometry("450x380")
        self.root.resizable(False, False)
        self.root.iconbitmap("icon.ico")

        self.notebook = ttk.Notebook(root)
        self.run_tab = ttk.Frame(self.notebook)
        self.download_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.run_tab, text='Run')
        self.notebook.add(self.download_tab, text='Download')

        try:
            self.init_run_tab()
        except Exception as e:
            self.throw_error("Error in initializing Run tab", e)

        try:
            self.init_download_tab()
        except Exception as e:
            self.throw_error("Error in initializing Download tab", e)

        self.notebook.pack(expand=1, fill="both")

    def init_run_tab(self):
        app_path = os.path.join(os.getenv('USERPROFILE'), '.sevenworks', 'tools')
        app_list = [d for d in os.listdir(app_path) if os.path.isdir(os.path.join(app_path, d))]

        self.app_listbox = tk.Listbox(self.run_tab, selectmode=tk.SINGLE)
        for app in app_list:
            self.app_listbox.insert(tk.END, app)
        self.app_listbox.pack(padx=10, pady=10, side=tk.LEFT, fill=tk.Y)

        app_details_frame = tk.Frame(self.run_tab)
        app_details_frame.pack(padx=10, pady=10, side=tk.RIGHT, anchor=tk.N)  # Updated here
        self.icon_label = tk.Label(app_details_frame)
        self.icon_label.grid(row=0, column=0, padx=10, pady=5)
        self.name_label = tk.Label(app_details_frame, text="Name:")
        self.name_label.grid(row=1, column=0, sticky=tk.W, padx=10, pady=5)
        self.author_label = tk.Label(app_details_frame, text="Author:")
        self.author_label.grid(row=2, column=0, sticky=tk.W, padx=10, pady=5)
        self.description_text_run = tk.Text(app_details_frame, wrap=tk.WORD, height=5, width=30)
        self.description_text_run.grid(row=3, column=0, sticky=tk.W, padx=10, pady=5)

        run_button = tk.Button(app_details_frame, text="Run", command=self.run_tool)
        run_button.grid(row=4, column=0, padx=10, pady=10, sticky=tk.W)
        run_admin_button = tk.Button(app_details_frame, text="Run (Admin)", command=self.run_tool_admin)
        run_admin_button.grid(row=4, column=0, padx=10, pady=10, sticky=tk.E)
        delete_button = tk.Button(app_details_frame, text="Delete", command=self.delete_tool)
        delete_button.grid(row=5, column=0, padx=10, pady=10, sticky=tk.W)
        self.app_listbox.bind('<<ListboxSelect>>', self.update_details)


    def update_details(self, event):
        selected_index = self.app_listbox.curselection()

        if not selected_index: return

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
                self.description_text_run.delete("1.0", tk.END)
                self.description_text_run.insert(tk.END, app_info.get('description', 'No description'))
            else:
                print(f"Warning: info.json not found in {app_path}")
        else:
            print("Icon path does not exist:", icon_path)

    def run_tool(self):
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
                    self.throw_error(f"Error running the selected app ({selected_app})", e)
            else:
                print(f"Warning: 'exec' not defined in info.json for {selected_app}")
        else:
            print(f"Warning: info.json not found in {app_path}")

    def run_tool_admin(self):
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
                    self.throw_error(f"Error running the selected app as admin ({selected_app})", e)
            else:
                print(f"Warning: 'exec' not defined in info.json for {selected_app}")
        else:
            print(f"Warning: info.json not found in {app_path}")

    def delete_tool(self):
        selected_app = self.app_listbox.get(self.app_listbox.curselection())
        app_path = os.path.join(os.getenv('USERPROFILE'), '.sevenworks', 'tools', selected_app)

        try:
            import shutil
            shutil.rmtree(app_path)
            self.refresh_list()
        except Exception as e:
            self.throw_error(f"Error deleting the selected app ({selected_app})", e)

    def refresh_list(self):
        self.app_listbox.delete(0, tk.END)
        app_path = os.path.join(os.getenv('USERPROFILE'), '.sevenworks', 'tools')
        app_list = [d for d in os.listdir(app_path) if os.path.isdir(os.path.join(app_path, d))]
        for app in app_list:
            self.app_listbox.insert(tk.END, app)

    def init_download_tab(self):
        self.download_listbox = tk.Listbox(self.download_tab, selectmode=tk.SINGLE)
        self.download_listbox.pack(padx=10, pady=10, side=tk.LEFT, fill=tk.Y)
        app_details_frame = tk.Frame(self.download_tab)
        app_details_frame.pack(padx=10, pady=10, side=tk.RIGHT, fill=tk.Y)
        self.name_label_download = tk.Label(app_details_frame, text="Name:")
        self.name_label_download.grid(row=0, column=0, sticky=tk.W, padx=10, pady=5)
        self.description_text = tk.Text(app_details_frame, wrap=tk.WORD, height=5, width=30)
        self.description_text.grid(row=1, column=0, sticky=tk.W, padx=10, pady=5)
        download_button = tk.Button(app_details_frame, text="Download", command=self.download_tool)
        download_button.grid(row=2, column=0, padx=10, pady=10, sticky=tk.W)
        scrollbar = tk.Scrollbar(app_details_frame, command=self.description_text.yview)
        scrollbar.grid(row=1, column=1, sticky='nsew')
        self.description_text.config(yscrollcommand=scrollbar.set)
        self.download_listbox.bind('<<ListboxSelect>>', self.update_tools_download)
        self.fetch_tools()

    def fetch_tools(self):
        try:
            response = requests.get("https://raw.githubusercontent.com/SevenworksDev/DeadHack/main/apps.json")
            deadHack.apps_data = response.json()
            for app in deadHack.apps_data:
                self.download_listbox.insert(tk.END, app["name"])
        except requests.exceptions.RequestException as e:
            self.throw_error("Error fetching downloadable apps", e)
        except json.JSONDecodeError as e:
            self.throw_error("Error decoding JSON data", e)

    def update_tools_download(self, event):
      selected_index = self.download_listbox.curselection()
      if not selected_index: return
      selected_app = self.download_listbox.get(selected_index)

      for app in deadHack.apps_data:
          if app["name"] == selected_app:
              self.name_label_download.config(text=f"Name: {selected_app}")
              self.description_text.delete("1.0", tk.END)
              self.description_text.insert(tk.END, app['description'])
              break

    def download_tool(self):
        selected_index = self.download_listbox.curselection()
        if not selected_index: return
        selected_app = self.download_listbox.get(selected_index)

        for app in deadHack.apps_data:
            if app["name"] == selected_app:
                download_url = app["download"]

                try:
                    response = requests.get(download_url, stream=True)
                    response.raise_for_status()
                    zip_path = os.path.join(os.getenv('USERPROFILE'), '.sevenworks', 'tools', 'temp.zip')
                    with open(zip_path, 'wb') as zip_file:
                        for chunk in response.iter_content(chunk_size=128):
                            zip_file.write(chunk)
                    target_folder = os.path.join(os.getenv('USERPROFILE'), '.sevenworks', 'tools')
                    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                        zip_ref.extractall(target_folder)
                    os.remove(zip_path)
                    self.refresh_list()
                except requests.exceptions.RequestException as e:
                    self.throw_error(f"Error downloading {selected_app}", e)
                except zipfile.BadZipFile as e:
                    self.throw_error(f"Error extracting {selected_app}: {e}", e)
                break

    def throw_error(self, message, error):
        messagebox.showerror("Error", f"{message}\n\nError details: {error}")
        self.root.destroy()

def main():
    os.makedirs(os.path.join(os.getenv('USERPROFILE'), '.sevenworks', 'tools'), exist_ok=True)
    root = tk.Tk()
    app = deadHack(root)
    root.mainloop()

if __name__ == "__main__":
    main()