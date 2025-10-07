import tkinter as tk
from tkinter import filedialog, messagebox
from tkinterdnd2 import TkinterDnD, DND_FILES
from PIL import Image, ImageTk
import subprocess
import os

SUPPORTED_EXTENSIONS = (
    ".mp3", ".wav", ".ogg", ".flac", ".m4a", ".aac", ".wma", ".aiff", ".alac", ".opus"
)

# 🔥 Splash screen with animated GIF and "Loading..." banner
def show_splash(callback):
    splash = tk.Toplevel()
    splash.overrideredirect(True)
    splash.geometry("400x350+500+300")
    splash.configure(bg="#2c2f33")

    gif_path = "musicNotes.gif"
    gif = Image.open(gif_path)
    frames = []
    try:
        while True:
            frames.append(ImageTk.PhotoImage(gif.copy()))
            gif.seek(len(frames))
    except EOFError:
        pass

    gif_label = tk.Label(splash, bg="#2c2f33")
    gif_label.place(relx=0.5, rely=0.55, anchor="center") # 👈 shifted lower

    loading_label = tk.Label(
        splash,
        text="🎶 Loading Sound & Music Converter...",
        font=("Segoe UI", 12, "bold"),
        bg="#2c2f33",
        fg="#00ffcc"
    )
    loading_label.place(relx=0.5, rely=0.15, anchor="center") # 👈 moved higher

    job_id = None

    def animate(index=0):
        nonlocal job_id
        gif_label.config(image=frames[index])
        job_id = splash.after(100, animate, (index + 1) % len(frames))

    animate()

    def close_splash():
        if job_id:
            splash.after_cancel(job_id)
        splash.destroy()
        callback()

    splash.after(2000, close_splash)

# 🎯 Main GUI setup
def launch_gui():
    root = TkinterDnD.Tk()
    root.title("Sound & Music Converter")
    root.geometry("400x500+500+300")
    root.configure(bg="#2c2f33")
    root.resizable(True, True)

    tk.Label(
        root,
        text="🎵 Sound & Music Converter 🎵",
        font=("Segoe UI", 16, "bold"),
        bg="#2c2f33",
        fg="#00ffcc"
    ).pack(pady=(10, 0), fill="x")

    tk.Label(
        root,
        text="Convert your audio with style 🎧",
        font=("Segoe UI", 10),
        bg="#2c2f33",
        fg="#bbbbbb"
    ).pack(pady=(0, 10))

    format_var = tk.StringVar(value="mp3")
    tk.Label(root, text="Select output format:", bg="#2c2f33", fg="#bbbbbb").pack()
    format_menu = tk.OptionMenu(root, format_var, "mp3", "wav", "ogg", "flac")
    format_menu.configure(bg="#23272a", fg="white", highlightthickness=0)
    format_menu.pack(pady=(0, 10))

    save_folder_var = tk.StringVar(value="")

    def choose_folder():
        folder = filedialog.askdirectory()
        if folder:
            save_folder_var.set(folder)
            folder_label.config(text=f"Save to: {folder}")

    tk.Button(root, text="Choose Save Folder", command=choose_folder, bg="#00ffcc", fg="#2c2f33").pack(pady=(5, 0))
    folder_label = tk.Label(root, text="No folder selected", bg="#2c2f33", fg="#bbbbbb")
    folder_label.pack()

    drop_label = tk.Label(
        root,
        text="Drag and drop audio file here",
        bg="#23272a",
        fg="white",
        relief="ridge",
        anchor="center",
        justify="center"
    )
    drop_label.pack(expand=True, fill="both", padx=20, pady=20)
    drop_label.drop_target_register(DND_FILES)
    drop_label.bind("<Enter>", lambda e: drop_label.configure(bg="#3a3f44"))
    drop_label.bind("<Leave>", lambda e: drop_label.configure(bg="#23272a"))

    def convert_audio(file_path):
        output_format = format_var.get()
        save_folder = save_folder_var.get()

        if not save_folder:
            messagebox.showwarning("Missing Folder", "Please choose a save folder.")
            return

        input_ext = os.path.splitext(file_path)[1].lower()
        if input_ext not in SUPPORTED_EXTENSIONS:
            messagebox.showwarning("Unsupported File", f"'{input_ext}' is not a supported audio format.")
            return

        if input_ext == f".{output_format}":
            messagebox.showinfo("No Conversion Needed", f"File is already in .{output_format} format.")
            return

        base_name = os.path.splitext(os.path.basename(file_path))[0]
        output_path = os.path.join(save_folder, f"{base_name}.{output_format}")

        if os.path.exists(output_path):
            response = messagebox.askyesno(
                "File Exists",
                f"'{output_path}' already exists.\nDo you want to choose a different name?"
            )
            if response:
                new_name = filedialog.asksaveasfilename(
                    defaultextension=f".{output_format}",
                    initialdir=save_folder,
                    initialfile=f"{base_name}_new.{output_format}",
                    title="Choose a new filename"
                )
                if not new_name:
                    return
                output_path = new_name
            else:
                return

        command = ["ffmpeg", "-y", "-i", file_path, output_path]

        try:
            subprocess.run(command, check=True)
            messagebox.showinfo("Success", f"File converted:\n{output_path}")
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Conversion Failed", str(e))

    def handle_drop(event):
        file_path = event.data.strip("{}")
        convert_audio(file_path)

    drop_label.dnd_bind("<<Drop>>", handle_drop)

    root.mainloop()

# 🚀 Start app with splash first, then GUI
if __name__ == "__main__":
    temp_root = tk.Tk()
    temp_root.withdraw()

    def start_gui():
        temp_root.destroy()
        launch_gui()

    show_splash(start_gui)
    temp_root.mainloop()