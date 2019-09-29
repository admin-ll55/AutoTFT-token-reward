from PyMacroV2 import *
import datetime
import re
from win32api import GetSystemMetrics
import pytesseract
import psutil
import win32process

def echo_status():
  global status
  msg = "["+str(datetime.datetime.now())+"]"+status
  print(msg)
  open("AutoTFT.log", 'ab').write((msg+"\n").encode())
  Delay(1)
def get_lolc_hwnd():
  def callback(hwnd, hwnds):
    if win32gui.GetWindowText(hwnd) == "League of Legends":
      rect = win32gui.GetWindowRect(hwnd)
      x = rect[0]
      y = rect[1]
      w = rect[2] - x
      h = rect[3] - y
      if len(hwnds) == 0 and w == 1280 and h == 720:
        hwnds.append(hwnd)
    return True
  hwnds = []
  win32gui.EnumWindows(callback, hwnds)
  return hwnds
fetched = False
while not fetched:
  try:
    lolc_hwnd = get_lolc_hwnd()[0]
    fetched = True
  except:
    fetched = False
#To-do
#if fetched == False:
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
        ShowWindowByHWND(lolc_hwnd)
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
      ShowWindowByHWND(lolc_hwnd)
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
      pos = FindImage("07_client_play_again.png", 0, 0, x, y, 0.8)
      while pos[0] == -1:
        ALT_TAB()
        Delay(1)
        ALT_TAB()
        Delay(1)
        pos = FindImage("07_client_play_again.png", 0, 0, x, y, 0.8)
        # SaveImage("[debug]client_play_again", 0, 0, x, y)
      opx, opy = FindImage("16_placement_bar.png", 0, 0, x, y, 0.8)
      opx = opx - 6
      px, py = FindImage("16_placement.png", opx, opy, opx+43, opy+409, 0.8)
      # SaveImage("[debug]16_placement", opx, opy, opx+43, opy+409)
      SaveImage("[debug]placement", opx+px+15, opy+py+6, opx+px+15+22, opy+py+6+22)
      place = str(pytesseract.image_to_string(cv2.bitwise_not(cv2.imread("[debug]placement.png")),config='--psm 7 digit'))
      # print(place)
      # input()
      status = "ended w/ "+place+"th place"
      echo_status()
      img = cv2.imread("07_client_play_again.png")
      height, width, channels = img.shape
      MouseLPress(pos[0]+width/2, pos[1]+height/2)
      MoveMouse(0, 0)
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
      ohpx, ohpy = (0, 0)
      hpx, hpy = FindImage("15_hp_corner.png", ohpx, ohpy, x, y, 0.8)
      SaveImage("[debug]hp", ohpx+hpx+11, ohpy+hpy+3, ohpx+hpx+11+25, ohpy+hpy+3+20)
      hp = str(pytesseract.image_to_string(cv2.bitwise_not(cv2.imread("[debug]hp.png")),config='--psm 7 digit'))
      # print(hpx, hpy, hp)
      # input()
      Delay(1)
      ClickOnImageLoop("05_game_setting_button.png", 0, 0, x, y, 0.8, 1)
      Delay(1)
      ClickOnImageLoop("13_ff.png", 0, 0, x, y, 0.8, 1)
      Delay(1)
      ClickOnImageLoop("14_ff_ff.png", 0, 0, x, y, 0.8, 1)
      Delay(1)
      status = "ff w/ "+hp+" hp"
      count = 0
      echo_status()
      Delay(8)
    if WindowExists(lolgc) and status == "queueing":
      Delay(10)
      SwitchToWindow(lolgc)
      Delay(1)
      if FindImage("09_rito.png", 0, 0, x, y, 0.8)[0] == -1:
        count += 1
        continue
      status = "ingame"
      count = 0
      echo_status()
    if WindowExists(lolc) and status == "queueing":
      ShowWindowByHWND(lolc_hwnd)
      Delay(1)
      # SaveImage("[debug]client_accept_match_button", 0, 0, x, y)
      if not ClickOnImage("02_client_accept_match_button.bmp", 0, 0, x, y, 0.95):
        count += 1
        continue
      MoveMouse(0, 0)
      count = 0
      status = "accepted"
      echo_status()
      status = "queueing"
      echo_status()
    if WindowExists(lolc) and status == "pending":
      ShowWindowByHWND(lolc_hwnd)
      Delay(1)
      # SaveImage("[debug]client_find_match_button", 0, 0, x, y)
      if not ClickOnImage("01_client_find_match_button.bmp", 0, 0, x, y, 0.8):
        count += 1
        continue
      MoveMouse(0, 0)
      status = "queueing"
      count = 0
      echo_status()
    Delay(1)
  except KeyboardInterrupt:
    exit()