import tkinter as tk
from tkinter import ttk
from tkinter.font import Font
from tkinter import filedialog

import os

from send_messages import send_whatsapp_message, send_whatsapp_photo
from settings import save_settings_to_file, load_settings_from_file


class MessageConstructor(tk.Frame):
    def __init__(self, master, title, with_photo=True, max_blocks=6, send_action=None, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.configure(bg="#f7f7f7")
        self.master = master
        self.with_photo = with_photo
        self.max_blocks = max_blocks
        self.block_count = 0
        self.block_type = tk.StringVar(value="Name")
        self.is_expanded = False
        self.title = title
        self.send_action = send_action
        self.blocks = []
        self.init_ui()

        if self.with_photo:
            self.add_block("Photo (default)", is_photo=True)

    def init_ui(self):
        # Custom font
        custom_font = Font(family="Helvetica", size=12, weight="bold")

        # Create and configure a style with the custom font
        style = ttk.Style()
        style.configure("Custom.TButton", font=custom_font)

        # Apply the custom style to the ttk.Button
        toggle_button = ttk.Button(self, text=self.title, command=self.toggle_view, style="Custom.TButton")
        toggle_button.pack(fill=tk.X, padx=5, pady=5)

        self.container = tk.Frame(self, bg="#f7f7f7")

        side_panel = tk.Frame(self.container, bg="#f7f7f7")
        side_panel.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

        block_types = ["Name", "Text" if not self.with_photo else "Caption", "Custom text"]
        for block in block_types:
            radio_button = tk.Radiobutton(side_panel, text=block, variable=self.block_type, value=block,
                                          bg="#f7f7f7", selectcolor="#f0f0f0")
            radio_button.pack(anchor=tk.W, pady=2)

        self.constructor_area = tk.Frame(self.container, borderwidth=1, relief=tk.GROOVE, bg="white")
        self.constructor_area.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)

        self.add_button = tk.Button(self.constructor_area, text="+", command=self.add_block_prompt)
        self.add_button.pack(side=tk.LEFT)

        self.send_button = tk.Button(self.container, text="Send", command=self.on_send)
        self.send_button.pack(side=tk.BOTTOM, fill=tk.X)

    def toggle_view(self):
        self.master.toggle_other_sections(self)

    def add_block_prompt(self):
        if self.block_count < self.max_blocks:
            self.add_block(self.block_type.get())
        if self.block_count >= self.max_blocks:
            self.add_button.pack_forget()

    def add_block(self, block_type, is_photo=False):
        block_frame = tk.Frame(self.constructor_area, borderwidth=1, relief=tk.SOLID)
        block_frame.pack(side=tk.LEFT, padx=5, pady=5)

        block_data = {"type": block_type, "widget": block_frame}
        if block_type == "Custom text":
            # Use Text widget for multi-line input
            text_entry = tk.Text(block_frame, height=3, width=20)
            text_entry.pack(side=tk.LEFT)
            block_data["entry"] = text_entry
        else:
            label = tk.Label(block_frame, text=block_type)
            label.pack(side=tk.LEFT)

        if not is_photo:
            delete_button = tk.Button(block_frame, text="x", command=lambda: self.delete_block(block_frame, block_data))
            delete_button.pack(side=tk.LEFT)

        self.blocks.append(block_data)
        self.block_count += 1
        self.add_button.pack_forget()
        if self.block_count < self.max_blocks:
            self.add_button.pack(side=tk.LEFT)

    def delete_block(self, block_frame, block_data):
        block_frame.destroy()
        self.blocks.remove(block_data)
        self.block_count -= 1
        if self.block_count < self.max_blocks:
            self.add_button.pack(side=tk.LEFT)

    def on_send(self):
        if self.send_action:
            self.send_action()


class MainApplication(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Message Constructor")
        self.configure(bg="#f0f0f0")  # Light grey background for the main window

        self.minsize(800, 500)

        self.settings = load_settings_from_file()

        settings_button = tk.Button(self, text="Settings", command=self.open_settings, bg="#0078D7", fg="white", bd=0)
        settings_button.pack(pady=10, padx=10, fill=tk.X)

        self.photo_frame = MessageConstructor(self, "Message with Photo", with_photo=True,
                                              send_action=self.send_photo)
        self.photo_frame.pack(pady=10, padx=10, fill=tk.X)

        self.no_photo_frame = MessageConstructor(self, "Message without Photo", with_photo=False, max_blocks=5,
                                                 send_action=self.send_text)
        self.no_photo_frame.pack(pady=10, padx=10, fill=tk.X)
        self.setup_ui()

    def setup_ui(self):
        # Custom style for Progressbar
        style = ttk.Style()
        style.theme_use('clam')  # Using a specific theme
        style.configure("TProgressbar", background="#0078D7", troughcolor="#f0f0f0", bordercolor="#f0f0f0",
                        lightcolor="#f0f0f0", darkcolor="#f0f0f0")

        progress_label = tk.Label(self, text="Progress:", bg="#f0f0f0", font=("Arial", 12, "bold"))
        progress_label.pack(padx=10, pady=(10, 0))

        self.progress_bar = ttk.Progressbar(self, orient="horizontal", mode="determinate", length=300)
        self.progress_bar.pack(fill=tk.X, padx=10, pady=5)

        logs_label = tk.Label(self, text="Logs:", bg="#f0f0f0", font=("Arial", 12, "bold"))
        logs_label.pack(padx=10, pady=(10, 0))

        self.log_text = tk.Text(self, height=10, state="disabled", font=("Courier", 10), bg="#ffffff")
        self.log_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

    def open_settings(self):
        self.settings_window = tk.Toplevel(self)
        self.center_window_settings(self.settings_window)
        self.settings_window.title("Settings")
        self.settings_window.configure(bg="#f7f7f7")

        # Simplified entry fields for settings
        self.ultramsg_token_entry = self.create_setting_entry("ULTRAMSG_TOKEN", os.environ.get('ULTRAMSG_TOKEN', ''),
                                                              False, False)
        self.ultramsg_instance_id_entry = self.create_setting_entry("ULTRAMSG_INSTANCE_ID",
                                                                    os.environ.get('ULTRAMSG_INSTANCE_ID', ''), False,
                                                                    False)
        self.spreadsheet_id_entry = self.create_setting_entry("SPREADSHEET_ID", os.environ.get('SPREADSHEET_ID', ''),
                                                              False, False)
        self.service_account_file_entry = self.create_setting_entry("SERVICE_ACCOUNT_FILE",
                                                                    os.environ.get('SERVICE_ACCOUNT_FILE', ''), True,
                                                                    False)
        self.message_delay_entry = self.create_setting_entry("MESSAGE_DELAY (in seconds)",
                                                             os.environ.get('MESSAGE_DELAY', '1'), False, True)
        self.sheet_name_entry = self.create_setting_entry("SHEET_NUMBER (just number)",
                                                          os.environ.get('SHEET_NUMBER', '1'), False, True)

        # Save button
        save_button = tk.Button(self.settings_window, text="Save", command=self.save_settings, bg="#0078D7", fg="white",
                                bd=0)
        save_button.pack(pady=10, padx=10)

        self.settings_window.transient(self)
        self.settings_window.grab_set()

    def center_window_settings(self, window):
        window.update_idletasks()  # Update the state of the window
        width = window.winfo_width()
        height = window.winfo_height()

        # Get the position of the main application window
        x_main = self.winfo_x()
        y_main = self.winfo_y()

        # Get the size of the main application window
        width_main = self.winfo_width()
        height_main = self.winfo_height()

        # Calculate the position to center the window over the main application window
        x = x_main + (width_main // 2) - (width // 2)
        y = y_main + (height_main // 2) - (height // 2)

        window.geometry(f'{600}x{300}+{x}+{y}')

    def create_setting_entry(self, label_text, default_value, file_picker=False, only_digits=False):
        frame = tk.Frame(self.settings_window, bg="#f7f7f7")
        frame.pack(padx=10, pady=5, fill=tk.X)

        label_font = ("Arial", 10, "bold")
        label = tk.Label(frame, text=label_text, bg="#f7f7f7", font=label_font, fg="#333333")
        label.pack(side=tk.LEFT, padx=5)

        if only_digits:
            vcmd = (self.register(lambda P: P.isdigit() or P == ""), '%P')
            entry = tk.Entry(frame, bd=2, relief=tk.GROOVE, validate='key', validatecommand=vcmd)
        else:
            entry = tk.Entry(frame, bd=2, relief=tk.GROOVE)
        entry.insert(0, default_value)
        entry.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=5)

        # Add clipboard bindings
        entry.bind("<Control-c>", lambda e: self.copy_to_clipboard(entry))
        entry.bind("<Control-v>", lambda e: self.custom_paste(entry, e))
        entry.bind("<Control-x>", lambda e: self.cut_to_clipboard(entry))

        if file_picker:
            button = tk.Button(frame, text="Browse", command=lambda: self.browse_file(entry), bg="#0078D7", fg="white",
                               bd=0)
            button.pack(side=tk.RIGHT, padx=5)

        return entry

    def copy_to_clipboard(self, entry):
        self.clipboard_clear()
        if entry.selection_get():
            self.clipboard_append(entry.selection_get())

    def cut_to_clipboard(self, entry, event):
        self.copy_to_clipboard(entry)
        entry.delete("sel.first", "sel.last")

    def custom_paste(self, entry, event):
        try:
            text = self.clipboard_get()
            entry.insert(tk.INSERT, text)
        except tk.TclError:
            pass  # Handle case where there's nothing to paste
        return "break"  # Prevent further processing of the event

    def browse_file(self, entry):
        filename = filedialog.askopenfilename(title="Select file", filetypes=[("JSON files", "*.json")])
        if filename:
            entry.delete(0, tk.END)
            entry.insert(0, filename)

    def save_settings(self):
        # Retrieve values from entry fields
        ultramsg_token = self.ultramsg_token_entry.get()
        ultramsg_instance_id = self.ultramsg_instance_id_entry.get()
        spreadsheet_id = self.spreadsheet_id_entry.get()
        service_account_file = self.service_account_file_entry.get()
        sheet_number = self.sheet_name_entry.get()
        message_delay = self.message_delay_entry.get()

        # Update environment variables or application settings
        os.environ['ULTRAMSG_TOKEN'] = ultramsg_token
        os.environ['ULTRAMSG_INSTANCE_ID'] = ultramsg_instance_id
        os.environ['SPREADSHEET_ID'] = spreadsheet_id
        os.environ['SERVICE_ACCOUNT_FILE'] = service_account_file
        os.environ['MESSAGE_DELAY'] = message_delay
        os.environ['SHEET_NUMBER'] = sheet_number

        settings = {
            'ULTRAMSG_TOKEN': ultramsg_token,
            'ULTRAMSG_INSTANCE_ID': ultramsg_instance_id,
            'SPREADSHEET_ID': spreadsheet_id,
            'SERVICE_ACCOUNT_FILE': service_account_file,
            'MESSAGE_DELAY': message_delay,
            'SHEET_NUMBER': sheet_number
        }

        save_settings_to_file(settings)

        # Optionally, save these settings to a configuration file or other persistent storage

        # Close the settings window
        self.settings_window.destroy()

    def update_progress(self, current, total):
        # Calculate the percentage completion
        progress = (current / total) * 100
        self.progress_bar["value"] = progress
        self.update_idletasks()  # Update the UI

    def write_log(self, message):
        self.log_text.configure(state="normal")
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.configure(state="disabled")
        self.log_text.yview(tk.END)

    def clear_logs(self):
        self.log_text.configure(state="normal")
        self.log_text.delete(1.0, tk.END)
        self.log_text.configure(state="disabled")

    def toggle_other_sections(self, current_section):
        if current_section.is_expanded:
            current_section.container.pack_forget()
            current_section.is_expanded = False
        else:
            for section in [self.photo_frame, self.no_photo_frame]:
                if section.is_expanded:
                    section.container.pack_forget()
                    section.is_expanded = False
            current_section.container.pack(fill=tk.BOTH, expand=True)
            current_section.is_expanded = True

    def send_photo(self):
        self.clear_logs()
        message_content = []
        for block in self.photo_frame.blocks:
            if block["type"] == "Custom text":
                # Retrieve text from the Text widget
                text = block["entry"].get("1.0", "end-1c")
                # Replace occurrences of '\n' with actual newline characters
                processed_text = text.replace("\\n", "\n")
                message_content.append("{{" + processed_text + "}}")
            else:
                message_content.append("{{" + block["type"] + "}}")

        config = {
            "ultramsg_token": os.environ['ULTRAMSG_TOKEN'],
            "ultramsg_instance_id": os.environ['ULTRAMSG_INSTANCE_ID'],
            "service_account_file": os.environ['SERVICE_ACCOUNT_FILE'],
            "spreadsheet_id": os.environ['SPREADSHEET_ID'],
            "message_delay": os.environ['MESSAGE_DELAY'],
            "sheet_number": os.environ['SHEET_NUMBER']
        }
        send_whatsapp_photo(format=" ".join(message_content),
                            update_progress_callback=self.update_progress,
                            write_log_callback=self.write_log,
                            completion_callback=self.show_completion_popup,
                            error_callback=self.show_error_popup,
                            config=config
                            )

    def send_text(self):
        self.clear_logs()
        message_content = []
        for block in self.no_photo_frame.blocks:
            if block["type"] == "Custom text":
                # Retrieve text from the Text widget
                text = block["entry"].get("1.0", "end-1c")
                # Replace occurrences of '\n' with actual newline characters
                processed_text = text.replace("\\n", "\n")
                message_content.append("{{" + text + "}}")
            else:
                message_content.append("{{" + block["type"] + "}}")
        config = {
            "ultramsg_token": os.environ['ULTRAMSG_TOKEN'],
            "ultramsg_instance_id": os.environ['ULTRAMSG_INSTANCE_ID'],
            "service_account_file": os.environ['SERVICE_ACCOUNT_FILE'],
            "spreadsheet_id": os.environ['SPREADSHEET_ID'],
            "message_delay": os.environ['MESSAGE_DELAY'],
            "sheet_number": os.environ['SHEET_NUMBER']
        }
        send_whatsapp_message(format=" ".join(message_content),
                              update_progress_callback=self.update_progress,
                              write_log_callback=self.write_log,
                              completion_callback=self.show_completion_popup,
                              error_callback=self.show_error_popup,
                              config=config
                              )

    def show_completion_popup(self, sent_count, not_sent_count):
        popup = self.create_centered_popup("Sending Completed")
        message = f"Messages Sent: {sent_count}\nMessages Not Sent: {not_sent_count}"
        self.add_popup_content(popup, message, "OK")

    def show_error_popup(self, message):
        popup = self.create_centered_popup("Error occurred")
        self.add_popup_content(popup, message, "OK")

    def create_centered_popup(self, title):
        popup = tk.Toplevel(self)
        popup.title(title)
        popup.configure(bg="#f7f7f7")
        popup.transient(self)  # Make the window a transient window of the main window
        popup.grab_set()
        return popup

    def add_popup_content(self, popup, message, button_text):
        custom_font = ("Arial", 12)
        label = tk.Label(popup, text=message, bg="#f7f7f7", font=custom_font)
        label.pack(pady=10, padx=10)
        ok_button = tk.Button(popup, text=button_text, command=popup.destroy, bg="#0078D7", fg="white", bd=0, padx=10,
                              pady=5)
        ok_button.pack(pady=(0, 10))
        popup.update_idletasks()  # Update the state of the popup
        self.center_window(popup)

    def center_window(self, window):
        window.update_idletasks()  # Update the state of the window
        width = window.winfo_width()
        height = window.winfo_height()
        x_main = self.winfo_x()
        y_main = self.winfo_y()
        width_main = self.winfo_width()
        height_main = self.winfo_height()
        x = x_main + (width_main // 2) - (width // 2)
        y = y_main + (height_main // 2) - (height // 2)
        window.geometry(f'{width}x{height}+{x}+{y}')


if __name__ == "__main__":
    app = MainApplication()
    app.mainloop()
