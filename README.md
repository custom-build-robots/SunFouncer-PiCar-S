# SunFounder-PiCar-S
Mit den beiden hier vorgestelltn Programmen kann das PiCar-S von SunFounder gesteuert werden. 
- Das Programm "SunFounderPiCarS_advanced_control.py" kapselt die Logik für die Lenkung und Beschleunigung des Autos. 
- Das Programm "SunFounderPiCarS_motor_controller.py" kapselt die Ansteuerung der beiden Antriebsmotoren über den TB6612 Motortreiber sowie die Lenkung des Autos mit dem Lenk-Servo.
- Mit dem Programm "SunFounderPiCarS_vaf_control.py" kann das Roboter Auto auch via Terminal Fenster ferngesteuert werden bzw. es koennen die beiden autonomen Modi gestartet werden für ein Beschleunigungsrennen bzw. der Labyrinth Modus.

Beide Programm müssen in einem Ordner auf dem Raspberry Pi liegen. Das Programm "SunFounderPiCarS_advanced_control.py" muss in der Konsole ausgeführt werden.
- SunFounderPiCarS_advanced_control.py
- SunFounderPiCarS_motor_controller.py
- SunFounderPiCarS_vaf_control.py


## Hinweis
Um das Programm "SunFounderPiCarS_vaf_control.py" sollten zwei zusätzliche Ultraschall Sensoren am PiCar-S angebracht werden. Das folgende Bild zeigt die Modifukation an dem Roboter Bausatz von SunFounder.

![Raspberry Pi robot - PiCar-S](https://custom-build-robots.com/wp-content/uploads/2017/11/SunFounder_PiCar-S_ultrasonic_sensor_02-768x432.jpg)

Mehr über das SunFounder PiCar-S gibt es auf meinem Blog zu erfahren: https://custom-build-robots.com/bausatz/sunfounder-roboter-auto-picar-s-bausatz-verkabelung-und-softwareinstallation/9352
