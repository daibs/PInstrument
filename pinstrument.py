# -*- coding: utf-8 -*-
"""
@author: pi
"""

import signal
import time
import os
import touchphat
import pygame.time
import pygame.mixer
pygame.mixer.pre_init(44100,-16,2,512)
pygame.mixer.init()

type_num = 5
tone_num = 13
tone_color = 0
all_tone_num = tone_num * type_num
tone = [0 for i in range(all_tone_num)]
directory = "/home/pi/python/wave/"

scale = ["C","CS","D","DS","E","F","FS","G","GS","A","AS","B","CO"]
source_type = ["","_tri","_sin","_rect","_saw"]
extension = ".WAV"
for j in range(type_num):
    for i in range(tone_num):
        tone[i + j * tone_num] = pygame.mixer.Sound(directory + scale[i] + source_type[j] + extension)

for pad in ['Back','A','B','C','D','Enter']:
    touchphat.set_led(pad, True)
    time.sleep(0.1)
    touchphat.set_led(pad, False)
    time.sleep(0.1)
    
key_dict = {"A":0,"B":2,"C":4,"D":5}
enter = 0
sharp = 0
enter_start_time = 0
enter_time = 0
sharp_start_time = 0
sharp_time = 0
@touchphat.on_touch(['Back','A','B','C','D','Enter'])
def handle_touch(event):
    global enter
    global sharp
    global tone_color
    global enter_start_time
    global sharp_start_time
    global enter_time
    global sharp_time
    if event.name == "Enter":
        enter = 7
        enter_time = 0
        enter_start_time = time.time()
    elif event.name == "Back":
        sharp = 1
        sharp_time = 0
        sharp_start_time = time.time()
    else:
        if key_dict[event.name] + enter + sharp > 12:
            pygame.mixer.stop()
            if tone_color == 4:
                tone_color = 0
            else:
                tone_color += 1
            print("change")
        else:
            tone[key_dict[event.name] + enter + sharp + tone_color * tone_num].play()
    print(event.name)

@touchphat.on_release(['Back','A','B','C','D','Enter'])
def handle_release(event):
    global enter
    global sharp
    global tone_color
    global enter_start_time
    global sharp_start_time
    global enter_time
    global sharp_time
    shutdown_time = 5
    if event.name == "Enter":
        enter = 0
        pygame.mixer.stop()
        enter_stop_time = time.time()
        enter_time = enter_stop_time - enter_start_time
        print(enter_time)
    elif event.name == "Back":
        sharp = 0
        pygame.mixer.stop()
        sharp_stop_time = time.time()
        sharp_time = sharp_stop_time - sharp_start_time
        print(sharp_time)
    else:
        if key_dict[event.name] + enter + sharp > 12:
            print("chage")
        else:
            tone[key_dict[event.name] + enter + sharp + tone_color * tone_num].stop()
    if enter_time > shutdown_time and sharp_time > shutdown_time:
        print("shutdown")
        for pad in ['Enter','D','C','B','A','Back']:
            touchphat.set_led(pad, True)
            time.sleep(0.1)
            touchphat.set_led(pad, False)
            time.sleep(0.1)        
        for i in range(3):
            touchphat.all_on()
            time.sleep(0.1)
            touchphat.all_off()
            time.sleep(0.1)
        os.system("sudo shutdown -h now")
    print(event.name + " release")



signal.pause()
