from kivy.clock import Clock
from kivy.core.text import LabelBase
from kivy.uix.screenmanager import ScreenManager, NoTransition, SlideTransition, FadeTransition
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.core.window import Window
import json
import requests

Window.size = (310, 580)



class Qtime(MDApp):
    def build(self):
        Window.bind(on_keyboard=self.on_key)
        Clock.schedule_once(self.check_logged)
        sm = ScreenManager()
        sm.add_widget(Builder.load_file("assets/kv/main.kv"))
        sm.add_widget(Builder.load_file("assets/kv/login.kv"))
        sm.add_widget(Builder.load_file("assets/kv/signup.kv"))
        sm.add_widget(Builder.load_file("assets/kv/home.kv"))
        sm.get_screen('home')
        return sm

    def on_key(self, window, key, *args):
        if key == 27:
            if self.root.current_screen.name == "main":
                return True
            elif self.root.current_screen.name == "login":
                self.root.transition = SlideTransition(direction="right")
                self.root.current = "main"
                return True
            elif self.root.current_screen.name == "signup":
                self.root.transition = SlideTransition(direction = "right")
                self.root.current = "main"
                return True
            elif self.root.current_screen.name == "home":
                self.root.current = "home"
                return True

    def get_data(self):
        f = open("data.json", "rb")
        f_data = f.read().decode()
        data = json.loads(f_data)
        f.close()
        return data

    def get_akun(self):
        x = open("wayo.json", "rb")
        x_akun = x.read().decode()
        akun = json.loads(x_akun)
        x.close()
        return akun

    def set_data(self, key, value):
        data = self.get_data()
        data[key] = value
        f = open("data.json", "wb")
        f.write(json.dumps(data).encode())

    def set_akun(self, key, value):
        akun = self.get_akun()
        akun[key] = value
        x = open("wayo.json", "wb")
        x.write(json.dumps(akun).encode())

    def check_logged(self, *args):
        data = self.get_data()
        hayo = self.get_akun()
        if data['logged'] == "True":
            self.root.transition = NoTransition()
            self.root.current = "home"
            self.wayolo()
        else:
            self.root.transition = SlideTransition()

    def doLogin(self, tem, pw, reslog):
        url = 'http://52.187.66.15:5000/login'
        params = {
            'username': tem,
            'password': pw
        }
        r = requests.Session()
        res = r.post(url, params = params)
        if res.ok:
            self.set_data("logged", "True")
            self.set_akun("username", tem)
            self.wayolo()
        else:
            reslog.text = str(res.json()['message'])

    def doSignup(self,name,email,username,pw,reslog):
        url = 'http://52.187.66.15:5000/register'
        params = {
            'name': name,
            'email': email,
            'username': username,
            'password': pw
        }
        r = requests.Session()
        res = r.post(url, params=params)
        if res.ok:
            reslog.text = "AKUN SUKSES DIBUAT"
        else:
            reslog.text = str(res.json()['message'])
            print(res.json()['message'])

    def doLogout(self):
        self.root.transition = FadeTransition()
        self.root.current = "main"
        self.set_data("logged", "False")
        self.set_akun("username", "")
        self.check_logged()

    def wayolo(self):
        hayo = self.get_akun()
        url = 'http://52.187.66.15:5000/search-user'
        params = {
            'username': hayo['username']
        }
        self.root.current = "home"
        self.root.get_screen('home').ids.userName.text = "username kamu : "+ " " + hayo['username']
        r = requests.Session()
        res = r.post(url, params=params)
        getres = res.json()[0]
        self.root.get_screen('home').ids.name.text = "nama kamu : " + " " + str(getres['name'])
        self.root.get_screen('home').ids.email.text = "email kamu : " + " " + str(getres['email'])


if __name__ == "__main__":
    LabelBase.register(name="MPoppins", fn_regular="assets/font/Poppins-Medium.ttf")
    LabelBase.register(name="BPoppins", fn_regular="assets/font/Poppins-SemiBold.ttf")
    Qtime().run()
