import pygame 
from pygame.locals import *
import numpy as np 
import time,sys,io,random,os,getpass,winsound
from datetime import datetime



basePath=os.getenv('APPDATA')+"\\CONWAY_FILES\\"
formato=".txt"
print(basePath)
if not os.path.exists(basePath):
    os.mkdir(basePath)



__Version__="1.21.5"
__Authors__=["Nadie"]



icon = pygame.image.load("game3.png")
pygame.display.set_icon(icon)

pygame.display.set_caption("Conway's Game of Life")

gameOver=False

mode=int(1)
rainbow_mode=False
rainbow_color=(255,0,0)

boolgrid=True
boolinfo=True

sum_generation=0
Generation=0

list_generation=[]
pygame.init()


grid_width, grid_height = 750, 750


width, height = 950, 750
screen = pygame.display.set_mode((width,height), pygame.RESIZABLE)

black=0,0,0
white=255,255,255
grey=128,128,128

bg= black
bg_cube=white


screen.fill(bg)

nxC, nyC=100, 100

dimCW=grid_width/nxC
dimCH=grid_height/nyC

gameState=np.zeros((nxC,nyC))

fontx, fonty= width*0.8421, 25

globali=1
while os.path.isfile(basePath+str(globali)):
	globali+=1

"""
gameState[5,3]=1
gameState[5,4]=1
gameState[5,5]=1
"""
def update_globals():
	global width, height
	global grid_width, grid_height
	global dimCW, dimCH
	global fontx, fonty

	width,height= screen.get_size() 
	grid_width, grid_height= width*79//100,height
	dimCW=grid_width/nxC
	dimCH=grid_height/nyC
	fontx, fonty= width*84//100,25


def pause():
	global pauseExect
	pauseExect= not pauseExect

def chancemode(chance=1):
	global mode
	global bg,bg_cube
	global rainbow_mode
	if chance==1:
		if mode<4:
			mode+=1
		else:
			mode=1
	else:
		if mode<4:
			mode+=1
		else:
			mode=1
	if mode==1:
		bg=black
		bg_cube=white
		rainbow_mode=0
	elif mode==2:
		bg=white
		bg_cube=black
		rainbow_mode=0
	elif mode==3:
		bg=black
		bg_cube=white
		rainbow_mode=1
	elif mode==4:
		bg=white
		bg_cube=black
		rainbow_mode=1


def save():
	result_list=[]
	for y in range(0, nxC):
		for x in range(0, nyC):
			if gameState[x,y]==1:
				result_list.append((x,y))

	return result_list

def save_file():
	global globali
	
	if not os.path.isfile(basePath+str(str(globali)+formato)):
		RbL=save()
		RbS=""
		for i in RbL:
			RbS=RbS+str(i)
		file=io.open(basePath+str(globali)+formato,"w")
		file.write(RbS)
		file.close()
		globali=1
	else:
		globali+=1 
		save_file()



def insert(file):
	f=list(io.open(file,"r").read())
	return f
	
print(insert(basePath+"1"+formato), type(insert(basePath+"1"+formato)))


def show_generation():
	print(Generation)

def reset():
	global Generation
	global pauseExect
	pE=pauseExect
	pauseExect=True
	Generation= 0
	for y in range(0, nxC):
		for x in range(0, nyC):
			newGameState[x,y]=0
	pauseExect=pE

def next_poblation():
	global gameState
	global newGameState
	global sum_generation
	global Generation

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
	if sum_generation!=0 and pauseExect:
		Generation+=1



pauseExect = False


while not gameOver:
	if screen.get_size() != (width,height):
		update_globals()

	if rainbow_mode and not pauseExect:
		rainbow_color=(random.randint(0,255),random.randint(0,255),random.randint(0,255))

	if boolinfo:	
	
		fuente = pygame.font.SysFont("Small Fonts Normal", int(width*0.026315))
		mensaje= fuente.render("Grid: {}x{}".format(nxC,nyC), 1, bg_cube)
		screen.blit(mensaje, (fontx, fonty*1))
	
		mensaje= fuente.render("Generation: "+str(Generation), 1, bg_cube)
		screen.blit(mensaje, (fontx, fonty*2))

		mensaje= fuente.render("Poblation: "+str(round(sum_generation)), 1, bg_cube)
		screen.blit(mensaje, (fontx, fonty*3))
		if pauseExect:
			pygame.draw.polygon(screen,(255,0,0), [(fontx,fonty*5),(fontx,fonty*5+20),(fontx+15,fonty*5+10)] ,0)
		else:
			pygame.draw.polygon(screen,bg_cube, [(fontx,fonty*5),(fontx,fonty*5+20),(fontx+5,fonty*5+20),(fontx+5,fonty*5)] ,0)
			pygame.draw.polygon(screen,bg_cube, [(fontx+10,fonty*5),(fontx+10,fonty*5+20),(fontx+5+10,fonty*5+20),(fontx+5+10,fonty*5)] ,0)


		
	else:
		
		fuente = pygame.font.Font("emulogic.ttf", int(width*0.010526))
		mensaje= fuente.render("Created by", 1, bg_cube)
		screen.blit(mensaje, (fontx-10, fonty*1))
		for i in range(len(__Authors__)):
	
			mensaje= fuente.render(__Authors__[i], 1, rainbow_color if rainbow_mode else bg_cube)
			screen.blit(mensaje, (fontx-10, fonty*(i+2)))
			t=i

		mensaje= fuente.render("Version: {}".format(__Version__), 1, bg_cube)
		screen.blit(mensaje, (fontx-10, fonty*(t+3)))

	pygame.display.flip()



	newGameState=np.copy(gameState)

	screen.fill(bg)
	time.sleep(0.001)

	
	for event in pygame.event.get():
		keys_pressed = pygame.key.get_pressed()
		if event.type == pygame.QUIT:
			sys.exit()
		if  event.type ==pygame.KEYDOWN:

			if event.key ==pygame.K_UP:
				r_l=save()
				if nxC>=20:
					nxC-=10
					nyC-=10
					dimCW=grid_width/nxC
					dimCH=grid_height/nyC
					newGameState=np.zeros((nxC,nyC))
					for i in r_l:
						try:
							newGameState[i[0],i[1]]=1
						except:pass
					#gameState=np.zeros((nxC,nyC))
			if event.key ==pygame.K_DOWN:
				r_l=save()
				if nxC<=110:
					nxC+=10
					nyC+=10
					dimCW=grid_width/nxC
					dimCH=grid_height/nyC
					newGameState=np.zeros((nxC,nyC))
					gameState=np.zeros((nxC,nyC))
					for i in r_l:
						try:
							newGameState[i[0],i[1]]=1
						except:pass

			if event.key==pygame.K_s:
				save_file()
			if event.key==pygame.K_m:
				chancemode()
			if event.key==pygame.K_k:
				pause()
			if event.key==pygame.K_r:
				reset()
			if event.key==pygame.K_g:
				boolgrid= not boolgrid 
			if event.key==pygame.K_i:
				boolinfo= not boolinfo
			if event.key==pygame.K_z:
				pass
				
			if event.key==pygame.K_n and pauseExect:

					next_poblation()


		
		mouseClick=pygame.mouse.get_pressed()
		posX, posY= pygame.mouse.get_pos()		
		if sum(mouseClick)>0:
			
			celX, celY= int(np.floor(posX/dimCW)), int(np.floor(posY/dimCH))
			try:
				newGameState[celX,celY]= not mouseClick[2]
			except: 
								
				if 770<posX<=780 and 50<posY<=60 and pauseExect:
					next_poblation()

				if fontx-5<posX<fontx+20 and fonty*5-5<posY<fonty*5+25:
					pauseExect= not pauseExect



	for y in range(0, nxC):
		for x in range(0, nyC):
			posX, posY= pygame.mouse.get_pos()
			celX, celY= int(np.floor(posX/dimCW)), int(np.floor(posY/dimCH))
			n_neigh=gameState[(x - 1) % nxC, (y - 1) % nyC] + \
						gameState[(x)	 % nxC, (y - 1) % nyC] + \
						gameState[(x + 1) % nxC, (y - 1) % nyC] + \
						gameState[(x - 1) % nxC, (y)	% nyC] + \
						gameState[(x + 1) % nxC, (y) 	% nyC] + \
						gameState[(x - 1) % nxC, (y + 1) % nyC] + \
						gameState[(x)	 % nxC, (y + 1) % nyC] + \
						gameState[(x + 1) % nxC, (y + 1) % nyC]


			if not pauseExect:
			   #if gameState[x,y]==0 and n_neigh==3:
				if gameState[x,y]==0 and n_neigh==3:
					newGameState[x,y]=1
					

			   #elif gameState[x,y]==1 and (n_neigh<2 or n_neigh>3):
				elif gameState[x,y]==1 and (n_neigh<2 or n_neigh>3):
					newGameState[x,y] = 0

			else: 
				pass




			poly=[((x) * dimCW, y * dimCH),
					((x+1) * dimCW, y * dimCH),
					((x+1) * dimCW, (y+1) * dimCH),
					((x) * dimCW, (y+1) * dimCH)]

			
			if newGameState[x,y]== 0:
				if boolgrid and x!=celX and y!=celY:
					pygame.draw.polygon(screen,bg_cube, poly ,1)

				elif boolgrid and (x==celX or y==celY):
					pygame.draw.polygon(screen,grey, poly ,0)
					pygame.draw.polygon(screen,bg_cube, poly ,1)
					
				
			elif newGameState[x,y]== 1:
				if rainbow_mode:
					if boolgrid:
						pygame.draw.polygon(screen,rainbow_color, poly ,0)
						pygame.draw.polygon(screen,bg_cube, poly ,1)
					else:
						pygame.draw.polygon(screen,rainbow_color, poly ,0)
						pygame.draw.polygon(screen,bg_cube, poly ,1)
				else:
					if boolgrid:
						pygame.draw.polygon(screen,bg_cube, poly ,0)
					else:
						pygame.draw.polygon(screen,grey, poly ,0)
						pygame.draw.polygon(screen,bg_cube, poly ,1)

	
	before_list_generation=list_generation
	list_generation=save()
	before_sum_generation=sum_generation
	sum_generation=0

	if not boolgrid:
		pygame.draw.lines (screen, bg_cube, False,  [(grid_width, 0),(grid_width,grid_height)], 2)
	for y in range(0, nxC):
		for x in range(0, nyC):
			sum_generation+=newGameState[x,y]


	if sum_generation>0 and not pauseExect and before_list_generation!=list_generation:
		Generation+=1
	elif sum_generation>0 and before_sum_generation==0:
		Generation=0

	gameState =np.copy(newGameState)
	

	pygame.display.flip()
