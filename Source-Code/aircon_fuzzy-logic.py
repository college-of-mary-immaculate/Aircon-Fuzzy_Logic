import tkinter as tk
from PIL import Image, ImageTk, ImageSequence
import os
import sys

root = None
remote_window = None
temp_entry = None
aircon_window = None
fan_window = None
aircon_label = None
timer_label = None
temp_label = None
current_temp_label = None
humidity_label = None  
entered_temp = 0  
final_aircon_temp = 0  
final_aircon_humidity = ""  

def triangular_membership(x, a, b, c):
    if x <= a or x >= c:
        return 1
    elif a < x < b:
        return (x - a) / (b - a)  
    elif b <= x < c:
        return (c - x) / (c - b)  
    return 0

def cool_membership(temp):
    if temp <= 10:
        return 1
    elif 10 < temp < 16:
        return (temp - 10) / (16 - 10)  
    elif 16 <= temp <= 18:
        return 1  
    elif 18 < temp < 21:
        return (21 - temp) / (21 - 18)  
    return 0

def warm_membership(temp):
    if 18 < temp < 24:
        return (temp - 18) / (24 - 18)  
    elif 24 <= temp <= 26:
        return 1  
    elif 26 < temp < 30:
        return (30 - temp) / (30 - 26) 
    return 0

def hot_membership(temp):
    if temp < 26:
        return 0  
    elif 26 <= temp < 30:
        return (temp - 26) / (30 - 26)  
    return 1  

def membership_function(temp):
     
    cool = cool_membership(temp)
    warm = warm_membership(temp)
    hot = hot_membership(temp)
    return {"Cool": cool, "Warm": warm, "Hot": hot}

def fuzzy_logic(temp):
   
    temperature = membership_function(temp)
   
    if temperature["Cool"] > 0:
        return "Cool"
    elif temperature["Warm"] > 0:
        return "Warm"
    elif temperature["Hot"] > 0:
        return "Hot"
    return "Normal"

def calculate_humidity(temp):
    if temp >= 25:
        return "High"
    elif 18 <= temp < 25:
        return "Normal"
    else:
        return "Low"

def submit_temperature():
    global entered_temp
    try:
        entered_temp = float(temp_entry.get())

        if 10 <= entered_temp <= 30:  
            condition = fuzzy_logic(entered_temp)
            humidity = calculate_humidity(entered_temp)

            result_label.config(text=f"Aircon Condition: {condition}, Humidity: {humidity}")
         
            if condition == "Hot":
                play_aircon_gif()
                start_countdown(10, entered_temp)  
                remote_window.after(10000, lambda: (remote_window.destroy(), show_fan_mode()))
            elif condition == "Cool":
                play_aircon_gif()
                start_countdown(10, entered_temp) 
                remote_window.after(10000, remote_window.destroy)  
            elif condition == "Warm":
                play_aircon_gif()
                start_countdown(10, entered_temp)  
                remote_window.after(10000, remote_window.destroy)  

            result_label.config(text="Please enter a temperature between 16 and 30 °C.")
    except ValueError:
        result_label.config(text="Please enter a valid number.")

def open_remote_window():
    global temp_entry, remote_window

    remote_window = tk.Toplevel(root)
    remote_window.title("Remote Control")
    remote_window.geometry("300x200")
    remote_window.configure(bg="black")

    temp_label = tk.Label(remote_window, text="Enter Temperature (°C):", fg="white", bg="black")
    temp_label.pack(pady=20)

    temp_entry = tk.Entry(remote_window)
    temp_entry.pack(pady=5)

    submit_button = tk.Button(remote_window, text="Submit", command=submit_temperature)
    submit_button.pack(pady=10)

def animate_background(counter=0):
    bg_image = ImageTk.PhotoImage(bg_frames[counter])
    image_label.config(image=bg_image)
    image_label.image = bg_image  
    root.after(100, animate_background, (counter + 1) % len(bg_frames))

final_aircon_temp = 0
final_aircon_humidity = ""

def start_countdown(seconds, current_temp):
    global timer_label, current_temp_label, humidity_label, final_aircon_temp, final_aircon_humidity
    if aircon_window and aircon_window.winfo_exists():
        if seconds > 1:
            adjusted_temp = current_temp - (entered_temp - 18) * (10 - seconds) / 10
            current_temp_label.config(text=f"Current Temp: {adjusted_temp:.1f}°C")
            
            humidity = calculate_humidity(adjusted_temp)
            humidity_label.config(text=f"Humidity: {humidity}") 
            
            timer_label.config(text=f"Time Remaining: {seconds} sec")

            if seconds <= 3:
                timer_label.config(text="Switching to Fan Mode soon...")

            aircon_window.after(1000, start_countdown, seconds - 1, current_temp)
        else:
            timer_label.config(text="Switching to Fan Mode...")
            final_aircon_temp = float(current_temp_label.cget("text").split(': ')[1][:-2])
            final_aircon_humidity = humidity_label.cget("text").split(': ')[1]

            aircon_window.destroy()
            show_fan_mode()

def update_final_values():
    global final_aircon_temp, final_aircon_humidity
    final_aircon_temp = float(current_temp_label.cget("text").split(': ')[1][:-2])
    final_aircon_humidity = humidity_label.cget("text").split(': ')[1]

def play_aircon_gif(counter=0):
    global aircon_window, aircon_label, timer_label, temp_label, current_temp_label, humidity_label

    if aircon_window is None or not aircon_window.winfo_exists():
        aircon_window = tk.Toplevel(root)
        aircon_window.title("Aircon Cooling")
        aircon_window.geometry("1024x678")

        aircon_label = tk.Label(aircon_window)
        aircon_label.pack()

        timer_label = tk.Label(aircon_window, text="",
                                     font=("Fixedsys", 30), fg="black")
        timer_label.place(relx=0.5, rely=0.1, anchor="center") 

        temp_label = tk.Label(aircon_window, text=f"Entered Temp: {entered_temp}°C",
                                     font=("Fixedsys", 20), fg="black")
        temp_label.place(relx=0.5, rely=0.2, anchor="center")

        current_temp_label = tk.Label(aircon_window,
                                         font=("Fixedsys", 20), fg="black")
        current_temp_label.place(relx=0.5, rely=0.3, anchor="center")

        humidity_label = tk.Label(aircon_window,
                                         font=("Fixedsys", 20), fg="black")
        humidity_label.place(relx=0.5, rely=0.4, anchor="center")  

    ac_image = ImageTk.PhotoImage(ac_frames[counter])
    aircon_label.config(image=ac_image)
    aircon_label.image = ac_image  

    aircon_window.after(100, lambda: play_aircon_gif((counter + 1) % len(ac_frames)))

def play_fan_mode(counter=0, final_temp=0, final_humidity=""):
    global fan_window, fan_label, entered_temp, final_aircon_temp, final_aircon_humidity, humidity_label_fan, temp_label_fan, current_temp_label_fan

    if fan_window is None or not fan_window.winfo_exists():
        fan_window = tk.Toplevel(root)
        fan_window.title("Fan Mode")
        fan_window.geometry("1024x678")

        fan_label = tk.Label(fan_window)
        fan_label.pack()

        temp_label_fan = tk.Label(fan_window, text=f"Entered Temp: {entered_temp:.1f}°C",
                                     font=("Fixedsys", 20), fg="black")
        temp_label_fan.place(relx=0.5, rely=0.2, anchor="center")

        current_temp_label_fan = tk.Label(fan_window, text=f"New Temp: {final_temp:.1f}°C",
                                             font=("Fixedsys", 20), fg="black")
        current_temp_label_fan.place(relx=0.5, rely=0.3, anchor="center")

        humidity_label_fan = tk.Label(fan_window, text=f"Humidity: {final_humidity}",
                                         font=("Fixedsys", 20), fg="black")
        humidity_label_fan.place(relx=0.5, rely=0.4, anchor="center")

    fan_image = ImageTk.PhotoImage(fan_frames[counter])
    fan_label.config(image=fan_image)
    fan_label.image = fan_image

    fan_window.after(100, lambda: play_fan_mode((counter + 1) % len(fan_frames)))

def show_fan_mode():
    print("Displaying Fan Mode...")
    play_fan_mode(final_temp=final_aircon_temp, final_humidity=final_aircon_humidity)  

root = tk.Tk()
root.title("Cafe Aircon Controller")
root.geometry("1024x678")

image_label = tk.Label(root)
image_label.pack(fill="both", expand=True)

remote_button = tk.Button(root, text="Enter Temperature", command=open_remote_window,
                          font=("Arial", 12),
                          bg="#444444", fg="black",
                          bd=5, relief="raised")
remote_button.place(relx=0.5, rely=0.5, anchor="center")

result_label = tk.Label(root, text="")
result_label.pack()
bg_image = Image.open("main.gif")
bg_frames = [frame.copy() for frame in ImageSequence.Iterator(bg_image)]

ac_image = Image.open("cold.gif")
ac_frames = [frame.copy() for frame in ImageSequence.Iterator(ac_image)]

fan_image = Image.open("fan.gif")
fan_frames = [frame.copy() for frame in ImageSequence.Iterator(fan_image)]

animate_background()
root.mainloop()
