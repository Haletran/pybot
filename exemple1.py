from pybot import Robot
robot = Robot()

robot.changer_titre("hello,pybot!")
robot.allumer_ecran()
robot.dessiner_ecran()
robot.dort(1)
robot.changer_titre("fullscreen in 1 second")
robot.dessiner_ecran()
robot.dort(1)
robot.plein_ecran(True)
robot.dessiner_ecran()
robot.dort(1)
robot.changer_titre("bye in 1 second")
robot.plein_ecran(False)
robot.dessiner_ecran()
robot.dort(1)
robot.eteindre_ecran()
