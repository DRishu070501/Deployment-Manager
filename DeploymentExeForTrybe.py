import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import requests
from threading import Thread
import winsound

SERVER_URL = "https://kps.trybe-dev.mobioffice.io/deploymentApi"


def update_status(label_var, status):
    """Updates the status label."""
    label_var.set(status)


def play_success_sound():
    """Plays a success sound."""
    winsound.MessageBeep(winsound.MB_OK)


def play_error_sound():
    """Plays an error sound."""
    winsound.MessageBeep(winsound.MB_ICONHAND)


def shake_window(root):
    """Shakes the window for a visual effect."""
    for _ in range(5):  # Shake back and forth 5 times
        x, y = root.winfo_x(), root.winfo_y()
        root.geometry(f"+{x + 10}+{y}")
        root.update()
        root.geometry(f"+{x - 10}+{y}")
        root.update()


def call_backend(endpoint_suffix):
    status_backend.set("Backend: In Progress...")

    def task():
        try:
            response = requests.get(f"{SERVER_URL}/deployBackend{endpoint_suffix}")
            if response.status_code == 200:
                update_status(status_backend, "Backend: Success")
                play_success_sound()
                messagebox.showinfo("Success", f"Backend deployed successfully ({endpoint_suffix})!")
            else:
                update_status(status_backend, "Backend: Failed")
                play_error_sound()
                shake_window(root)
                messagebox.showerror("Error", f"Backend Error: {response.json().get('message', 'Unknown error')}")
        except Exception as e:
            update_status(status_backend, "Backend: Failed")
            play_error_sound()
            shake_window(root)
            messagebox.showerror("Error", f"Error connecting to backend: {e}")

    Thread(target=task).start()


def call_ui(endpoint_suffix):
    status_ui.set("UI: In Progress...")

    def task():
        try:
            response = requests.get(f"{SERVER_URL}/deployUi{endpoint_suffix}")
            if response.status_code == 200:
                update_status(status_ui, "UI: Success")
                play_success_sound()
                messagebox.showinfo("Success", f"UI deployed successfully ({endpoint_suffix})!")
            else:
                update_status(status_ui, "UI: Failed")
                play_error_sound()
                shake_window(root)
                messagebox.showerror("Error", f"UI Error: {response.json().get('message', 'Unknown error')}")
        except Exception as e:
            update_status(status_ui, "UI: Failed")
            play_error_sound()
            shake_window(root)
            messagebox.showerror("Error", f"Error connecting to UI: {e}")

    Thread(target=task).start()


root = tk.Tk()
root.title("Deployment Manager")
root.geometry("400x400")
root.configure(bg="#f5f5f5")


title_font = ("Arial", 18, "bold")
label_font = ("Arial", 12)
button_font = ("Arial", 12, "bold")


button_color = "#4CAF50"  
button_text_color = "#FFFFFF"  
status_color = "#007BFF"  


title_frame = tk.Frame(root, bg="#f5f5f5", pady=10)
title_frame.pack(fill="x")

tk.Label(title_frame, text="Deployment Manager", font=title_font, bg="#f5f5f5").pack()


status_backend = tk.StringVar(value="Backend: Idle")
status_ui = tk.StringVar(value="UI: Idle")

status_frame = tk.Frame(root, bg="#f5f5f5", pady=10)
status_frame.pack(fill="x", padx=20)

tk.Label(status_frame, textvariable=status_backend, font=label_font, fg=status_color, bg="#f5f5f5").pack(pady=5)
tk.Label(status_frame, textvariable=status_ui, font=label_font, fg=status_color, bg="#f5f5f5").pack(pady=5)


dropdown_label = tk.Label(root, text="Select Project:", font=label_font, bg="#f5f5f5")
dropdown_label.pack(pady=10)


style = ttk.Style()


style.configure("TCombobox",
                font=("Arial", 12),
                padding=5,
                relief="flat",
                background="#f5f5f5",
                foreground="#333333")


style.map("TCombobox",
          background=[("readonly", "#e7e7e7")])


selected_type = tk.StringVar(value="KP")
type_dropdown = ttk.Combobox(root, textvariable=selected_type, values=["KP", "KG"], state="readonly", width=10)
type_dropdown.pack(pady=5)


button_frame = tk.Frame(root, bg="#f5f5f5", pady=20)
button_frame.pack(fill="x", padx=20)


def on_deploy_backend():
    endpoint_suffix = "Kg" if selected_type.get() == "KG" else ""
    call_backend(endpoint_suffix)


def on_deploy_ui():
    endpoint_suffix = "Kg" if selected_type.get() == "KG" else ""
    print(endpoint_suffix)
    call_ui(endpoint_suffix)


tk.Button(button_frame, text="Deploy Backend", command=on_deploy_backend, font=button_font,
          bg=button_color, fg=button_text_color, relief="raised", width=20).pack(pady=5)

tk.Button(button_frame, text="Deploy UI", command=on_deploy_ui, font=button_font,
          bg=button_color, fg=button_text_color, relief="raised", width=20).pack(pady=5)

tk.Button(button_frame, text="Exit", command=root.quit, font=button_font,
          bg="#FF0000", fg=button_text_color, relief="raised", width=20).pack(pady=5)

root.mainloop()
