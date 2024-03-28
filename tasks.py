from pynput import mouse, keyboard
import time
import pickle
m = mouse.Controller()
k = keyboard.Controller()
class Recorder:
    def __init__(self):
        self.events = []
        self.start = 0
        self.toggle = True
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
        self.mlistener.start()
        time.sleep(0.1)
        self.klistener.start()
    def Stop(self):
        self.mlistener.stop()
        self.klistener.stop()
        with open("task.pickle","wb") as f:
            pickle.dump(self.events, f, pickle.HIGHEST_PROTOCOL)
class Player:
    def __init__(self,fp):
        with open(fp, 'rb') as f:
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
