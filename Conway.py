import pygame 
from pygame.locals import *
import numpy as np 
import time
import sys
import random
import pickle

gameOver=False

boolcuadricula=True
boolinfo=False

sum_generation=0
__generation__=0

pygame.init()

width, height = 750, 750
screen = pygame.display.set_mode((height, width))

negro=0,0,0
blanco=255,255,255
gris=128,128,128
azul= 0,100,150
amarillo=255, 233, 0

bg= negro
bg_cubo=blanco
bg_cuadricula=gris

screen.fill(bg)

nxC, nyC=100, 100

dimCW=width/nxC
dimCH=height/nyC

gameState=np.zeros((nxC,nyC))

#automata palo
"""
gameState[5,3]=1
gameState[5,4]=1
gameState[5,5]=1
"""



def save():
	result_list=[]
	for y in range(0, nxC):
		for x in range(0, nyC):
			if gameState[x,y]==1:
				result_list.append((x,y))

	return result_list


def show_generation():
	print(__generation__)

def clear():
	global __generation__
	__generation__= 0
	for y in range(0, nxC):
		for x in range(0, nyC):
			newGameState[x,y]=0

def next_poblation():
	global gameState
	global newGameState
	global sum_generation

	sum_generation=0
	for y in range(0, nxC):
		for x in range(0, nyC):
			
			n_neigh=gameState[(x - 1) % nxC, (y - 1) % nyC] + \
					gameState[(x)	 % nxC, (y - 1) % nyC] + \
					gameState[(x + 1) % nxC, (y - 1) % nyC] + \
					gameState[(x - 1) % nxC, (y)	% nyC] + \
					gameState[(x + 1) % nxC, (y) 	% nyC] + \
					gameState[(x - 1) % nxC, (y + 1) % nyC] + \
					gameState[(x)	 % nxC, (y + 1) % nyC] + \
					gameState[(x + 1) % nxC, (y + 1) % nyC]


			if gameState[x,y]==0 and n_neigh==3:
				newGameState[x,y]=1

			elif gameState[x,y]==1 and (n_neigh<2 or n_neigh>3):
				newGameState[x,y] = 0

			sum_generation+=newGameState[x,y]

	gameState =np.copy(newGameState)
	if sum_generation!=0 and not pauseExect:
		__generation__+=1



pauseExect= False

while not gameOver:
	if boolinfo:
		fuente = pygame.font.SysFont("Terminal", 50)
		mensaje= fuente.render("Generation: "+str(__generation__), 1, amarillo)
		screen.blit(mensaje, (width-250-(len(str(__generation__))*20), height-50))
		pygame.display.flip()

	newGameState=np.copy(gameState)

	screen.fill(bg)

	time.sleep(0.1)

	

	for event in pygame.event.get():
		keys_pressed= pygame.key.get_pressed()
		if event.type == pygame.QUIT:
			sys.exit()
		if  event.type ==pygame.KEYDOWN:

			if event.key ==pygame.K_UP:
				r_l=save()
				if nxC>=20:
					nxC-=10
					nyC-=10
					dimCW=width/nxC
					dimCH=height/nyC
					newGameState=np.zeros((nxC,nyC))
					for i in r_l:
						try:
							newGameState[i[0],i[1]]=1
						except:pass
					#gameState=np.zeros((nxC,nyC))
			if event.key ==pygame.K_DOWN:
				r_l=save()
				if nxC<=130:
					nxC+=10
					nyC+=10
					dimCW=width/nxC
					dimCH=height/nyC
					newGameState=np.zeros((nxC,nyC))
					gameState=np.zeros((nxC,nyC))
					for i in r_l:
						try:
							newGameState[i[0],i[1]]=1
						except:pass
			if event.key==pygame.K_m:
				if bg==negro:
					bg=blanco
					bg_cubo=negro
					bg_cuadricula=azul
				else:
					bg=negro
					bg_cubo=blanco
					bg_cuadricula=gris
			if event.key==pygame.K_k:
				pauseExect= not pauseExect
			if event.key==pygame.K_c:
				clear()
			if event.key==pygame.K_g:
				boolcuadricula= not boolcuadricula 
			if event.key==pygame.K_s:
				#save()
				show_generation()
			if event.key==pygame.K_n and pauseExect:
					next_poblation()
			if event.key==pygame.K_i:
				boolinfo= not boolinfo
		mouseClick=pygame.mouse.get_pressed()
		if sum(mouseClick)>0:
			posX, posY= pygame.mouse.get_pos()

			celX, celY= int(np.floor(posX/dimCW)), int(np.floor(posY/dimCH))
			newGameState[celX,celY]= not mouseClick[2]

	for y in range(0, nxC):
		for x in range(0, nyC):

			if not pauseExect:
				n_neigh=gameState[(x - 1) % nxC, (y - 1) % nyC] + \
						gameState[(x)	 % nxC, (y - 1) % nyC] + \
						gameState[(x + 1) % nxC, (y - 1) % nyC] + \
						gameState[(x - 1) % nxC, (y)	% nyC] + \
						gameState[(x + 1) % nxC, (y) 	% nyC] + \
						gameState[(x - 1) % nxC, (y + 1) % nyC] + \
						gameState[(x)	 % nxC, (y + 1) % nyC] + \
						gameState[(x + 1) % nxC, (y + 1) % nyC]

				if gameState[x,y]==0 and n_neigh==3:
					newGameState[x,y]=1

				elif gameState[x,y]==1 and (n_neigh<2 or n_neigh>3):
					newGameState[x,y] = 0

			poly=[((x) * dimCW, y * dimCH),
					((x+1) * dimCW, y * dimCH),
					((x+1) * dimCW, (y+1) * dimCH),
					((x) * dimCW, (y+1) * dimCH)]

			if newGameState[x,y]== 0 and boolcuadricula:
				pygame.draw.polygon(screen,bg_cuadricula, poly ,1)
			elif newGameState[x,y]== 1:
				pygame.draw.polygon(screen,bg_cubo, poly ,0)


	sum_generation=0
	for y in range(0, nxC):
		for x in range(0, nyC):
			sum_generation+=newGameState[x,y]

	if sum_generation!=0 and not pauseExect:
		__generation__+=1
	elif sum_generation==0:
		__generation__=0
	gameState =np.copy(newGameState)
	

	pygame.display.flip()