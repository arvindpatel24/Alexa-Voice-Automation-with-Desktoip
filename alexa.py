import os
import subprocess
import time 
import playsound
import pyautogui
import ctypes
import speech_recognition as sr
from gtts import gTTS
from datetime import datetime


i,j=1,0
pyautogui.FAILSAFE = True

def speak(text):
	global i
	i=i+1
	tts = gTTS(text=text,lang="en")
	filename = "voice"+str(i)+".mp3"
	tts.save(filename)
	playsound.playsound(filename)

def get_audio():
	r = sr.Recognizer()
	with sr.Microphone() as source:
		audio = r.listen(source)
		said = ""

		try:
			said = r.recognize_google(audio)
			print(said)
		except Exception as e:
			print("Exception: " + str(e))
	return said.lower()
def today_datetime():
	today = datetime.today()
	day,month,year,hour,minute = today.day,today.month,today.year,today.hour,today.minute
	months = ['January','Fabruary','March','April','May','June','July','August','September','October','November','December']
	if hour<12 or hour == 24 :
		mode = "A M"
	else:
		hour = hour - 12
		mode = "P M"

	day_text = "Today's date is " + months[month-1] +" "+ str(day) + " " + str(year) + " and time is " + str(hour) + " hour " + str(minute) + " minute " + mode
	speak(day_text)

def close_win():
	x,y = pyautogui.position()
	pyautogui.click(1340,5)      #Cross
	pyautogui.moveTo(x,y)

def note(text):
	date=datetime.now().date()
	file_name = str(date).replace(":","-") + "_note.txt"
	with open(file_name,"w") as f:
		f.write(text)
	f.close()
	subprocess.run(["notepad.exe",file_name],shell=True)
	#time.sleep(5)
	x,y = pyautogui.position()
	pyautogui.click(785,155)      #Cross
	pyautogui.moveTo(x,y)
	return
def square(x,y,size):
	subprocess.run("start mspaint.exe",shell=True)
	time.sleep(2)
	pyautogui.moveTo(x-(size//2),y-(size//2))
	pyautogui.dragRel(size,0,duration=0.5)
	pyautogui.dragRel(0,size,duration=0.5)
	pyautogui.dragRel(-size,0,duration=0.5)
	pyautogui.dragRel(0,-size,duration=0.5)



def main():
	start = "alexa"
	main_path = os.getcwd()
	path,arg="",""
	while(True):
		print("Listening")
		text = get_audio()
		if text.count(start)>0 :
			if "welcome" in text :
				speak("Thank You so much Sir. Its my pleasure to work with you.")
			elif "date" in text :
				today_datetime()
			elif "open" in text:
				if "file explorer" in text:
					subprocess.run("start explorer",shell=True)
				elif "last image" in text:
					os.chdir(path)
					li=os.listdir()
					path = path + li[-1]
					os.chdir(main_path)
					arg="start " + path
					os.system(arg)
				elif "camera" in text:
					subprocess.run('start microsoft.windows.camera:', shell=True)
					time.sleep(5)
					x,y = pyautogui.position()
					pyautogui.click(1330,400)
					pyautogui.moveTo(x,y)

				if ("paint" in text) or ("draw" in text) :
					x,y = pyautogui.size()
					x,y = x//2,y//2
					li = text.split()
					rad = int(li[-1])
					square(x,y,rad)
			elif "close" in text:
				if "paint" in text :
					x,y = pyautogui.position()
					pyautogui.click(1340,5)
					time.sleep(1)      
					pyautogui.click(715,390)
					pyautogui.moveTo(x,y)

				else:
					close_win()
			
			elif "go" in text:
				if "sleep" in text :
					speak("Thank You for choosing me chodu!!! Also your pikachu is too fast  and Electrifying. Hope we meet again.")
					playsound.playsound("pika.mp3")
					#os.system("shutdown /s /t 1")
					break
				elif "drive" in text :
					li = text.split()
					path = li[-2] + ":/"
					print(path)
					close_win()
					arg="start " + path
					os.system(arg)
				elif "back" in text :
					go_back();
				elif "desktop" in text :
					pyautogui.hotkey('win','d')
				else:
					li = text.split()
					path = path + li[-1]+ "/"
					close_win()
					arg="start " + path
					os.system(arg)

			elif ("screenshot" in text) or "take" in text :
				print("Screenshot taken.")
				pyautogui.hotkey('win','prntscrn')
					
			elif "tell" in text:
				if "current" in text:
					os.chdir(path)
					st=os.getcwd().replace('\\','  ')
					os.chdir(main_path)
					speak(st)
				elif ("files" in text) or ("location" in text):
					os.chdir(path)
					li=os.listdir()
					li=li[1:]
					st = ' '.join(li)
					os.chdir(main_path)
					speak(st)
			elif ("note" in text) or ("down") in text :
				speak("Okay Sir, I am ready to Note ")
				note_text = get_audio()
				note(note_text)
			elif ("wallpaper" in text) or ("change" in text):
				global j
				j=j+1
				path = "C:\\Users\\Ravi\\Desktop\\2020 Projects\\Project3_Alexa\\"+str(j)+".jpg"
				ctypes.windll.user32.SystemParametersInfoW(20, 0, path , 0)




		else :
			playsound.playsound("not_recognize.mp3")

	print("THE END")
	pyautogui.hotkey('ctrl','s')

if __name__ == '__main__':
	main()

