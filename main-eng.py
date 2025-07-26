import uiautomator2 as u2
import keyboard
from clc99 import *
import sys
import os
import signal
from tqdm import tqdm

print_admin("Welcome to the 99 Baicizhan Keyboard Connector! Please ensure your phone is connected in USB debugging mode and the Baicizhan app is installed. Configure the uiautomator2 library properly.")
print_uquestion("Press F2 to switch modes, press ESC to exit the program.")
print_status("Initializing program...")

d = u2.connect()

print_good("Device connected successfully!")
d.settings['operation_delay'] = (0, 0)  # Set operation delay to 0

d.app_start("com.jiongji.andriod.card") # Launch Baicizhan

key_position = {} # 0 for x, 1 for y
areas_position = {}

is_key_init = False
is_4areas_init = False

def init_keyboard():
    global is_key_init
    for i in tqdm(range(ord('a'), ord('z')+1)):
        try: 
            i = chr(i)
            x, y = d(text=i).center()
            key_position[i] = [x, y]
        except u2.exceptions.UiObjectNotFoundError:
            print_error("Failed to locate Baicizhan keyboard position. Please open Baicizhan and press 'y' to retry")
            keyboard.wait("y")
            i = ord('a')
            continue
        except Exception as e:
            print_e(f"Error occurred: {e}")

    key_position["backspace"] = [None, None, None]
    key_position["backspace"][1] = key_position["m"][1]
    key_position["backspace"][0] = key_position["m"][0] * 1.2

    key_position["enter"] = [None, None, None]
    key_position["enter"][0], key_position["enter"][1] = d(text="Submit").center() 
    print_good("Keyboard position acquired successfully!")
    is_key_init = True

def init_4areas():
    global is_4areas_init
    print_status("Acquiring four-quadrant positions...")

    four_area_list = d.xpath("//*[@resource-id=\"root\"]/*[1]/*[6]/*[1]/*[2]/*[1]/*").all()  # XPath比UIAuto.Dev大1,也就是比列表下标大1，从1开始算

    try:
        areas_position["leftup"] = [None, None, None]
        areas_position["leftdown"] = [None, None, None]
        areas_position["rightup"] = [None, None, None]
        areas_position["rightdown"] = [None, None, None]
        areas_position["next-question"] = [None, None, None]

        areas_position["leftup"][0], areas_position["leftup"][1] = four_area_list[0].center()
        areas_position["rightup"][0], areas_position["rightup"][1] = four_area_list[1].center()
        areas_position["leftdown"][0], areas_position["leftdown"][1] = four_area_list[2].center()
        areas_position["rightdown"][0], areas_position["rightdown"][1] = four_area_list[3].center()
    except u2.exceptions.UiObjectNotFoundError:
        print_error("Failed to locate four-quadrant positions. Please open Baicizhan and press 'y' to retry")
        keyboard.wait("y")
        init_4areas()
        return
    except Exception as e:
        print_e(f"Error occurred: {e}")
        return
    print_good("Four-quadrant positions acquired successfully!")

    print_status("Acquiring 'Next Question' position")
    areas_position["next-question"][0], areas_position["next-question"][1] = d.xpath("//*[@text=\"h9c7+xOXaSrtKuTcsVlQjWJyZ6Djn0fGF5seRevYGwk1S3vGRkZGRkZGRkZev4DJ5jPuVdPXb0AAAAASUVORK5CYII=\"]").center()
    print_good("'Next Question' position acquired! Press Enter to click the next question button.")

    is_4areas_init = True

print_warning("Please ensure the Baicizhan app is open and in the question interface.")

while True:
    cmd = input("1 for keyboard mode, 2 for four-quadrant mode, 3 to exit: ")
    if cmd == "1":
        print_good("Keyboard mode selected!")
        mode = "kbd"
        break
    elif cmd == "2":
        print_good("Four-quadrant mode selected!")
        mode = "4areas"
        break
    elif cmd == "3":
        sys.exit(0)
    else:
        print_error("Invalid input, please enter 1 or 2.")
        continue

if mode == "kbd":
    init_keyboard()
elif mode == "4areas":
    init_4areas()

print_good("Preprocessing completed!")


def on_key_event(e):
    # Only process key down events
    if e.event_type == keyboard.KEY_DOWN:
        if e.name == "esc":
            print_warning("Exiting program")
            keyboard.unhook_all()
            os.kill(os.getpid(), signal.SIGINT)
            sys.exit()
        if e.name == "f2":
            global mode
            mode = "4areas" if mode == "kbd" else "kbd"
            if mode == "kbd" and not is_key_init:
                init_keyboard()
            elif mode == "4areas" and not is_4areas_init:
                init_4areas()
            print_status("Switched to {} mode".format("keyboard" if mode == "kbd" else "four-quadrant"))

        # Process character keys
        if mode == "kbd":
            if e.name.isprintable() and len(e.name) == 1:
                try:
                    d.click(key_position[e.name][0], key_position[e.name][1])
                except:
                    print_error(f'Failed to find {e.name} key')
            
            # Process special function keys
            elif e.name == "enter":
                d.click(x=key_position["enter"][0], y=key_position["enter"][1])
            elif e.name == "backspace":
                print_status("Sending backspace to device")
                d.click(x=key_position["backspace"][0], y = key_position["backspace"][1])
        elif mode == "4areas":
                if e.name == "w":
                    d.click(x=areas_position["leftup"][0], y=areas_position["leftup"][1])
                elif e.name == "s":
                    d.click(x=areas_position["leftdown"][0], y=areas_position["leftdown"][1])
                elif e.name == "e":
                    d.click(x=areas_position["rightup"][0], y=areas_position["rightup"][1])
                elif e.name == "d":
                    d.click(x=areas_position["rightdown"][0], y=areas_position["rightdown"][1])
                elif e.name == "enter":
                    d.click(x=areas_position["next-question"][0], y=areas_position["next-question"][1])
    
# Set global keyboard hook
keyboard.hook(on_key_event, suppress=True)  # suppress=True prevents key propagation to other apps

print_status("Keyboard listener activated, press ESC to exit...")

keyboard.wait('esc')  # Wait for ESC key press
keyboard.unhook_all()
print("Program exited")