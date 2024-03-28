import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
from pynput.mouse import Button, Controller
from pynput import mouse
from pynput import keyboard
import threading
import time
import pickle
m = mouse.Controller()
k = keyboard.Controller()
class Recorder:
    def __init__(self):
        self.events = []
        self.start = 0
        self.recording = False
        self.mlistener = mouse.Listener(
            on_move=self.on_move,
            on_click=self.on_click,
            on_scroll=self.on_scroll
        )
        self.klistener = keyboard.Listener(
            on_press=self.on_press,
            on_release=self.on_release
        )
    def on_move(self,x, y):
        self.events.append(
                {
                    "time":round(time.time()-self.start,2),
                    "event":"move",
                    "info":[x,y]
                }
            )

    def on_click(self,x, y, button, pressed):
        self.events.append(
                {
                    "time":round(time.time()-self.start,2),
                    "event":"mpressed" if pressed else "mreleased",
                    "info":button
                }
            )

    def on_scroll(self,x, y, dx, dy):
        self.events.append(
                {
                    "time":round(time.time()-self.start,2),
                    "event":"scroll",
                    "info":[dx,dy]
                }
            )
    def on_press(self,key):
        self.events.append(
                {
                    "time":round(time.time()-self.start,2),
                    "event":"kpressed",
                    "info":key
                }
            )

    def on_release(self,key):

        self.events.append(
                {
                    "time":round(time.time()-self.start,2),
                    "event":"kreleased",
                    "info":key
                }
            )
        if key == keyboard.Key.esc:
            self.Stop()
    def Start(self):
        self.start = time.time()
        self.recording = True
        self.mlistener.start()
        time.sleep(0.1)
        self.klistener.start()
    def Stop(self):
        self.mlistener.stop()
        self.klistener.stop()
        self.recording = False
    def Save(self):
        with filedialog.asksaveasfile(mode="wb",defaultextension="txt") as f:
            pickle.dump(self.events, f, pickle.HIGHEST_PROTOCOL)
class Player:
    def __init__(self):
        with filedialog.askopenfile(mode="rb") as f:
            self.events = pickle.load(f)
    def Play(self):
        start = time.time()
        for i in self.events:
            if i["event"] != "move":
                print(i,start-time.time())
            while i["time"] > time.time()-start:
                pass
            if i["event"] == "move":
                m.position = (i["info"][0],i["info"][1])
            elif i["event"] == "mpressed":
                m.press(button=i["info"])
            elif i["event"] == "mreleased":
                m.release(button=i["info"])
            elif i["event"] == "scroll":
                m.scroll(i["info"][0],i["info"][1])
            elif i["event"] == "kpressed":
                k.press(i["info"])
            elif i["event"] == "kreleased":
                k.release(i["info"])

class settings(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)

        self.geometry("200x150")
        self.title("lion's autoclicker (Settings)")

        from os import path
        with open(file=path.expanduser("~")+"/conf.la3",mode="r") as conf:

            self.confs2 = conf.read().split("\n")
        
        self.confs = {
            "hotkey":["<COMMAND_L>","<ALT_L>"],
            "presetcps":[10],
            "runtime":[0],
            "startdelay":[5]
        }
        for i in self.confs2:
            pass
            
            


    def close(self):
        self.conf.close()
class tasks(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)

        self.geometry("300x150")
        self.title("lion's autoclicker (Tasks)")

        self.play_ico = tk.PhotoImage(file="run-button.png",width=30,height=30)
        self.stop_ico = tk.PhotoImage(file="stop-button.png",width=30,height=30)

        self.recorder = Recorder()
        self.player = None
        self.playing = False
        self.continuous = True

        self.recording = tk.BooleanVar(self,self.recorder.recording)

        self.recordbutton = tk.Button(self,text="Record",command=self.record)
        self.recordbutton.grid(row=0,column=0)

        self.togglebutton = tk.Button(self,command=self.toggle,image=self.play_ico)
        self.togglebutton.grid(row=0,column=1)
    def load(self):
        self.player = Player()
    
    def toggle(self):
        if not self.playing:
            self.togglebutton.image = self.stop_ico
            def run():
                if self.continuous == True:
                    while self.playing:
                        self.player.Play()
                else:
                    self.player.Play()
            self.pt = threading.Thread(target=run)
            self.pt.start()
        else:
            self.togglebutton.image = self.play_ico
            self.playing = False

    def record(self):
        if not self.recorder.recording:
            self.recorder.Start()

    def save(self):
        if self.recorder.recording:
            self.recorder.Stop()
        self.recorder.Save()
class main(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("lion's autoclicker [3.1]")
        self.geometry("350x150")
        
        self.menu = tk.Menu(self)
        self.configure(menu=self.menu)

        self.filemenu = tk.Menu(self.menu)
        self.optionsmenu = tk.Menu(self.menu)
        self.menu.add_cascade(label="File",menu=self.filemenu)
        self.filemenu.add_command(label="Load Script",command=self.load_script)
        self.menu.add_separator()
        self.menu.add_cascade(label="Options",menu=self.optionsmenu)
        self.optionsmenu.add_command(label="Open Settings",command=self.open_settings)

        self.click_delay_label = tk.Label(self, text="Interval (s):")
        self.click_delay_label.grid(row=1, column=1, sticky="w", padx=(20, 0), pady=(30, 20))

        self.click_delay_var = tk.StringVar()
        self.click_delay_var.set(0)
        self.click_delay_var.trace_add("write", self.update_cps)
        self.click_delay_entry = tk.Entry(self, textvariable=self.click_delay_var, width=3)
        self.click_delay_entry.grid(row=1, column=2, sticky="w", padx=(0, 0), pady=(30, 20))

        self.togglesunken = False
        self.start_stop_button = tk.Button(self, text="Toggle", command=self.toggle_autoclicker, relief="raised")
        self.start_stop_button.grid(row=2, column=2, sticky="w", padx=(0, 0), pady=(0, 30))

        self.exit_button = tk.Button(self, text="Tasks", command=self.open_tasks)
        self.exit_button.grid(row=2, column=1, sticky="w", padx=(20, 0), pady=(0, 30))

        self.key_var = tk.StringVar()
        self.key_var.set("")
        self.key_entry = tk.Entry(self, textvariable=self.key_var, width = 1)
        self.key_entry.grid(row=2,column=3,sticky="w", padx=(70,0),pady=(0,30))
        self.key_entry.grid_remove()
        
        self.cps_var = tk.StringVar()
        self.cps_var.set('0 CPS')
        self.cps_display = tk.Label(self, textvariable=self.cps_var)
        self.cps_display.grid(row=1, column=3, padx=(100, 0), pady=(0, 0))

        self.mb = "LMB"
        self.mb_var = tk.StringVar()
        self.mb_var.set(self.mb)
        #self.lmb_setter = tk.Button(self, textvariable = self.mb_var, command=self.configure_mb)
        self.lmb_setter = tk.OptionMenu(self, self.mb_var, "LMB","RMB","Key", command=self.configure_mb)

        self.lmb_setter.grid(row=2, column=3,sticky="w",padx=(90,0),pady=(0,25))

        self.mouse_controller = Controller()
        self.keyboard_controller = keyboard.Controller()
        self.running = False
        self.hotkey = {keyboard.Key.alt_l, keyboard.Key.cmd_l}
        self.current_keys = set()

        #self.settingsbutton = tk.Button(self,text="...",command=self.open_settings)
        #self.settingsbutton.grid(row=3,column=1)

        self.listener = keyboard.Listener(on_press=self.on_key_press, on_release=self.on_key_release)
        self.listener.start()

    def toggle_autoclicker(self):
        if not self.running:
            try:
                delay = float(self.click_delay_var.get())
                if delay < 0:
                    raise ValueError
                self.running = True
                self.start_stop_button.configure(fg="green")
                time.sleep(1)
                self.start_autoclicker()
            except ValueError:
                messagebox.showerror("Invalid Interval", "Please enter a click interval greater than zero.")
        else:
            self.running = False
            self.start_stop_button.configure(fg="black")

    def start_autoclicker(self):

        if self.key_var.get() == "" and self.mb_var.get() == "KEY":
            self.running = False
            messagebox.showerror("Invalid Key","Please enter a alphanumeric character or symbol found on your device's keyboard.")
            return
        else:
            self.start_stop_button.configure(relief='sunken')

        def autoclick():
            while self.running:
                delay = float(self.click_delay_var.get())
                if self.mb_var.get() == "LMB":
                    self.mouse_controller.click(Button.left, 1)
                elif self.mb_var.get() == "RMB":
                    self.mouse_controller.click(Button.right, 1)
                elif self.mb_var.get() == "Key":
                    self.keyboard_controller.press(self.key_var.get())
                    self.keyboard_controller.release(self.key_var.get())
                elif self.mb_var.get() == "...":
                    self.run_script()
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

    def configure_mb(self,mb):
        if mb == "LMB":
            self.key_entry.grid_remove()
        elif mb == "RMB":
            self.key_entry.grid_remove()
        elif mb == "Key":
            self.key_entry.grid()
        elif mb == "...":
            self.key_entry.grid_remove()

    def quit_app(self):
            self.running = False
            self.listener.stop()
            self.destroy()

    def load_script(self):

        self.file = filedialog.askopenfile("r",defaultextension=(".txt"))
        if self.file.readline().lower() not in ["!! lion's utilities executable\n", "!! la3 script\n", "!! lion's autoclicker executable\n", "!! la3 executable\n","!! la3 custom script\n"]:
            self.file.close()
            messagebox.showerror("Incompatible File","Script does not start with a valid flag.")
            return
        self.lines = self.file.read().split("\n")
        self.file.close()

        self.loadedscript = []
        for line in self.lines[self.lines.index("?? start")+1:self.lines.index("?? end")]:
            if line == '': continue
            elif line.startswith('#'): continue
            else: pass
            splitline = line.split("|")
            self.loadedscript.append({"command" : splitline[0].strip(), "args" : [i.strip() for i in splitline[1].split(",")]})
        
        self.mb_var.set("...")
        self.key_entry.grid_remove()
        
    def run_script(self):

        for step in self.loadedscript:
            if step["command"].lower() == "wait":
                time.sleep(float(step["args"][0]))
            elif step["command"].lower() == "click":
                assert step["args"][0].lower() in ["lmb","rmb"]
                if step["args"][0].lower() == "lmb": tmp = Button.left
                elif step["args"][0].lower() == "rmb": tmp = Button.right
                else: tmp = Button.left
                self.mouse_controller.click(tmp,int(step["args"][1]))
            elif step["command"].lower() == "hit key":
                self.keyboard_controller.press(step["args"][0])
                self.keyboard_controller.release(step["args"][0])
            elif step["command"].lower() == "press key":
                self.keyboard_controller.press(step["args"][0])
            elif step["command"].lower() == "release key":
                self.keyboard_controller.release(step["args"][0])
            elif step["command"].lower() == "type":
                self.keyboard_controller.type(step["args"][0])
            elif step["command"].lower() == "move by":
                self.mouse_controller.move(dx=int(step["args"][0]),dy=int(step["args"][1]))
            elif step["command"].lower() == "move to":
                self.mouse_controller.position = (int(step["args"][0]),int(step["args"][1]))
            elif step["command"].lower() == "scroll":
                if step["args"][0].lower() == "up": tmp = 1
                elif step["args"][0].lower() == "down": tmp = -1
                else: tmp = 1
                self.mouse_controller.scroll(dy=tmp*int(step["args"][1]))

    def parse_key(self):
        pass

    def open_settings(self):

        settings(self).grab_set()

    def open_tasks(self):

        tasks(self).grab_set()
app = main()
app.mainloop()
