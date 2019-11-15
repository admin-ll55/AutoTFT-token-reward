from PyMacroV2 import *
import datetime
import re
from win32api import GetSystemMetrics
import pytesseract
import psutil
import win32process
import subprocess
import threading
def job(z):
  global status
  cmd = 'tasklist /fi "imagename eq league of legends.exe" /v'
  s = subprocess.Popen(cmd, stdout=subprocess.PIPE).stdout.read().decode()
  if "League of Legends.exe" in s and "Unknown" in s:
    status = s
    echo_status()
    subprocess.Popen(["[end_lolgc].bat"])
    subprocess.Popen(["[run].bat", z])
    exit()
def echo_status():
  global status
  msg = "["+str(datetime.datetime.now())+"]"+status
  print(msg)
  open("AutoTFT.log", 'ab').write((msg+"\n").encode())
  Delay(1)
def get_lolc_hwnd():
  def callback(hwnd, ctx):
    if win32gui.GetWindowText(hwnd) == "League of Legends":
      rect = win32gui.GetWindowRect(hwnd)
      x = rect[0]
      y = rect[1]
      w = rect[2] - x
      h = rect[3] - y
      if len(hwnds) == 0 and w in (160, 1280) and h in (28, 720):
        hwnds.append(hwnd)
  while True:
    hwnds = []
    win32gui.EnumWindows(callback, None)
    try:
      return hwnds[0]
    except:
      pass
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'
x, y = (GetSystemMetrics(0), GetSystemMetrics(1))
lolc = "League of Legends"
lolgc = "League of Legends (TM) Client"
ziggs = "Woops! Something broke."
if WindowExists(lolc):
  lolc_hwnd = get_lolc_hwnd()
status = ""
# status = "queueing"
count = 1
limit = 60*15
timer = 60*2
# timer = 60*15
unit_cost_rgb = ((39,57,71),(8,92,39),(15,96,117),(140,31,140),(110,96,64))
# limit = 1
while True:
  try:
    if status == "":
      if WindowExists(lolgc):
        status = "ingame"
      elif WindowExists(lolc):
        ShowWindowByHWND(lolc_hwnd)
        Delay(1)
        if FindImage("07_client_play_again.png", 0, 0, x, y, 0.95)[0] > 0:
          status = "ff"
        elif FindImage("01_client_find_match_button.bmp", 0, 0, x, y, 0.95)[0] > 0:
          status = "pending"
        else:
          status = "queueing"
      else:
        count = 121
        status = "queueing"
      echo_status()
    if count > timer:
      if status == "queueing" or FindImage("03_game_reconnecting_message.bmp", 0, 0, x, y, 0.95):
        subprocess.call(["[end_lolc].bat"])
        if FindImage("03_game_reconnecting_message.bmp", 0, 0, x, y, 0.95):
          subprocess.call(["[end_lolgc].bat"])
        Delay(1)
        if WindowExists("Garena - Game Center"):
          SwitchToWindow("Garena - Game Center")
          Delay(4)
          ClickOnImage("19_stuck_1.png", 0, 0, x, y, 0.95)
          Delay(2)
          ClickOnImage("19_stuck_2.png", 0, 0, x, y, 0.95)
          Delay(30*2)
          lolc_hwnd = get_lolc_hwnd()
          ShowWindowByHWND(lolc_hwnd)
          Delay(2)
          ClickOnImage("18_stuck_queueing_0.png", 0, 0, x, y, 0.95) # or start button
          Delay(2)
          ClickOnImage("18_stuck_queueing_1.png", 0, 0, x, y, 0.95)
          Delay(2)
          ClickOnImage("18_stuck_queueing_2.png", 0, 0, x, y, 0.95)
          Delay(2)
          ClickOnImage("18_stuck_queueing_3.png", 0, 0, x, y, 0.95)
          Delay(2)
          ClickOnImage("18_stuck_queueing_4.png", 0, 0, x, y, 0.95)
          Delay(2)
      msg = "["+str(datetime.datetime.now())+"]same status '"+status+"' stuck for "+str(count)+", resetting"
      count = 0
      status = ""
      print(msg)
      open("AutoTFT.log", 'ab').write((msg+"\n").encode())
      continue
    if WindowExists(ziggs):
      SwitchToWindow(ziggs)
      Delay(1)
      ClickOnImage("12_bugsplat_dont_send.png", 0, 0, x, y, 0.95)
      Delay(1)
    if WindowExists(lolc):
      ShowWindowByHWND(lolc_hwnd)
      Delay(1)
      if ClickOnImage("00_client_reconnect_button.bmp", 0, 0, x, y, 0.95):
        status = "queueing"
        Delay(1)
      if ClickOnImage("08_client_skip_result.png", 0, 0, x, y, 0.95):
        status = "pending"
        count = 9999
        Delay(1)
      if ClickOnImage("10_client_confirm_mission.png", 0, 0, x, y, 0.95):
        status = "ff"
        Delay(5)
        continue
    if WindowExists(lolc) and re.search("^ff", status) != None:
      if WindowExists(lolgc):
        Delay(10)
        if WindowExists(lolgc):
          SwitchToWindow(lolgc)
          Delay(1)
          KeyPress(Key.enter)
          Delay(1/3)
          KeyPress(Key_('/'))
          Delay(1/3)
          KeyPress(Key_('f'))
          Delay(1/3)
          KeyPress(Key_('f'))
          Delay(1/3)
          KeyPress(Key.enter)
          Delay(1)
          ClickOnImage("13_ff.png", 0, 0, x, y, 0.95) or ClickOnImage("14_ff_ff.png", 0, 0, x, y, 0.95)
          continue
      ALT_TAB()
      Delay(1)
      ShowWindowByHWND(lolc_hwnd)
      win32gui.MoveWindow(lolc_hwnd, int((x-1280)/2), int((y-720)/2), 1280, 720, True)
      Delay(1)
      # SaveImage("[debug]client_play_again", 0, 0, x, y)
      pos = FindImage("07_client_play_again.png", 0, 0, x, y, 0.95)
      ok = True
      while pos[0] == -1:
        ALT_TAB()
        Delay(1)
        ShowWindowByHWND(lolc_hwnd)
        win32gui.MoveWindow(lolc_hwnd, int((x-1280)/2), int((y-720)/2), 1280, 720, True)
        Delay(1)
        pos = FindImage("07_client_play_again.png", 0, 0, x, y, 0.95)
        # SaveImage("[debug]client_play_again", 0, 0, x, y)
        count += 1
        if count > timer:
          ok = False
          break
      if not ok:
        continue
      opx, opy = FindImage("16_placement_bar.png", 0, 0, x, y, 0.95)
      opx = opx - 6
      px, py = FindImage("16_placement.png", opx, opy, opx+43, opy+409, 0.95)
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
      subprocess.Popen(["[run].bat", ""])
      exit()
    if not WindowExists(lolgc) and status == "ingame":
      Delay(10)
      if not WindowExists(lolgc) and status == "ingame":
        status = ""
        count = 0
        continue
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
      for z in range(0, limit):
        try:
          Delay(1)
          print("\r"+str((limit-z)//60).zfill(2)+"m "+str((limit-z)%60).zfill(2)+"s left", end='')
          if z % 7 == 0:
            threading.Thread(target=job, args=(z,)).start()
        except KeyboardInterrupt:
          break
      print("\r",end='')
      # SwitchToWindow(lolgc)
      # Delay(1)
      #0 672
      #11 675 25 20
      ohpx, ohpy = (0, 0)
      hpx, hpy = FindImage("15_hp_corner.png", ohpx, ohpy, x, y, 0.95)
      SaveImage("[debug]hp", ohpx+hpx+11, ohpy+hpy+3, ohpx+hpx+11+25, ohpy+hpy+3+20)
      hp = str(pytesseract.image_to_string(cv2.bitwise_not(cv2.imread("[debug]hp.png")),config='--psm 7 digit'))
      # print(hpx, hpy, hp)
      # input()
      Delay(1)
      ok = False
      while not ok:
        ShowWindowByHWND(lolc)
        SwitchToWindow(lolgc)
        KeyPress(Key.enter)
        Delay(1/3)
        KeyPress(Key_('/'))
        Delay(1/3)
        KeyPress(Key_('f'))
        Delay(1/3)
        KeyPress(Key_('f'))
        Delay(1/3)
        KeyPress(Key.enter)
        Delay(1)
        if ClickOnImage("13_ff.png", 0, 0, x, y, 0.95) or ClickOnImage("14_ff_ff.png", 0, 0, x, y, 0.95):
          ok = True
        else:
          ok = False
          if not WindowExists(lolgc):
            count = 9999
            break
        Delay(1)
      if not ok:
        continue
      status = "ff w/ "+hp+" hp"
      count = 0
      echo_status()
      Delay(8)
    if WindowExists(lolgc) and status == "queueing":
      Delay(10)
      SwitchToWindow(lolgc)
      Delay(1)
      if FindImage("09_rito.png", 0, 0, x, y, 0.95)[0] == -1:
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
        if FindImage("18_stuck_queueing_0.png", 0, 0, x, y, 0.95)[0] != -1:
          count = 9999
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
      if not ClickOnImage("01_client_find_match_button.bmp", 0, 0, x, y, 0.95):
        count += 1
        continue
      MoveMouse(0, 0)
      status = "queueing"
      count = 0
      echo_status()
    Delay(1)
  except KeyboardInterrupt:
    exit()