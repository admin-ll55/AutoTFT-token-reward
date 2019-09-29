import ctypes
import os
import time
while True:
  f = open("AutoTFT.log", 'r')
  t = f.readlines()[-1]
  f.close()
  ctypes.windll.kernel32.SetConsoleTitleW(t)
  time.sleep(1/3)
