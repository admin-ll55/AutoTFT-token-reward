from PyMacroV2 import *
import datetime
import re
from win32api import GetSystemMetrics
import pytesseract

def echo_status():
  global status
  msg = "["+str(datetime.datetime.now())+"]"+status
  print(msg)
  open("AutoTFT.log", 'ab').write((msg+"\n").encode())
  Delay(1)

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'
x, y = (GetSystemMetrics(0), GetSystemMetrics(1))
lolc = "League of Legends"
lolgc = "League of Legends (TM) Client"
ziggs = "Woops! Something broke."
status = ""
# status = "queueing"
count = 1
limit = 60*15
unit_cost_rgb = ((39,57,71),(8,92,39),(15,96,117),(140,31,140),(110,96,64))
# limit = 1

while True:
  try:
    if status == "":
      if WindowExists(lolgc):
        status = "ingame"
      else:
        SwitchToWindow(lolc)
        Delay(1)
        if FindImage("07_client_play_again.png", 0, 0, x, y, 0.8)[0] > 0:
          status = "ff"
        elif FindImage("01_client_find_match_button.bmp", 0, 0, x, y, 0.8)[0] > 0:
          status = "pending"
        else:
          status = "queueing"
      echo_status()
    if count > 15*60/1.5:
      count = 0
      status = ""
      msg = "["+str(datetime.datetime.now())+"]same status stuck for "+str(count)+", resetting"
      print(msg)
      open("AutoTFT.log", 'ab').write((msg+"\n").encode())
      continue
    if WindowExists(ziggs):
      SwitchToWindow(ziggs)
      Delay(1)
      ClickOnImage("12_bugsplat_dont_send.png", 0, 0, x, y, 0.8)
      Delay(1)
    if WindowExists(lolc):
      SwitchToWindow(lolc)
      Delay(1)
      if ClickOnImage("00_client_reconnect_button.bmp", 0, 0, x, y, 0.8):
        status = "queueing"
        Delay(1)
    if WindowExists(lolc) and re.search("^ff", status) != None:
      ALT_TAB()
      Delay(1)
      ALT_TAB()
      Delay(1)
      if ClickOnImage("10_client_confirm_mission.png", 0, 0, x, y, 0.8):
        Delay(5)
        continue
      # SaveImage("[debug]client_play_again", 0, 0, x, y)
      while FindImage("07_client_play_again.png", 0, 0, x, y, 0.8)[0] == -1:
        ALT_TAB()
        Delay(1)
        ALT_TAB()
        Delay(1)
        # SaveImage("[debug]client_play_again", 0, 0, x, y)
      #7 317
      #22 322 22 22
      px, py = FindImage("16_placement.png", 349, 256, 392, 665, 0.8)
      # SaveImage("[debug]16_placement", 349, 256, 392, 665)
      SaveImage("[debug]placement", 349+px+15, 256+py+6, 349+px+15+22, 256+py+6+22)
      place = str(pytesseract.image_to_string(cv2.bitwise_not(cv2.imread("[debug]placement.png")),config='--psm 7 digit'))
      # print(place)
      # input()
      status = "ended w/ "+place+"th place"
      echo_status()
      MoveToImage("07_client_play_again.png", 0, 0, x, y, 0.8)
      Delay(1)
      ClickOnImage("07_client_play_again.png", 0, 0, x, y, 0.8)
      status = "pending"
      count = 0
      echo_status()
    if WindowExists(lolgc) and status == "ingame":
      SwitchToWindow(lolgc)
      Delay(1)
      #745 828
      #894 828
      #1044 828
      #1193 828
      #1342 828
      # SaveImage("grab_cost", 0, 0, x, y)
      # img = str(cv2.imread("grab_cost.png")[828,745])
      # img = re.sub("(\[|\])", "", re.sub("\s+", " ", img)).split(" ")
      # temp = img[2]
      # img = (int(temp), int(img[1]), int(img[0]))
      # print(unit_cost_rgb)
      # print(img)
      # print(unit_cost_rgb.index(img))
      # exit()
      if FindImage("05_game_setting_button.png", 0, 0, x, y, 0.8)[0] == -1:
        count += 1
        continue
      for z in range(0, limit):
        Delay(1)
        print("\r"+str((limit-z)//60).zfill(2)+"m "+str((limit-z)%60).zfill(2)+"s left", end='')
      print("\r",end='')
      # SwitchToWindow(lolgc)
      # Delay(1)
      #0 672
      #11 675 25 20
      hpx, hpy = FindImage("15_hp_corner.png", 1493, 0, x, y, 0.8)
      SaveImage("[debug]hp", 1493+hpx+11, hpy+3, 1493+hpx+11+25, hpy+3+20)
      hp = str(pytesseract.image_to_string(cv2.bitwise_not(cv2.imread("[debug]hp.png")),config='--psm 7 digit'))
      # print(hp)
      # input()
      Delay(1)
      ClickOnImage("05_game_setting_button.png", 0, 0, x, y, 0.8)
      Delay(1)
      ClickOnImage("13_ff.png", 0, 0, x, y, 0.95)
      Delay(1)
      ClickOnImage("14_ff_ff.png", 0, 0, x, y, 0.8)
      Delay(1)
      status = "ff w/ "+hp+" hp"
      count = 0
      echo_status()
      Delay(8)
    if WindowExists(lolgc) and status == "queueing":
      SwitchToWindow(lolgc)
      Delay(1)
      if FindImage("09_rito.png", 0, 0, x, y, 0.8)[0] == -1:
        count += 1
        continue
      status = "ingame"
      count = 0
      echo_status()
    if WindowExists(lolc) and status == "queueing":
      SwitchToWindow(lolc)
      Delay(1)
      # SaveImage("[debug]client_accept_match_button", 0, 0, x, y)
      if not ClickOnImage("02_client_accept_match_button.bmp", 0, 0, x, y, 0.8):
        count += 1
        continue
      else:
        MoveMouse(0, 0)
        count = 0
        status = "accepted"
        echo_status()
        status = "queueing"
        echo_status()
    if WindowExists(lolc) and status == "pending":
      SwitchToWindow(lolc)
      Delay(1)
      # SaveImage("[debug]client_find_match_button", 0, 0, x, y)
      if not ClickOnImage("01_client_find_match_button.bmp", 0, 0, x, y, 0.8):
        count += 1
        continue
      status = "queueing"
      count = 0
      echo_status()
    Delay(1)
  except KeyboardInterrupt:
    exit()