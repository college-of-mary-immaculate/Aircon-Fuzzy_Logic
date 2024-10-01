import tkinter as tk
from PIL import Image, ImageTk, ImageSequence
import os
import sys

class AirconApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Cafe Aircon Controller")
        self.root.geometry("1024x678")
        
        self.entered_temp = 0
        self.final_aircon_temp = 0
        self.final_aircon_humidity = ""

        self.image_label = tk.Label(self.root)
        self.image_label.pack(fill="both", expand=True)

        self.remote_button = tk.Button(self.root, text="Enter Temperature", command=self.open_remote_window,
                                       font=("Arial", 12), bg="#444444", fg="black", bd=5, relief="raised")
        self.remote_button.place(relx=0.5, rely=0.5, anchor="center")

        self.result_label = tk.Label(self.root, text="")
        self.result_label.pack()

        bg_image = Image.open("main.gif")
        self.bg_frames = [frame.copy() for frame in ImageSequence.Iterator(bg_image)]
        self.animate_background()

        ac_image = Image.open("cold.gif")
        self.ac_frames = [frame.copy() for frame in ImageSequence.Iterator(ac_image)]

        fan_image = Image.open("fan.gif")
        self.fan_frames = [frame.copy() for frame in ImageSequence.Iterator(fan_image)]

        self.aircon_window = None
        self.fan_window = None
        self.aircon_label = None
        self.timer_label = None
        self.temp_label = None
        self.current_temp_label = None
        self.humidity_label = None

    def animate_background(self, counter=0):
        bg_image = ImageTk.PhotoImage(self.bg_frames[counter])
        self.image_label.config(image=bg_image)
        self.image_label.image = bg_image
        self.root.after(100, self.animate_background, (counter + 1) % len(self.bg_frames))

    def open_remote_window(self):
        self.remote_window = tk.Toplevel(self.root)
        self.remote_window.title("Remote Control")
        self.remote_window.geometry("300x200")
        self.remote_window.configure(bg="black")

        temp_label = tk.Label(self.remote_window, text="Enter Temperature (°C):", fg="white", bg="black")
        temp_label.pack(pady=20)

        self.temp_entry = tk.Entry(self.remote_window)
        self.temp_entry.pack(pady=5)

        submit_button = tk.Button(self.remote_window, text="Submit", command=self.submit_temperature)
        submit_button.pack(pady=10)

    def submit_temperature(self):
        try:
            self.entered_temp = float(self.temp_entry.get())

            if 10 <= self.entered_temp <= 30:  
                condition = self.fuzzy_logic(self.entered_temp)
                humidity = self.calculate_humidity(self.entered_temp)

                self.result_label.config(text=f"Aircon Condition: {condition}, Humidity: {humidity}")
             
                if condition == "Hot":
                    self.play_aircon_gif()
                    self.start_countdown(10, self.entered_temp)
                    self.remote_window.after(10000, lambda: (self.remote_window.destroy(), self.show_fan_mode()))
                elif condition == "Cool":
                    self.play_aircon_gif()
                    self.start_countdown(10, self.entered_temp)
                    self.remote_window.after(10000, self.remote_window.destroy)
                elif condition == "Warm":
                    self.play_aircon_gif()
                    self.start_countdown(10, self.entered_temp)
                    self.remote_window.after(10000, self.remote_window.destroy)
            else:
                self.result_label.config(text="Please enter a temperature between 16 and 30 °C.")
        except ValueError:
            self.result_label.config(text="Please enter a valid number.")

    def fuzzy_logic(self, temp):
        temperature = self.membership_function(temp)
        if temperature["Cool"] > 0:
            return "Cool"
        elif temperature["Warm"] > 0:
            return "Warm"
        elif temperature["Hot"] > 0:
            return "Hot"
        return "Normal"

    def membership_function(self, temp):
        cool = self.cool_membership(temp)
        warm = self.warm_membership(temp)
        hot = self.hot_membership(temp)
        return {"Cool": cool, "Warm": warm, "Hot": hot}

    def cool_membership(self, temp):
        if temp <= 10:
            return 1
        elif 10 < temp < 16:
            return (temp - 10) / (16 - 10)
        elif 16 <= temp <= 18:
            return 1
        elif 18 < temp < 21:
            return (21 - temp) / (21 - 18)
        return 0

    def warm_membership(self, temp):
        if 18 < temp < 24:
            return (temp - 18) / (24 - 18)
        elif 24 <= temp <= 26:
            return 1
        elif 26 < temp < 30:
            return (30 - temp) / (30 - 26)
        return 0

    def hot_membership(self, temp):
        if temp < 26:
            return 0
        elif 26 <= temp < 30:
            return (temp - 26) / (30 - 26)
        return 1

    def calculate_humidity(self, temp):
        if temp >= 25:
            return "High"
        elif 18 <= temp < 25:
            return "Normal"
        else:
            return "Low"

    def start_countdown(self, seconds, current_temp):
        if self.aircon_window and self.aircon_window.winfo_exists():
            if seconds > 1:
                adjusted_temp = current_temp - (self.entered_temp - 18) * (10 - seconds) / 10
                self.current_temp_label.config(text=f"Current Temp: {adjusted_temp:.1f}°C")
                
                humidity = self.calculate_humidity(adjusted_temp)
                self.humidity_label.config(text=f"Humidity: {humidity}") 
                
                self.timer_label.config(text=f"Time Remaining: {seconds} sec")

                if seconds <= 3:
                    self.timer_label.config(text="Switching to Fan Mode soon...")

                self.aircon_window.after(1000, self.start_countdown, seconds - 1, current_temp)
            else:
                self.timer_label.config(text="Switching to Fan Mode...")
                self.final_aircon_temp = float(self.current_temp_label.cget("text").split(': ')[1][:-2])
                self.final_aircon_humidity = self.humidity_label.cget("text").split(': ')[1]

                self.aircon_window.destroy()
                self.show_fan_mode()

    def play_aircon_gif(self, counter=0):
        if self.aircon_window is None or not self.aircon_window.winfo_exists():
            self.aircon_window = tk.Toplevel(self.root)
            self.aircon_window.title("Aircon Cooling")
            self.aircon_window.geometry("1024x678")

            self.aircon_label = tk.Label(self.aircon_window)
            self.aircon_label.pack()

            self.timer_label = tk.Label(self.aircon_window, text="",
                                             font=("Fixedsys", 30), fg="black")
            self.timer_label.place(relx=0.5, rely=0.1, anchor="center")

            self.temp_label = tk.Label(self.aircon_window, text=f"Entered Temp: {self.entered_temp}°C",
                                             font=("Fixedsys", 20), fg="black")
            self.temp_label.place(relx=0.5, rely=0.2, anchor="center")

            self.current_temp_label = tk.Label(self.aircon_window,
                                                 font=("Fixedsys", 20), fg="black")
            self.current_temp_label.place(relx=0.5, rely=0.3, anchor="center")

            self.humidity_label = tk.Label(self.aircon_window,
                                             font=("Fixedsys", 20), fg="black")
            self.humidity_label.place(relx=0.5, rely=0.4, anchor="center")

        ac_image = ImageTk.PhotoImage(self.ac_frames[counter])
        self.aircon_label.config(image=ac_image)
        self.aircon_label.image = ac_image

        self.aircon_window.after(100, lambda: self.play_aircon_gif((counter + 1) % len(self.ac_frames)))

    def show_fan_mode(self):
        print("Displaying Fan Mode...")
        self.play_fan_mode(self.final_aircon_temp, self.final_aircon_humidity)

    def play_fan_mode(self, final_temp, final_humidity, counter=0):
        if self.fan_window is None or not self.fan_window.winfo_exists():
            self.fan_window = tk.Toplevel(self.root)
            self.fan_window.title("Fan Mode")
            self.fan_window.geometry("1024x678")

            self.fan_label = tk.Label(self.fan_window)
            self.fan_label.pack()

            self.temp_label_fan = tk.Label(self.fan_window, text=f"Entered Temp: {self.entered_temp:.1f}°C",
                                           font=("Fixedsys", 20), fg="black")
            self.temp_label_fan.place(relx=0.5, rely=0.2, anchor="center")

            self.final_temp_label_fan = tk.Label(self.fan_window, text=f"Final Temp: {final_temp:.1f}°C",
                                                 font=("Fixedsys", 20), fg="black")
            self.final_temp_label_fan.place(relx=0.5, rely=0.3, anchor="center")

            self.final_humidity_label_fan = tk.Label(self.fan_window, text=f"Humidity: {final_humidity}",
                                                     font=("Fixedsys", 20), fg="black")
            self.final_humidity_label_fan.place(relx=0.5, rely=0.4, anchor="center")

        fan_image = ImageTk.PhotoImage(self.fan_frames[counter])
        self.fan_label.config(image=fan_image)
        self.fan_label.image = fan_image
        self.fan_window.after(100, lambda: self.play_fan_mode(final_temp, final_humidity, (counter + 1) % len(self.fan_frames)))


if __name__ == "__main__":
    root = tk.Tk()
    app = AirconApp(root)
    root.mainloop()
