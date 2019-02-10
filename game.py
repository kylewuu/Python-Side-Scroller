import pygame
import time

pygame.init()
screen_width=1200
screen_height=700
win = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("asdf")

class Bike:
	"""This is to store the different moving pieces of the bike. The body is the whole thing, while the front and the back wheels move. All the wheels are relative to the body of the bike"""
	def __init__(self, body_x, body_y, front_wheel_x,front_wheel_y, back_wheel_x,back_wheel_y):
		self.body_x=body_x
		self.body_y=body_y
		self.front_wheel_y=front_wheel_x
		self.front_wheel_x=front_wheel_y
		self.back_wheel_x=back_wheel_x
		self.back_wheel_y=back_wheel_y
	def tire_position_update(self):
		self.back_wheel_x=self.body_x+38 #loading front wheel
		self.back_wheel_y=self.body_y+105
		self.front_wheel_x=self.body_x+111 #loading back wheel
		self.front_wheel_y=self.body_y+40

#initiatlizing
bike=Bike(10, 450,1,1,1,1) #where the pieces first load
tile_x=150
tile_y=540
tire_diameter=45
width= 80
height= 40
velocity=0
rect_colour= (255,0,0)
left=False
right=True
walkCount=0
clock=pygame.time.Clock()
isJump=False
jumpcount=7
acceleration= 1
decceleration=1
backacceleration=0.5
max_velocity=15
no_forward= False
no_backward= False #for collisions on side of crates
quadrant=1
tile_length=60
gravity=1
bike.tire_position_update()
default_land=bike.back_wheel_y+tire_diameter


#images loading
moveleft=[pygame.transform.rotate(pygame.transform.scale(pygame.image.load('offroad/body.png'),(140,80)),35), pygame.transform.rotate(pygame.transform.scale(pygame.image.load('offroad/body.png'),(140,80)),35)]
#moveright=[pygame.transform.flip(pygame.transform.scale(pygame.image.load('offroad/body.png'),(300,180)), True, False),pygame.transform.flip(pygame.transform.scale(pygame.image.load('offroad/body.png'),(300,180)), True, False)] **no need for this anymore as you can't move left
backwheel_img=[pygame.transform.scale(pygame.image.load('offroad/tire.png'),(tire_diameter,tire_diameter)), pygame.transform.scale(pygame.transform.rotate(pygame.image.load('offroad/tire.png'),(90)),(tire_diameter,tire_diameter))]
frontwheel_img=[pygame.transform.scale(pygame.image.load('offroad/tire.png'),(tire_diameter,tire_diameter)), pygame.transform.scale(pygame.transform.rotate(pygame.image.load('offroad/tire.png'),(90)),(tire_diameter,tire_diameter))]
background= pygame.image.load('bg.png')

#tiles
tiles=pygame.transform.scale(pygame.image.load('tiles/Crate.png'), (tile_length,tile_length))
tiles_array=[]


#functions
def redrawgamewindow():
	global walkCount #for having an animation when moving

	win.blit(background, (0,0))
	if walkCount >1:
		walkCount= 0

	if left:
		win.blit(moveleft[walkCount],(bike.body_x,bike.body_y))
		walkCount+=1

	elif right:
		win.blit(moveleft[walkCount],(bike.body_x,bike.body_y))
		walkCount+=1


	bike.tire_position_update()
	win.blit(frontwheel_img[1],(bike.front_wheel_x,bike.front_wheel_y))
	win.blit(backwheel_img[0],(bike.back_wheel_x,bike.back_wheel_y))

	#tiles drawing
	win.blit(tiles,(tile_x, tile_y))

	pygame.display.update()

#main loop to run the game
while(True):
	redrawgamewindow()
	clock.tick(60)
	for event in pygame.event.get():
		if event.type==pygame.QUIT:
			pygame.quit()

	keys= pygame.key.get_pressed()

	#collision walls
	tire_left_collide=bike.back_wheel_x
	tire_right_collide=bike.back_wheel_x+tire_diameter
	tire_bottom_collide=bike.back_wheel_y+tire_diameter

	#for when you're actually pressing the keys
	if quadrant==1:
		if keys[pygame.K_w] and bike.body_x<=(screen_width-width) and velocity<=max_velocity and no_forward==False and tire_right_collide<tile_x:
			bike.body_x+=acceleration

		elif keys[pygame.K_s] and bike.body_x>=0 and velocity<=max_velocity:
			bike.body_x-=decceleration

		elif tire_right_collide>=tile_x:
			no_forward=True

		elif tire_right_collide<tile_x:
			no_forward=False

		#jumping
		if not(isJump):
			if keys[pygame.K_SPACE]:
				isJump= True
		else:
			if tire_bottom_collide>default_land:
				isJump=False

			if jumpcount >= -7 and isJump==True:
				neg= 1
				if jumpcount<0:
					neg=-1
				bike.body_y-= (jumpcount**2)*0.5*neg
				jumpcount-=1

			else:
				isJump=False
				jumpcount=77

	elif quadrant==2:
		if keys[pygame.K_w] and bike.body_x<=(screen_width-width) and velocity<=max_velocity:
			bike.body_x+=acceleration

		elif keys[pygame.K_w] and bike.body_x>=0 and velocity<=max_velocity and no_forward== False:
			bike.body_x-=decceleration

		#jumping
		if not(isJump):
			if keys[pygame.K_SPACE]:
				isJump= True
		else:
			if tire_bottom_collide>default_land:
				isJump=False

			if jumpcount >= -7 and isJump==True:
				neg= 1
				if jumpcount<0:
					neg=-1
				bike.body_y-= (jumpcount**2)*0.5*neg
				jumpcount-=1

			else:
				isJump=False
				jumpcount=7


	elif quadrant==3:#quadrant 3 needs a lot of work
		if keys[pygame.K_w] and bike.body_x<=(screen_width-width) and velocity<=max_velocity:
			velocity+=acceleration

		elif keys[pygame.K_w] and bike.body_x>=0 and velocity<=max_velocity:
			velocity-=decceleration

		#jumping
		if not(isJump):
			if keys[pygame.K_SPACE]:
				isJump= True
		else:
			if tire_bottom_collide>tile_y:
				isJump=False

			if jumpcount >= -7 and isJump==True:
				neg= 1
				if jumpcount<0:
					neg=-1
				bike.body_y-= (jumpcount**2)*0.5*neg
				jumpcount-=1

			else:
				isJump=False
				jumpcount=7

	'''
	elif quadrant==4:
		if keys[pygame.K_w] and bike.body_x<=(screen_width-width) and velocity<=max_velocity and no_forward== False:
			velocity+=acceleration

		elif keys[pygame.K_w] and bike.body_x>=0 and velocity<=max_velocity and no_forward== False:
			velocity-=decceleration

		#for slowing down
		elif(velocity<0 and bike.body_x<=(screen_width-width)):
			velocity+=acceleration

		elif(velocity>0 and bike.body_x<=(screen_width-width)):
			velocity-=decceleration

	elif quadrant==5:
		if keys[pygame.K_w] and bike.body_x<=(screen_width-width) and velocity<=max_velocity and no_forward== False:
			velocity+=acceleration

		elif keys[pygame.K_w] and bike.body_x>=0 and velocity<=max_velocity and no_forward== False:
			velocity-=decceleration

		#for slowing down
		elif(velocity<0 and bike.body_x<=(screen_width-width)):
			velocity+=acceleration

		elif(velocity>0 and bike.body_x<=(screen_width-width)):
			velocity-=decceleration
	'''



	#quadrant testings
	if (tire_right_collide<=tile_x and bike.back_wheel_y>tile_y):
		quadrant=1

	elif(tire_right_collide<=tile_x and bike.back_wheel_y<tile_y):
		quadrant=2

	elif(bike.back_wheel_x+tire_diameter<tile_x+tile_length and bike.back_wheel_x>tile_x and bike.back_wheel_y>tile_y):
		quadrant=3

	elif(bike.back_wheel_y<tile_y and bike.back_wheel_x>tile_x+tile_length):
		quadrant=4

	elif(bike.back_wheel_y>tile_y and bike.back_wheel_x>tile_x+tile_length):
		quadrant=5


	print("default land ",default_land,"tire_bottom_collide",tire_bottom_collide,"bike.back_wheel_y ",bike.back_wheel_y,"quadrant ",quadrant)
