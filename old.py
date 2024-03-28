import tkinter as tk
from tkinter import messagebox
from pynput.mouse import Button, Controller
from pynput import keyboard
import threading
import time

class AutoClickerApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("lion's autoclicker [2.1]")
        self.geometry("350x150")

        self.click_delay_label = tk.Label(self, text="Interval (s):")
        self.click_delay_label.grid(row=1, column=1, sticky="w", padx=(20, 0), pady=(30, 20))

        self.click_delay_var = tk.StringVar()
        self.click_delay_var.set(0)
        self.click_delay_var.trace("w", self.update_cps)
        self.click_delay_entry = tk.Entry(self, textvariable=self.click_delay_var, width=3)
        self.click_delay_entry.grid(row=1, column=2, sticky="w", padx=(0, 0), pady=(30, 20))

        self.togglesunken = False
        self.start_stop_button = tk.Button(self, text="Toggle", command=self.toggle_autoclicker, relief="raised")
        self.start_stop_button.grid(row=2, column=2, sticky="w", padx=(0, 0), pady=(0, 30))

        self.exit_button = tk.Button(self, text="Exit", command=self.quit_app)
        self.exit_button.grid(row=2, column=1, sticky="w", padx=(20, 0), pady=(0, 30))

        self.key_var = tk.StringVar()
        self.key_var.set("")
        self.key_entry = tk.Entry(self, textvariable=self.key_var, width = 1)
        self.key_entry.grid(row=2,column=3,sticky="w", padx=(80,0),pady=(0,30))
        self.key_entry.grid_remove()
        
        self.cps_var = tk.StringVar()
        self.cps_var.set('0 CPS')
        self.cps_display = tk.Label(self, textvariable=self.cps_var)
        self.cps_display.grid(row=1, column=3, padx=(100, 0), pady=(0, 0))

        self.mb = "LMB"
        self.mb_var = tk.StringVar()
        self.mb_var.set(self.mb)
        self.lmb_setter = tk.Button(self, textvariable = self.mb_var, command=self.configure_mb)

        self.lmb_setter.grid(row=2, column=3, sticky="n",padx=(100,0),pady=(0,10))

        self.mouse_controller = Controller()
        self.keyboard_controller = keyboard.Controller()
        self.running = False
        self.hotkey = {keyboard.Key.alt_l, keyboard.Key.cmd_l}
        self.current_keys = set()

        self.listener = keyboard.Listener(on_press=self.on_key_press, on_release=self.on_key_release)
        self.listener.start()

    def toggle_autoclicker(self):
        if not self.running:
            try:
                delay = float(self.click_delay_var.get())
                if delay < 0:
                    raise ValueError
                self.running = True
                self.start_autoclicker()
            except ValueError:
                messagebox.showerror("Invalid Interval", "Please enter a click interval greater than zero.")
        else:
            self.running = False
            self.start_stop_button.configure(relief='raised')


    def start_autoclicker(self):

        if self.key_var.get() == "" and self.mb == "KEY":
            self.running = False
            messagebox.showerror("Invalid Key","Please enter a alphanumeric character or symbol found on your device's keyboard.")
            return
        else:
            self.start_stop_button.configure(relief='sunken')

        def autoclick():
            while self.running:
                delay = float(self.click_delay_var.get())
                if self.mb == "LMB":
                    self.mouse_controller.click(Button.left, 1)
                elif self.mb == "RMB":
                    self.mouse_controller.click(Button.right, 1)
                elif self.mb == "KEY":
                    self.keyboard_controller.press(self.key_var.get())
                    self.keyboard_controller.release(self.key_var.get())
                time.sleep(delay)

        self.autoclicker_thread = threading.Thread(target=autoclick)
        self.autoclicker_thread.start()
    def on_key_press(self, key):
        if any([key in self.hotkey, key in self.current_keys]):
            self.current_keys.add(key)
            if self.hotkey == self.current_keys:
                self.toggle_autoclicker()

    def on_key_release(self, key):
            try:
                self.current_keys.remove(key)
            except KeyError:
                pass

    def update_cps(self, *args):
            try:
                delay = float(self.click_delay_var.get())
                if delay <= 0:
                    raise ValueError
                cps = round(1 / delay, 2)
                if int(cps) == cps:
                    cps = int(cps)
            except ValueError:
                cps = 0
            self.cps_var.set(f"{cps} CPS")

    def configure_mb(self):
        if self.mb == "LMB":
            self.mb = "RMB"
            self.mb_var.set(self.mb)
        elif self.mb == "RMB":
            self.mb = "KEY"
            self.mb_var.set(self.mb)
            self.key_entry.grid()
        elif self.mb == "KEY":
            self.mb = "LMB"
            self.mb_var.set(self.mb)
            self.key_entry.grid_remove()

    def quit_app(self):
            self.running = False
            self.listener.stop()
            self.destroy()

app = AutoClickerApp()
app.mainloop()
