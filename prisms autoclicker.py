# Version 4.1
# Previously "lion's autoclicker"

# Hello there.

__version__ = "4.1"

import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
from pynput.mouse import Button, Controller
from pynput import mouse
from pynput import keyboard
import threading
from time import time, sleep
import pickle
from os import nice
nice(20)
global m
m = mouse.Controller()
global k
k = keyboard.Controller()
global app
class SyncedRecorder:
    def __init__(self):
        self.events = []
        self.down = []
        self.recording = False
        self.stop = False
        self.start = 0
        self.rkt = threading.Thread(target=self.recordkeys,name="syncedkeyboardrecorder",daemon=True)
        self.rkt.start()
        sleep(0.1)
        self.rmt = threading.Thread(target=self.recordmouse,name="syncedmouserecorder",daemon=True)
        self.rmt.start()
        sleep(0.1)
    def recordkeys(self):
        with keyboard.Events() as events:
            for event in events:
                if type(event) == keyboard.Events.Press:
                    try:
                        self.on_press(event.key)
                    except KeyError as e:
                        pass
                elif type(event) == keyboard.Events.Release:
                    try:
                        self.on_release(event.key)
                    except KeyError as e:
                        pass
    def recordmouse(self):
        with mouse.Events() as events:
            for event in events:
                if self.recording:
                    if type(event) == mouse.Events.Click:
                        self.on_click(event.x,event.y,event.button,event.pressed)
                    elif type(event) == mouse.Events.Move:
                        self.on_move(event.x,event.y)
                    elif type(event) == mouse.Events.Scroll:
                        self.on_scroll(event.x,event.y,event.dx,event.dy)
                if self.stop:
                    break
            return
    def on_move(self,x, y):
        try:
            if self.recording:
                self.events.append(
                        {
                            "time":round(time()-self.start,2),
                            "event":"move",
                            "info":[x,y]
                        }
                    )
        except Exception: print("!on_move")
    def on_click(self,x, y, button, pressed):
        try:
            if self.recording:
                self.events.append(
                        {
                            "time":round(time()-self.start,2),
                            "event":"mpressed" if pressed else "mreleased",
                            "info":button
                        }
                    )
        except Exception: print("!on_click")
    def on_scroll(self,x, y, dx, dy):
        try:
            if self.recording:
                self.events.append(
                        {
                            "time":round(time()-self.start,2),
                            "event":"scroll",
                            "info":[dx,dy]
                        }
                )
        except Exception: print("!on_scroll")
    def on_press(self,key):
        global app
        try:
            self.down.append(key)
        except:
            pass
        try:
            if keyboard.Key.alt in self.down and keyboard.KeyCode.from_char("®") in self.down:
                app.tasky.record()
            elif keyboard.Key.alt in self.down and keyboard.KeyCode.from_char("π") in self.down:
                app.tasky.toggle()
            elif keyboard.Key.alt in self.down and keyboard.KeyCode.from_char("†") in self.down:
                app.toggle()
            elif self.recording:
                #if not ((keyboard.Key.alt in self.down) and key in [keyboard.KeyCode.from_char("†"),keyboard.KeyCode.from_char("®")]):
                    self.events.append(
                            {
                                "time":round(time()-self.start,2),
                                "event":"kpressed",
                                "info":key
                            }
                        )
        except Exception:
            pass
    def on_release(self,key):
        try:
            self.down.remove(key)
        except Exception as e:
            pass
        try:
            if self.recording:
                #if not ((keyboard.Key.alt in self.down) and key in [keyboard.KeyCode.from_char("†"),keyboard.KeyCode.from_char("®")]):
                if key != keyboard.KeyCode.from_char("®"):
                    self.events.append(
                            {
                                "time":round(time()-self.start,2),
                                "event":"kreleased",
                                "info":key
                            }
                        )
        except Exception:
            pass
    def Start(self):
        self.start = time()
        self.recording = True
    def Stop(self):
        self.recording = False
    def Save(self):
        with filedialog.asksaveasfile(mode="wb",defaultextension="txt") as f:
            pickle.dump(self.events, f, pickle.HIGHEST_PROTOCOL)
    def Yield(self):
        return self.events

class WIPEventBasedRecorder:
    def __init__(self):
        raise NotImplemented
        self._events = []
        self.isrecording = False
        self.starttime = int
    def _record(self):

        for event in keyboard.Events():
            if not self.isrecording:
                break
            else:
                self.events.append({
                    "time":self.time-self.starttime,
                    "event":event
                })
        
        return
    def _format(self):
        pass
class Recorder:
    def __init__(self):
        self.events = []
        self.down = []
        self.start = 0
        self.recording = False
        self.mlistener = mouse.Listener(
            on_move=self.on_move,
            on_click=self.on_click,
            on_scroll=self.on_scroll,
            name="mlistener"
        )
        self.klistener = keyboard.Listener(
            on_press=self.on_press,
            on_release=self.on_release,
            name="klistener"
        )
    def on_move(self,x, y):
        if self.recording:
            self.events.append(
                    {
                        "time":time()-self.start,
                        "event":"move",
                        "info":[x,y]
                    }
                )
    def on_click(self,x, y, button, pressed):
        try:
            if self.recording:
                self.events.append(
                        {
                            "time":time()-self.start,
                            "event":"mpressed" if pressed else "mreleased",
                            "info":button
                        }
                    )
        except: pass
    def on_scroll(self,x, y, dx, dy):
        try:
            if self.recording:
                self.events.append(
                        {
                            "time":time()-self.start,
                            "event":"scroll",
                            "info":[dx,dy]
                        }
                )
        except: pass
    def on_press(self,key):
        try:
            self.down.append(key)

            if keyboard.Key.alt in self.down:
                global app
                if keyboard.KeyCode.from_char("®") in self.down:
                    app.tasky.record()
                    return
                elif keyboard.KeyCode.from_char("π") in self.down:
                    app.tasky.toggle()
                    return
                elif keyboard.KeyCode.from_char("†") in self.down:
                    app.toggle()
                    return

            if self.recording:
                self.events.append(
                        {
                            "time":time()-self.start,
                            "event":"kpressed",
                            "info":key
                        }
                )
        except:
            pass
 
    def on_release(self,key):
        try:
            self.down.remove(key)
            if self.recording and key != keyboard.KeyCode.from_char("®"):
                self.events.append(
                        {
                            "time":time()-self.start,
                            "event":"kreleased",
                            "info":key
                        }
                    )
        except:
            pass
    def Start(self):
        self.start = time()
        self.recording = True
    def Stop(self):
        self.recording = False
    def Save(self):
        with filedialog.asksaveasfile(mode="wb",defaultextension="txt") as f:
            pickle.dump(self.events, f, pickle.HIGHEST_PROTOCOL)
    def Yield(self):
        return self.events
class Player:
    def __init__(self):
        self.events = []
        self.compiled = []
        self.playing = False
        self.iscompiled = False
    def load_from_file(self):
        with filedialog.askopenfile(mode="rb") as f:
            self.events = pickle.load(f)
    def load(self,events):
        self.events=events
    def Play(self):
        for i in self.compiled:
            if not self.playing:
                return
            i[0](i[1])

taskrecorder = Recorder()

taskrecorder.klistener.start()
taskrecorder.klistener.wait()
taskrecorder.mlistener.start()
taskrecorder.mlistener.wait()

class settings(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)

        self.geometry("200x150")
        self.title("prism's autoclicker (Settings)")
        messagebox.showerror(message="(womp womp) Settings are still in development.")
        self.destroy()
        
class tasks(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)

        self.geometry("200x50")
        self.title("prism's tasks")
        self.play_ico = tk.PhotoImage(data="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",width=40,height=40)
        self.stop_ico = tk.PhotoImage(data="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",width=40,height=40)
        self.record_ico = tk.PhotoImage(data="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",width=40,height=40)
        self.stop_record_ico = tk.PhotoImage(data="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",width=40,height=40)
        self.save_ico = tk.PhotoImage(data="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",width=40,height=40)
        self.load_ico = tk.PhotoImage(data="iVBORw0KGgoAAAANSUhEUgAAACgAAAAoCAYAAAH7+Yj7AAAAAXNSR0IArs4c6QAAAIRlWElmTU0AKgAAAAgABQESAAMAAAABAAEAAAEaAAUAAAABAAAASgEbAAUAAAABAAAAUgEoAAMAAAABAAIAAIdpAAQAAAABAAAAWgAAAAAAAAPoAAAAAQAAA+gAAAABAAOgAQADAAAAAQABAACgAgAEAAAAAQAAACigAwAEAAAAAQAAACgAAAAA4iS1LAAAAAlwSFlzAACZygAAmcoB45GkIgAAAVlpVFh0WE1MOmNvbS5hZG9iZS54bXAAAAAAADx4OnhtcG1ldGEgeG1sbnM6eD0iYWRvYmU6bnM6bWV0YS8iIHg6eG1wdGs9IlhNUCBDb3JlIDYuMC4wIj4KICAgPHJkZjpSREYgeG1sbnM6cmRmPSJodHRwOi8vd3d3LnczLm9yZy8xOTk5LzAyLzIyLXJkZi1zeW50YXgtbnMjIj4KICAgICAgPHJkZjpEZXNjcmlwdGlvbiByZGY6YWJvdXQ9IiIKICAgICAgICAgICAgeG1sbnM6dGlmZj0iaHR0cDovL25zLmFkb2JlLmNvbS90aWZmLzEuMC8iPgogICAgICAgICA8dGlmZjpPcmllbnRhdGlvbj4xPC90aWZmOk9yaWVudGF0aW9uPgogICAgICA8L3JkZjpEZXNjcmlwdGlvbj4KICAgPC9yZGY6UkRGPgo8L3g6eG1wbWV0YT4KGV7hBwAABH1JREFUWAntWMuOE0cUPe1ugw0OY3seTnYhL8iOBQKxySaR/AdZZJ3PYpVFPmIUsslDkWYCLBKRSEhJhGQYZoKHgQF7+pV7qlzd7e4uT0HMaCKlJLse99apW3Ufdau9b364l7ZabRRLwIFW+1xxDAF7QRDgyi+eImxdOkJjjmXWUZxRFGH7siF78L7/+c/UdE0dcJEkTdHwNCYJavpnvzdxABkMmtj+4MWChb69HM3gQlWrhcrCzzjmKrUOR7ip4U9jfHVxKivmQvZX19WEjJG9l50ehru5tBRwq38IT3ZQYPRwMN4R9gKj3wTeP28QNSGKQmzf6KvBuj/vOzm1AkbGQynNeKPhQ6mMMiwqjUYjP8gkSYQ33215YraZa7f+wpfJY3x+9b2MZ6Xbg+9rlowRnS5u9j7Czd2MD5sYwZxjrbHkrHnLmTFfen8vn25aWnuq5239upO+0vEYEFutNNNqtYS++NBtAMXxhi8a1DDiKcdosTjR1iZWfjgzLgLv7T5SvV5vFZ7Yja3UCVEB9EXs4R/ncaG7jum+h6nNmsRHNi/cR6+/Nre7CqCSRlwCcQj6orVYSM6GYwUuEeolpNdI0LIIoX1K6HWlAsg4efeTQR1vaSxCHG3IuvPAFUDOikIdC0sITt2AxshfdXvVEY1oJDJ004fG+fHOgzRJ4mx1kg1rNujQ4M4nk5cIzrbbSOIc0GGuhYWipNr16izeMss6rHQjXrZ0O6wBTNXFqaO4VSAroWQ2KaIoxtPx3zIhRX/9bWXgttl1RzUHmMi5Pt1/guGDFSCMcct7iBgSbSyhbXXN0bDR3ZDgEOHTfQnuVF6pNNIEyfgx7g582ZFJDDTTnITZPIk0BLSVtgAeWug1SrHB5OOLDP+1AHPoauv0A9YrhX4kP+tZKT+rUb+cQD3gWFKSJKqzGHVozwmoUohqIPZu/7Yn4YvJki60fl9SRpdSDMSM3Cp8lSeSUGQs04/r/we0zPtEB31qjXo1tdmc0aZN54Zf3gqSxXq8U851OuK6sS2oGOQTqymiLznV4eEzBLzweEexrouXJyZVYSEaGs+X1rx0oymss5TmqRfQKQJQ9XxfFkvIi4kR5w2X+VVLi/HVfabZxM6jEYZ3XgD9AQZeip2D5/j63SmufPwhJtNQvM3mkSXAQjcWuy/nqQVy1lwoYMbFRnwkSe0RYonh3VaALx7KW3o0muUTJjTMzah25CZHcAbYG2Hzeh8bg3cQSp68yDndBVxZA3oDHEk6wc8WPLOO/Fi7iEceyWkxDs4ilI160nYp7gJSFGZfKgPTXzmeuaxQ4EnlS0RYmF8gWZun3ov/F9CqO0eCuw3SG2al0DRDx9Y6Ys5mvgKAu4D8RCc/jc0vMSJTnftqSbR7U2zDI7XyXIXDZd3eqAsF5KdRBtSVbh+bF58I6H0u+e/LW1CYxF4UA7nQQgHJwGgfBD668oVnmYW53hJvEnmZv8Z1towNnfowE9CGtV2nJ5GcOB7qTBaaF99OtAf15Ue5piPGm2QTwfi2mUwm+AdO2mUsfHXrrwAAAABJRU5ErkJggg==",width=40,height=40)
        self.player = Player()
        self.synced = True
        self.playing = False
        self.continuous = True
        self.events=None
        self.recorded=False

        self.togglebutton = tk.Button(self,command=self.toggle,image=self.play_ico)
        self.togglebutton.grid(row=0,column=0)

        self.recordbutton = tk.Button(self,command=self.record,image=self.record_ico)
        self.recordbutton.grid(row=0,column=1)

        self.savebutton = tk.Button(self,command=self.save,image=self.save_ico)
        self.savebutton.grid(row=0,column=2)

        self.loadbutton = tk.Button(self,command=self.load,image=self.load_ico)
        self.loadbutton.grid(row=0,column=3)

        self.withdraw()

    def load(self):
        try:
            self.player.load_from_file()
            self.events = self.player.events
            self.player.iscompiled = False
            self.compile()
            
        except TypeError:
            pass
    def toggle(self):
        if not self.playing:
        
            self.togglebutton.config(image = self.stop_ico)
            def run(): 
                self.playing = True
                self.player.playing = True
                if self.continuous == True:
                    while self.playing:
                        try:
                            self.player.Play()
                        except Exception: pass
                else:
                    try:
                        self.player.Play()
                    except Exception: pass
            self.pt = threading.Thread(target=run,daemon=True)
            self.pt.start()

        else:
            self.togglebutton.config(image = self.play_ico)
            self.playing = False
            self.player.playing = False
    def _compile(self):

        res = []

        start = time()
        print("[Prism's Autoclicker] Compiling events...")
        index = -1
        for i in self.events:
            index += 1
            res.append([sleep,i["time"]-(self.events[index-1]["time"] if index > 0 else 0)])
            if i["event"] == "move":
                def temp(r):
                    global m
                    m.position = r
                res.append([temp, (i["info"][0],i["info"][1])])
                continue
            elif i["event"] == "mpressed":
                res.append([m.press,i["info"]])
                continue
            elif i["event"] == "mreleased":
                res.append([m.release,i["info"]])
                continue
            elif i["event"] == "scroll":
                def temp(r):
                    global m
                    m.scroll(r[0],r[1])
                res.append([temp, [i["info"][0], i["info"][1]]])
                continue
            elif i["event"] == "kpressed":
                res.append([k.press, i["info"]])
            elif i["event"] == "kreleased":
                res.append([k.release, i["info"]])
                continue
        self.player.compiled = res
        self.player.iscompiled = True
        print("[Prism's Autoclicker] Event compiling completed!")
    def compile(self):
        tmp = threading.Thread(target=self._compile, daemon=True)
        tmp.start()
    def record(self):
        if self.playing:
            return

        if not taskrecorder.recording:
            self.recordbutton.config(image=self.stop_record_ico)
            taskrecorder.events=[]
            taskrecorder.Start()
        elif taskrecorder.recording:
            taskrecorder.recording=False
            self.events=taskrecorder.Yield()
            self.recordbutton.config(image=self.record_ico)
            self.player.load(self.events)
            self.player.iscompiled = False
            self.compile()
    def save(self):
        tmp = False
        if taskrecorder.recording:
            taskrecorder.Stop()
            tmp = True
        taskrecorder.Save()
        if tmp:
            self.events=taskrecorder.Yield()
            self.player.events = self.events
            self.player.iscompiled = False
            self.compile()
class main(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("prism's autoclicker")
        self.geometry("350x150")
        
        self.menu = tk.Menu(self)
        self.configure(menu=self.menu)

        self.filemenu = tk.Menu(self.menu)
        self.optionsmenu = tk.Menu(self.menu)
        self.menu.add_cascade(label="File",menu=self.filemenu)
        self.filemenu.add_command(label="Load Script",command=self.load_script)

        self.click_delay_label = tk.Label(self, text="Interval (s):")
        self.click_delay_label.grid(row=1, column=1, sticky="w", padx=(20, 0), pady=(30, 20))

        self.click_delay_var = tk.StringVar()
        self.click_delay_var.set(0)
        self.click_delay_var.trace_add("write", self.update_cps)
        self.click_delay_entry = tk.Entry(self, textvariable=self.click_delay_var, width=3)
        self.click_delay_entry.grid(row=1, column=2, sticky="w", padx=(0, 0), pady=(30, 20))

        self.togglesunken = False
        self.toggle_button = tk.Button(self, text="Toggle", command=self.toggle, relief="raised")
        self.toggle_button.grid(row=2, column=2, sticky="w", padx=(0, 0), pady=(0, 30))

        self.tasks_button = tk.Button(self, text="Tasks", command=self.open_tasks)
        self.tasks_button.grid(row=2, column=1, sticky="w", padx=(20, 0), pady=(0, 30))

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
        self.lmb_setter = tk.OptionMenu(self, self.mb_var, "LMB","RMB","Key", command=self.configure_mb)

        self.lmb_setter.grid(row=2, column=3,sticky="w",padx=(90,0),pady=(0,25))
        self.running = False
        self.tasky = tasks(self)
        #self.settingsbutton = tk.Button(self,text="...",command=self.open_settings)
        #self.settingsbutton.grid(row=3,column=1)

    def toggle(self):
        if not self.running:
            try:
                delay = float(self.click_delay_var.get())
                if delay < 0:
                    raise ValueError
                self.running = True
                self.toggle_button.configure(fg="green")
                self.start_autoclicker()
            except ValueError:
                messagebox.showerror("Invalid Interval", "Please enter a click interval greater than zero.")
        else:
            self.running = False
            self.toggle_button.configure(fg="black")

    def start_autoclicker(self):

        if self.key_var.get() == "" and self.mb_var.get() == "KEY":
            self.running = False
            messagebox.showerror("Invalid Key","Please enter a alphanumeric character or symbol found on your device's keyboard.")
            return

        def autoclick():
            if self.mb_var.get() == "LMB":
                tmp = [m.click,Button.left]
            elif self.mb_var.get() == "RMB":
                tmp = [m.click,Button.right]
            elif self.mb_var.get() == "Key":
                tmp = [k.touch,self.key_var.get()]
            elif self.mb_var.get() == "...":
                tmp = [self.run_script,None]
            delay = float(self.click_delay_var.get())
            while self.running:
                tmp[0](tmp[1])
                sleep(delay)

        self.autoclicker_thread = threading.Thread(target=autoclick, daemon=True)
        self.autoclicker_thread.start()

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
            self.tasky.destroy()
            self.destroy()

    def load_script(self):

        self.file = filedialog.askopenfile("r",defaultextension=(".txt"))
        if self.file.readline().lower() not in ["!! prism's utilities executable\n", "!! la3 script\n", "!! prism's autoclicker executable\n", "!! la3 executable\n","!! la3 custom script\n"]:
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
        
    def run_script(self, arg=None):

        for step in self.loadedscript:
            if step["command"].lower() == "wait":
                sleep(float(step["args"][0]))
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
        self.tasky.wm_deiconify()

app = main()

app.mainloop()