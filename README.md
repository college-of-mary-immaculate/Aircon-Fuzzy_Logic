# Cafe Aircon Controller 🏡☕

## WHAT ❓
The **Cafe Aircon Controller** is a Python-based Tkinter application designed to simulate the operation of an air conditioner in a café/home environment. The app features a simple GUI where users can enter a temperature value, and based on fuzzy logic, the air conditioner will respond with cooling or fan mode, depending on the temperature input. The humidity of the environment will also adjust, and it will be based on the temperature of the same environment. Animated GIFs of an air conditioner and fan play as a visual representation of the system's status.

## REQUIREMENTS 📝
To run this project, the following dependencies need to be installed:

- **Python 3.11.9** - The main programming language used for this application.
- **Pillow 10.3.0** - A Python Imaging Library (PIL fork) used to handle images and GIFs within the Tkinter application.

You can install the required Python packages by running:
(you can install them in the terminal or bash)
pip install Pillow

## HOW TO USE 📃

1.Clone or download the repository containing this project.
2.Install the required packages using the pip install Pillow command.
3.Ensure that the GIF files (main.gif, cold.gif, fan.gif) are located in the same directory as the Python script. (In this case, I uploaded a folder named, 'Source Code', make sure that when you open the code/folder in your chosen IDE, make sure that you open the folder itself, containing the GIF files. )
4.Run the Python script:
5.The application will launch with an animated background. Press the "Enter Temperature" button, input a temperature. The air conditioner will switch to cooling or fan mode based on the fuzzy logic system.

Fuzzy Logic Temperature Ranges: 🖇️

❄️ Cool Membership Function**:
   - Defined for temperatures ranging from 10°C to 18°C.
🍃 Warm Mode:
   - Defined for temperatures ranging from 18°C to 30°C, with a peak value at 24°C.
🥵 Hot Mode: If the temperature is above 26°C, the system will play the cooling GIF and transition to fan mode after a set time.
   - Defined for temperatures above 26°C.

## CREDITS ©️
This project is built using Python and Tkinter, with the following contributors:
-Bracia, Genniesys
-Galvez, Raecell Ann D.

Pillow library for image handling.
All GIF files are used for visual representations in the project.

## LICENSE 🪪
This project is licensed under the MIT License. See the LICENSE file for more details.