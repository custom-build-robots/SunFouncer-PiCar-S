#!/usr/bin/env python
# coding: latin-1
# Autor:	Ingmar Stapel
# Datum:	20171126
# Version:	1.0
# Homepage:	http://custom-build-robots.com
# Dieses Programm ist das sogenannte Steuerprogramm fuer das Roboter
# Auto PiCar-S von SunFounder ueber die Konsole und Tastatur vom PC 
# aus.
# Es verfügt auch ausgestattet mit zwei zusaetzlichen Ultraschall
# Sensoren ueber zwei autonom fahrende Modi. 
# - Beschleunigungsrennen (entlang einer Wand)
# - Vollautonomes Fahren (Labyrinth Modus)

# Hinweis: 
# Es muss noch das Modul readchar mit dem folgenden 
# Befehl installiert werden.
# Befehl: sudo pip install readchar

# Es werden verschiedene Python Klassen importiert deren Funktionen
# im Programm benoetigt werden fuer die Programmverarbeitung.
import sys, tty, termios, os, readchar, time

# Etwas Magie gehoert auch dazu ;-)
from threading import Thread
import threading

# Das Programm SunFounderMotorController.py wird als Modul geladen. 
# Es stellt die Funktionen fuer die Steuerun_threadg der H-Bruecke zur 
# Verfuegung.
import SunFounderPiCarS_motor_controller as MotorControl

# Import das Programm um die Ultraschall Sensoren anzusprechen
import ultrasonic as usonic

# Variable um den Thread zu beenden
global run_thread
run_thread = True

# Variablen Definition der Geschwindigkeit der Motoren des Roboter
# Autos.
global speed
speed = 0
global distanz_links
distanz_links = 0
global distanz_rechts
distanz_rechts = 0
global distanz_front
distanz_front = 0
	
# Variablen Definition des Lenkwinkels des Lenk-Servo Motors.
# Die neutrale Stellung war bei mit 530 erreicht. 
# Diese kann aber sehr sicher abweichen und hier muss ausprobiert 
# werden was zu Deinem Auto am besten passt.
global steering_value
steering_value = 350

global steering_value_initial
steering_value_initial = 350

# Hier werden die maximal und minimal Lenkeinschlaege festgelegt.
global steering_value_max
steering_value_max = 460
global steering_value_min
steering_value_min = 250

# letzte Lenkrichtung
letzte_lenkrichtung = ""

# Die Funktion getch() nimmt die Tastatureingabe des Anwenders
# entgegen. Die gedrueckten Buchstaben werden eingelesen. Sie werden
# benoetigt um die Richtung und Geschwindigkeit des Roboter-Autos
# festlegen zu koennen.
def getch():
	ch = readchar.readchar()
	return ch

# Die Funktion printscreen() gibt immer das aktuelle Menue aus
# sowie weitere Statusinformationen.
# Der Aufruf ist noch nicht schoen geloesst.
def printscreen():
	global speed
	global steering_value
	global distanz_links
	global distanz_rechts
	global distanz_front
	
	# der Befehl os.system('clear') leert den Bildschirmihalt vor
	# jeder Aktualisierun_threadg der Anzeige. So bleibt das Menue stehen
	# und die Bildschirmanzeige im Terminal Fenster steht still.
	os.system('clear')
	
	print("w/s: beschleunigen")
	print("a/d: lenken")
	print("b:   Beschleunigungsrennen")
	print("v:   Vollautonomes Fahren (VAF)")
	print("q:   stoppt die Motoren")
	print("x:   Programm beenden")
	print("================= Fahrzeuganzeige ================")
	print("Geschwindigkeit der Motoren:     "), speed
	print("Lenkeinschlag des Roboter Autos: "), steering_value
	print("Abstand links:                   "), distanz_links
	print("Abstand rechts:                  "), distanz_rechts
	print("Abstand front:                   "), distanz_front
	
# startet das VAF Programm
def start_vaf():
	global run_thread
	global speed
	global steering_value	
	global steering_value_initial	
	global distanz_links
	global distanz_rechts
	global distanz_front
	global steering_value_max
	global steering_value_min
	
	while run_thread:
		distanz_links = usonic.entfernung(19,26,"l")
		time.sleep(0.01)
		distanz_rechts = usonic.entfernung(16,12,"r")
		time.sleep(0.01)		
		distanz_front = usonic.sunfounder_get_distance(20)
		time.sleep(0.01)
		
		delta = distanz_links - distanz_rechts
		lenkung = delta / (distanz_links + distanz_rechts)

		if 3 <= distanz_front <= 8:
			speed = 0	
		elif 8 <= distanz_front <= 20:
			speed = 0.8
		elif 20 <= distanz_front <= 40:
			speed = 0.9
		else:
			speed = 1
		MotorControl.setMotorPower(speed)
	
		
		if -1 <= lenkung <= -0.3:		
			if distanz_front < 10:
				steering_value = steering_value + 50
			else:
				steering_value = steering_value + 10			
			if steering_value > steering_value_max:
				steering_value = steering_value_max
		elif 0.3 <= lenkung <= 1:
			if distanz_front < 10:
				steering_value = steering_value - 50
			else:		
				steering_value = steering_value - 10
			if steering_value < steering_value_min:
				steering_value = steering_value_min								
		else:
			steering_value = steering_value_initial

		MotorControl.setSteering(steering_value)

# startet das Beschleunigungsrennen Programm
def start_speed():
	global run_thread
	global speed
	global steering_value	
	global steering_value_initial	
	global distanz_links
	global distanz_rechts
	global distanz_front
	distanz = 0
	count = 0
	# 350 ist geradeauslauf.
	steering_speed_max = 370
	steering_speed_min = 330
	
	distanz_front = 0
	distanz_front = usonic.sunfounder_get_distance(20)
	while run_thread:
		distanz_sum = 0
		count += 1
		
		# Berechnet den Durchschnittsabstand von drei Messungen
		for i in range(1, 4):
			#distanz_links = usonic.entfernung(19,26,"l")
			distanz_rechts = usonic.entfernung(16,12,"r")
			
			distanz_sum += distanz_rechts
			time.sleep(0.01)		
		distanz = distanz_sum/3
		
		
		# Regelung der Geschwindigkeit fuer das Beschleunigungsrennen		
		if count >= 3:
			distanz_front = usonic.sunfounder_get_distance(20)
			count = 0
		if distanz_front < 25:
			speed = 0	
			t_start_speed.run_threadning = False
		else:
			speed = 1
	
		# Steuerung der Lenkung und haelt den eingestellten Abstand
		# zu der Wand.
		if 0 <= distanz <= 20:
			steering_value = steering_value - 5
			if steering_value < steering_speed_min:
				steering_value = steering_speed_min			
		elif 20 <= distanz <= 25:
			steering_value = steering_value_initial
		elif 25 <= distanz <= 300:
			steering_value = steering_value + 5		
			if steering_value > steering_speed_max:
				steering_value = steering_speed_max
		elif distanz > 1000:
			steering_value = steering_value_initial	
			speed = 0	
			
		MotorControl.setMotorPower(speed)
		MotorControl.setSteering(steering_value)

# Gibt das Menue das erste Mal aus.
printscreen()

# Diese Endlosschleife wird erst dann beendet wenn der Anwender 
# die Taste X tippt. Solange das Programm laeuft wird ueber diese
# Schleife die Eingabe der Tastatur eingelesen.
while True:

	# Mit dem Aufruf der Funktion getch() wird die Tastatureingabe 
	# des Anwenders eingelesen. Die Funktion getch() liesst den 
	# gedrueckte Buchstabe ein und uebergibt diesen an die 
	# Variablechar. So kann mit der Variable char weiter 
	# gearbeitet werden.
	char = getch()

	# Das Roboter-Auto faehrt vorwaerts wenn der Anwender die 
	# Taste "w" drueckt.
	if(char == "w"):
		# das Roboter-Auto beschleunigt in Schritten von 10% 
		# mit jedem Tastendruck des Buchstaben "w" bis maximal 
		# 100%. Dann faehrt es maximal schnell vorwaerts.
		speed = speed + 0.1

		if speed > 1:
			speed = 1

		# Dem Programm SunFounderMotorController.py welches zu beginn  
		# importiert wurde wird die Geschwindigkeit fuer 
		# die Motoren uebergeben.
		MotorControl.setMotorPower(speed)
		

	# Das Roboter-Auto faehrt rueckwaerts wenn die Taste "s" 
	# gedrueckt wird.
	if(char == "s"):
		# das Roboter-Auto bremst in Schritten von 10% 
		# mit jedem Tastendruck des Buchstaben "s" bis maximal 
		# -100%. Dann faehrt es maximal schnell rueckwaerts.
		speed = speed - 0.1

		if speed < -1:
			speed = -1
			
		# Dem Programm L298NMotorControl welches zu beginn  
		# importiert wurde wird die Geschwindigkeit fuer 
		# die linken und rechten Motoren uebergeben.		
		MotorControl.setMotorPower(speed)
		printscreen()

	 # mit dem druecken der Taste "q" werden die Motoren angehalten
	if(char == "q"):
		speed = 0
		run_thread = False
		try:
			t_start_vaf.run_threadning = False
			t_start_speed.run_threadning = False
		except:
			print("Unbekannter Fehler:", sys.exc_info()[0])
		MotorControl.setMotorPower(speed)
		# Dreht die Servo Motoren auf einen definierten
		# Ausgangszustand.	
		steering_value = steering_value_initial
		MotorControl.setSteering(steering_value)
		printscreen()

  
	# Mit der Taste "d" lenkt das Auto nach rechts. Dazu wird der
	# Servo Motor angesteuert.
	if(char == "d"):	
		if letzte_lenkrichtung != "d":
			letzte_lenkrichtung = "d"
			steering_value = steering_value_initial
			
		steering_value = steering_value + 10
		
		if steering_value > steering_value_max:
			steering_value = steering_value_max
		
		MotorControl.setSteering(steering_value)
		printscreen()
	
	# Mit der Taste "a" lenkt das Auto nach links bis die max/min
	# Geschwindigkeit der linken und rechten Motoren erreicht ist.
	if(char == "a"):
		if letzte_lenkrichtung != "a":
			letzte_lenkrichtung = "a"
			steering_value = steering_value_initial
			
		steering_value = steering_value - 10
			
		if steering_value < steering_value_min:
			steering_value = steering_value_min
		
		MotorControl.setSteering(steering_value)
		printscreen()

	# Startet das autonome Fahren fuer das Labyrinth
	if(char == "v"):
		run_thread = True
		t_start_vaf = Thread(target=start_vaf)
		t_start_vaf.start()

	# Startet das autonome Fahren fuer das Beschleunigungsrennen
	if(char == "b"):
		run_thread = True
		t_start_speed = Thread(target=start_speed)
		t_start_speed.start()
		
	# Mit der Taste "x" wird die Endlosschleife beendet 
	# und das Programm wird ebenfalls beendet. Zum Schluss wird 
	# noch die Funktion exit() aufgerufen die die Motoren stoppt.
	if(char == "x"):
		speed = 0
		run_thread = False
		try:
			t_start_vaf.run_threadning = False
			t_start_speed.run_threadning = False
		except:
			print("Unbekannter Fehler:", sys.exc_info()[0])	
		MotorControl.setMotorPower(speed)
		# Dreht die Servo Motoren auf einen definierten
		# Ausgangszustand beim Beenden des Programmes.
		steering_value = steering_value_initial
		MotorControl.setSteering(steering_value)
		MotorControl.exit()
		print("Program Ended")
		break
	
	# Die Variable char wird pro Schleifendurchlauf geleert. 
	# Das ist notwendig um weitere Eingaben sauber zu übernehmen.
	char = ""
	
# Ende des Programmes


