############ Jiawen Cao's program
############ June,2015
############ Avidda
############ It is a mock 3D game
############ Arrow left and right will help you to turn triangle left or right
############ pick up every square in the game and DONT MISS it
############ if you miss three the game is OVER!
############ ENJOY!
############ Sound file is too large so thait it is not included. Sep.19,2016
import random
import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *
from math import sqrt
import math
import sys


########################## Triangle ############################
class Triangle:

    def __init__(self,z):
        self.z = z
        self.verticies = [
    [0, sqrt(3)-sqrt(3)/3, self.z],
    [-1, sqrt(3)/-3, self.z],
    [1, sqrt(3)/-3, self.z]]

        self.edges = (
    (0,1),
    (1,2),
    (2,0))

    def move(self, speed):
        self.z = self.z+speed
        for i in range(0, len(self.verticies)):
            self.verticies[i][2] = self.z                       
#draw in triangle
    def draw(self):
        glBegin(GL_LINES)
        for edge in self.edges:
            for vertex in edge:
                # connect points
                #color of the triangle's line
                glColor3fv((1,1,1))
                glVertex3fv(self.verticies[vertex])
        glEnd()
 
################################ Square ###############################
class Square:
    def __init__(self,z, turnOffset):
        self.z = z
        #randomly pick which square is going to appear next
        self.a=random.randint(0,2)

        if self.a==0:
            self.verticies = [
        [-0.25,-0.58 ,z],
        [0.25,-0.58,z],
        [0.25,-.08,z],
        [-0.25,-.08,z]]

        elif self.a==1:
            self.verticies = [
        [0.627, 0.0735 , z],
        [0.377, 0.507, z],
        [-0.0557,0.257,z],
        [0.194, -0.177, z]]
        

        else:
            self.verticies = [
        [-0.377, 0.507 , z],
        [-0.627, 0.0735, z],
        [-0.194,-0.177, z],
        [0.0557, 0.257, z]]

        self.a = self.a + turnOffset
        self.a = self.a % 3

            


        self.edges = (
    (0,1),
    (1,2),
    (2,3),
    (3,0))

        self.surface=(0,1,2,3)


        
    def move(self, speed):
        self.z = self.z+speed
        for i in range(0, len(self.verticies)):
            self.verticies[i][2] = self.z                       


#draw in square
    def draw(self):
        global font

        glBegin(GL_QUADS)
        for vertex in self.surface:
            #color of the squares
            glColor3fv((0,1,0))
            glVertex3fv(self.verticies[vertex])
        glEnd()
        
        glBegin(GL_LINES)
        for edge in self.edges:
            for vertex in edge:
                # connect points
                glVertex3fv(self.verticies[vertex])
        glEnd()
    

########################## variables ##################################

times=0
life=3
turnRight = -1
turnLeft = -1
countTurns = 0
#ratio of the screen
display = (600,600)
#background music
pygame.mixer.init()
pygame.mixer.music.load("music.wav")
pygame.mixer.music.play()
speed=1.0



#############################main program#################################    
def main():
    global times, turnRight, turnLeft,life, countTurns,speed
    points = 0
    pygame.init()
    #display
    pygame.display.set_mode(display, DOUBLEBUF|OPENGL)
    pygame.display.set_caption("points: "+ str(points))
    #how much the user can see
    gluPerspective(45, (display[0]/display[1]), 0.1, 150.0)

    #list of triangles
    triangles = []
    #original position
    triangles.append(Triangle(-75))
    triangles.append(Triangle(-150))
    s=Square(-75,countTurns)
    while True:
        #to make the triangle to display again
        for t in triangles:
            if t.z > 0:
                t.z = -150
                #make the square to come more quickly than before
                if speed<10:
                    speed=speed+0.5
        
        for event in pygame.event.get():
            #user moves the triangle
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT and turnRight < 0:
                    turnRight = 0
                    s.a = s.a-1
                    countTurns=countTurns-1
                    if s.a < 0:
                        s.a = 2
                elif event.key == pygame.K_LEFT and turnLeft < 0:
                    turnLeft = 0
                    s.a = s.a+1
                    countTurns = countTurns+1
                    if s.a > 2:
                        s.a= 0
                elif event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()

            #to rotate triangle by degree
        if turnRight > -1 and turnRight < 120:
            glRotated(-10,0, 0, 1)
            turnRight = turnRight + 10
        else:
            turnRight = -1
            
        if turnLeft > -1 and turnLeft < 120:
            glRotated(10,0, 0, 1)
            turnLeft = turnLeft + 10
        else:
            turnLeft = -1
        #when player pick up item in the right way, points increase
        if s.z>0 and s.a ==0:
            points=points+100
            pygame.display.set_caption("points: "+str(points))
        elif s.z > 0 and (s.a==1 or s.a==2):
            life=life-1
            print "life:"+ str(life)
        #set square back to the original position
        if s.z > 0:
            s = Square(-150, countTurns)
            
        #when the player loses
        if life==0:
            print "Sorry, you lose and you get "+ str(points)
            pygame.quit()
            sys.exit()
            
            
                    
        
        #clear the screen
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

        # make the triangle and the square move
        for t in triangles:
            t.move(1)
        s.move(speed)
        # draw
        for t in triangles:
            t.draw()
        s.draw()
        #refresh
        pygame.display.flip()
        pygame.time.wait(50)
        times = times+1



main()
