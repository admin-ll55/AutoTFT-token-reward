from PyMacroV2 import *
import datetime
import re
from win32api import GetSystemMetrics
import pytesseract
import psutil
import win32process
import subprocess
import threading
import traceback
import sys
import time
#subprocess.Popen('start /min "" AutoTFT3.py', shell=True)
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
  win32gui.MoveWindow(lolc_hwnd, 0, 0, 1280, 720, True)
status = ""
# status = "queueing"
count = 1
limit = 60*20
if len(sys.argv) == 2:
  if sys.argv[1] != "":
    limit = int(sys.argv[1])
    status = "ingame"
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
        subprocess.Popen('start /min "" [end_lolc].bat', shell=True)
        if FindImage("03_game_reconnecting_message.bmp", 0, 0, x, y, 0.95):
          subprocess.Popen('start /min "" [end_lolgc].bat', shell=True)
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
      lolc_hwnd = get_lolc_hwnd()
      ShowWindowByHWND(lolc_hwnd)
      # win32gui.MoveWindow(lolc_hwnd, int((x-1280)/2), int((y-720)/2), 1280, 720, True)
      win32gui.MoveWindow(lolc_hwnd, 0, 0, 1280, 720, True)
      Delay(1)
      # SaveImage("[debug]client_play_again", 0, 0, x, y)
      pos = FindImage("07_client_play_again.png", 0, 0, x, y, 0.95)
      ok = True
      while pos[0] == -1:
        ALT_TAB()
        Delay(1)
        ShowWindowByHWND(lolc_hwnd)
        # win32gui.MoveWindow(lolc_hwnd, int((x-1280)/2), int((y-720)/2), 1280, 720, True)
        win32gui.MoveWindow(lolc_hwnd, 0, 0, 1280, 720, True)
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
      subprocess.Popen('start /min "" [run].bat', shell=True)
      sys.exit(0)
    if not WindowExists(lolgc) and status == "ingame":
      Delay(10)
      if not WindowExists(lolgc) and status == "ingame":
        status = ""
        count = 0
        continue
    if WindowExists(lolgc) and status == "ingame":
      SwitchToWindow(lolgc)
      Delay(1)
      r = False
      units = [
        ["20_master_yi.png", 0],
        ["20_sivir.png", 0],
        ["20_aatrox.png", 0],
        ["20_yasuo.png", 0],
        ["20_janna.png", 0],
        ["20_reksai.png", 0],
        ["20_nocturne.png", 0]
      ]
      qiyana = ["20_qiyana.png", 0]
      khazix = ["20_khazix.png", 0]
      qiyanas = [
        "20_qiyana_rock.png",
        "20_qiyana_ocea.png",
        "20_qiyana_fire.png"
      ]
      item = (
        "20_belt.png",
        "20_bow.png",
        "20_chest.png",
        "20_cloak.png",
        "20_glove.png",
        "20_rod.png",
        "20_spat.png",
        "20_sword.png",
        "20_tear.png"
      )
      is_wind = None
      appended = False
      r = True
      starttime = int(time.time())
      while True:
        def timeleft():
          return str((limit-(int(time.time())-starttime))//60).zfill(2)+"m "+str((limit-(int(time.time())-starttime))%60).zfill(2)+"s left "
        if int(time.time()) - starttime > limit:
          break
        try:
          if FindImage("14_leave.png", 0, 0 , x, y, 0.95)[0] != -1:
            break
          Delay(1)
          print("\r"+timeleft(), end='')
          gx, gy = FindImage("20_gold.png", 0, 0, x, y, 0.95)
          ogx, ogy = (11, 5)
          SaveImage("[debug]gold", gx+ogx, gy-ogy, gx+ogx+40, gy-ogy+17)
          try:
            cg = int(str(pytesseract.image_to_string(cv2.bitwise_not(cv2.imread("[debug]gold.png")),config='--psm 7 digit')))
          except:
            continue
          #if int(time.time()) - starttime < 60*9.5:
            #continue
          if True:
            if FindImage("20_gold.png", 0, 0, x, y, 0.95)[0] != -1:
              for i in range(0, len(item)):
                ix, iy = FindImage(item[i], 0, 0, x, 820, 0.97)
                if ix == -1 or iy >= 820 or iy <= 404:
                  continue
                else:
                  print(f'''{item[i].split("_")[1].split(".")[0]}@({ix},{iy}),''',end="",flush=True)
                  MoveMouse(ix+32, iy+32)
                  Delay(0.2)
                  MouseLDown()
                  Delay(0.2)
                  MoveMouse(x/2, 900)
                  Delay(0.2)
                  MouseLUp()
            gx, gy = FindImage("20_gold.png", 0, 0, x, y, 0.95)
            if gx != -1:
              ogx, ogy = (11, 5)
              SaveImage("[debug]gold", gx+ogx, gy-ogy, gx+ogx+40, gy-ogy+17)
              try:
                pg = int(str(pytesseract.image_to_string(cv2.bitwise_not(cv2.imread("[debug]gold.png")),config='--psm 7 digit')))
                print(f"pg{pg},", end="")
              except:
                continue
            if not appended:
              if is_wind is None:
                if FindImage(qiyana[0], 0, 0, x, y, 0.95)[0] != -1:
                  is_wind = True
                if is_wind is None:
                  for yy in range(0, len(qiyanas)):
                    if FindImage(qiyanas[yy], 0, 0, x, y, 0.95)[0] != -1:
                      is_wind = False
                      break
              if is_wind == True:
                units.append(qiyana)
                appended = True
              elif is_wind == False:
                units.append(khazix)
                appended = True
            print(f"(is_wind,{is_wind}),",end="",flush=True)
            for zz in range(0, len(units)):
              if units[zz][1] < 3:
                if ClickOnImage(units[zz][0], 0, 0, x, y, 0.95):
                  print(f'''{units[zz][0].split("_")[1].split(".")[0]},''',end="",flush=True)
                  units[zz][1] += 1
                  r = False
            gx, gy = FindImage("20_gold.png", 0, 0, x, y, 0.95)
            if gx != -1:
              ogx, ogy = (11, 5)
              SaveImage("[debug]gold", gx+ogx, gy-ogy, gx+ogx+40, gy-ogy+17)
              try:
                cg = int(str(pytesseract.image_to_string(cv2.bitwise_not(cv2.imread("[debug]gold.png")),config='--psm 7 digit')))
                print(f"cg{cg},", end="",flush=True)
              except:
                continue
              try:
                ohpx, ohpy = (0, 0)
                hpx, hpy = FindImage("15_hp_corner.png", ohpx, ohpy, x, y, 0.95)
                SaveImage("[debug]hp", ohpx+hpx+11, ohpy+hpy+3, ohpx+hpx+11+25, ohpy+hpy+3+20)
                hp = int(str(pytesseract.image_to_string(cv2.bitwise_not(cv2.imread("[debug]hp.png")),config='--psm 7 digit')))
                print(f"hp{hp},", end="",flush=True)
              except:
                continue
              if hp <= 40:
                ClickOnImage("20_r.png", 0, 0, x, y, 0.95)
                r = True
              else:
                if cg >= 55:
                  if not r:
                    ClickOnImage("20_f.png", 0, 0, x, y, 0.95)
                  else:
                    ClickOnImage("20_r.png", 0, 0, x, y, 0.95)
                  Delay(1)
                  MoveMouse(0, 0)
                r = True
              if r:
                print("r",flush=True)
              else:
                print("f",flush=True)
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
        ShowWindowByHWND(lolc_hwnd)
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
      SaveImage("[debug]client_accept_match_button", 0, 0, x, y)
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
      SaveImage("[debug]client_find_match_button", 0, 0, x, y)
      if not ClickOnImage("01_client_find_match_button.bmp", 0, 0, x, y, 0.95):
        count += 1
        continue
      MoveMouse(0, 0)
      status = "queueing"
      count = 0
      echo_status()
    Delay(1)
  except (KeyboardInterrupt, SystemExit):
    exit()
  except:
    traceback.print_exc()
    
