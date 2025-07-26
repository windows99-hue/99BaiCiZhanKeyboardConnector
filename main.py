import uiautomator2 as u2
import keyboard
from clc99 import *
import sys
import os
import signal

d = u2.connect()  # 连接设备
d.settings['operation_delay'] = (0, 0)  # 设置操作延迟为0

Backspace_x, Backspace_y = 1181, 2256

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
            print(f'发送字符 {e.name} 到设备')
            try:
                d(text=e.name).click()  # 点击对应的文本元素
            except:
                print(f'无法找到 {e.name} 键')
        
        # 处理特殊功能键
        elif e.name == "enter":
            d(text="提交").click()
        elif e.name == "backspace":
            print_status("发送退格键到设备")
            d.click(Backspace_x, Backspace_y)
    
# 设置全局键盘钩子
keyboard.hook(on_key_event, suppress=True)  # suppress=True阻止按键传播到其他应用

print_status("键盘监听已启动，按ESC键退出...")

keyboard.wait('esc')  # 等待ESC键被按下
keyboard.unhook_all()
print("程序已退出")