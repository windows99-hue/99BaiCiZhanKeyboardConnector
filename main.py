import uiautomator2 as u2
import keyboard
from clc99 import *
import sys
import os
import signal
from tqdm import tqdm

print_admin("欢迎来到99百词斩键盘连接器！请确保您的手机已连接USB调试模式，并且已安装了百词斩APP。妥善配置uiautomation2库。")

d = u2.connect()  # 连接设备

print_good("设备连接成功！")
d.settings['operation_delay'] = (0, 0)  # 设置操作延迟为0

print_status("正在预处理键盘位置。。。")
key_position = {} # 0为x，1为y
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

print_good("预处理完成！")

def on_key_event(e):
    # 只处理按键按下事件
    if e.event_type == keyboard.KEY_DOWN:
        if e.name == "esc":
            print_warning("退出程序")
            keyboard.unhook_all()
            os.kill(os.getpid(), signal.SIGINT)
            sys.exit()
        # 处理普通字符键
        if e.name.isprintable() and len(e.name) == 1:
            print_status(f'发送字符 {e.name} 到设备')
            try:
                d.click(key_position[e.name][0], key_position[e.name][1])  # 点击对应的文本元素
            except:
                print(f'无法找到 {e.name} 键')
        
        # 处理特殊功能键
        elif e.name == "enter":
            d.click(x=key_position["enter"][0], y=key_position["enter"][1])
        elif e.name == "backspace":
            print_status("发送退格键到设备")
            d.click(x=key_position["backspace"][0], y = key_position["backspace"][1])
    
# 设置全局键盘钩子
keyboard.hook(on_key_event, suppress=True)  # suppress=True阻止按键传播到其他应用

print_status("键盘监听已启动，按ESC键退出...")

keyboard.wait('esc')  # 等待ESC键被按下
keyboard.unhook_all()
print("程序已退出")