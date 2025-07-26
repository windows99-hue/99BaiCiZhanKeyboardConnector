import uiautomator2 as u2
import keyboard
from clc99 import *
import sys
import os
import signal
from tqdm import tqdm

print_admin("欢迎来到99百词斩键盘连接器！请确保您的手机已连接USB调试模式，并且已安装了百词斩APP。妥善配置uiautomation2库。")
print_uquestion("按下F2可切换模式，按下ESC可退出程序。")
print_status("正在初始化程序...")

d = u2.connect()

print_good("设备连接成功！")
d.settings['operation_delay'] = (0, 0)  # 设置操作延迟为0

key_position = {} # 0为x，1为y
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
            print_error("无法找到百词斩键盘位置，请打开百词斩后按下y重试")
            keyboard.wait("y")
            i = ord('a')
            continue
        except Exception as e:
            print_e(f"发生错误: {e}")

    key_position["backspace"] = [None, None, None]
    key_position["backspace"][1] = key_position["m"][1]
    key_position["backspace"][0] = key_position["m"][0] * 1.2

    key_position["enter"] = [None, None, None]
    key_position["enter"][0], key_position["enter"][1] = d(text="提交").center() 
    print_good("键盘位置获取成功！")
    is_key_init = True

def init_4areas():
    global is_4areas_init
    print_status("正在获取四方格位置...")

    try:
        areas_position["leftup"] = [None, None, None]
        areas_position["leftdown"] = [None, None, None]
        areas_position["rightup"] = [None, None, None]
        areas_position["rightdown"] = [None, None, None]
        areas_position["next-question"] = [None, None, None]

        areas_position["leftup"][0], areas_position["leftup"][1] = d(className="android.view.View")[16].center()
        areas_position["rightup"][0], areas_position["rightup"][1] = d(className="android.view.View")[17].center()
        areas_position["leftdown"][0], areas_position["leftdown"][1] = d(className="android.view.View")[18].center()
        areas_position["rightdown"][0], areas_position["rightdown"][1] = d(className="android.view.View")[19].center()
    except u2.exceptions.UiObjectNotFoundError:
        print_error("无法找到四方格位置，请打开百词斩后按下y重试")
        keyboard.wait("y")
        init_4areas()
        return
    except Exception as e:
        print_e(f"发生错误: {e}")
        return
    print_good("四方格位置获取成功！")

    print_status("正在获取\"下一题\"位置")
    areas_position["next-question"][0], areas_position["next-question"][1] = d(className="android.view.View")[29].center()
    print_good("\"下一题\"获取成功！按下回车键可以按下下一题按钮。")

    is_4areas_init = True

print_warning("请确保百词斩APP已打开，并且处于答题界面。")

while True:
    cmd = input("1为键盘模式, 2为四方格模式, 3退出: ")
    if cmd == "1":
        print_good("已选择键盘模式！")
        mode = "kbd"
        break
    elif cmd == "2":
        print_good("已选择四方格模式！")
        mode = "4areas"
        break
    elif cmd == "3":
        sys.exit(0)
    else:
        print_error("无效输入，请输入1或2。")
        continue

if mode == "kbd":
    init_keyboard()
elif mode == "4areas":
    init_4areas()

print_good("预处理完成！")


def on_key_event(e):
    # 只处理按键按下事件
    if e.event_type == keyboard.KEY_DOWN:
        if e.name == "esc":
            print_warning("退出程序")
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
            print_status("切换模式为{}".format("键盘" if mode == "kbd" else "四方格"))

        # 处理普通字符键
        if mode == "kbd":
            if e.name.isprintable() and len(e.name) == 1:
                #print_status(f'发送字符 {e.name} 到设备')
                try:
                    d.click(key_position[e.name][0], key_position[e.name][1])  # 点击对应的文本元素
                except:
                    print_error(f'无法找到 {e.name} 键')
            
            # 处理特殊功能键
            elif e.name == "enter":
                d.click(x=key_position["enter"][0], y=key_position["enter"][1])
            elif e.name == "backspace":
                print_status("发送退格键到设备")
                d.click(x=key_position["backspace"][0], y = key_position["backspace"][1])
        elif mode == "4areas":
                if e.name == "w":
                    #print_status("按下左上")
                    d.click(x=areas_position["leftup"][0], y=areas_position["leftup"][1])
                elif e.name == "s":
                    #print_status("按下左下")
                    d.click(x=areas_position["leftdown"][0], y=areas_position["leftdown"][1])
                elif e.name == "e":
                    #print_status("按下右上")
                    d.click(x=areas_position["rightup"][0], y=areas_position["rightup"][1])
                elif e.name == "d":
                    #print_status("按下右下")
                    d.click(x=areas_position["rightdown"][0], y=areas_position["rightdown"][1])
                elif e.name == "enter":
                    #print_status("按下下一题")
                    d.click(x=areas_position["next-question"][0], y=areas_position["next-question"][1])
    
# 设置全局键盘钩子
keyboard.hook(on_key_event, suppress=True)  # suppress=True阻止按键传播到其他应用

print_status("键盘监听已启动，按ESC键退出...")

keyboard.wait('esc')  # 等待ESC键被按下
keyboard.unhook_all()
print("程序已退出")