# cd C:\Users\anton_mc03yx6\Documents\GitHub\map-maker
#try excepts
#name generation (archipelago, peninsula, strait, etc)
import pygame, os

pygame.init()
width 		= 1280
height 		= 720
resolution	= 40
screen 		= pygame.display.set_mode((width,height))

land_center	 	= pygame.image.load(os.path.join('sprites', 'land_center.png')).convert_alpha()
land_side	 	= pygame.image.load(os.path.join('sprites', 'land_side.png')).convert_alpha()
land_bridge		= pygame.image.load(os.path.join('sprites', 'land_bridge.png')).convert_alpha()
land_corner 	= pygame.image.load(os.path.join('sprites', 'land_corner.png')).convert_alpha()
land_peninsula 	= pygame.image.load(os.path.join('sprites', 'land_peninsula.png')).convert_alpha()
land_island 	= pygame.image.load(os.path.join('sprites', 'land_island.png')).convert_alpha()
water 			= pygame.image.load(os.path.join('sprites', 'water.png')).convert_alpha()

white 	= (255, 255, 255)
black 	= (0, 0, 0)
blue 	= (52, 119, 235)
green 	= (0, 255, 0)
red 	= (255, 0, 0)

class World:
	def __init__(self):
		#initialize the world/map-instance
		self.chart = [["water" for y in range(int(height/resolution+1))] for x in range(int(width/resolution+1))]

	def update(self):
		#loop through the map and update the colors
		for x in range(0,len(self.chart)):
			for y in range(0,len(self.chart[x])):
				screen.blit(water, (x*resolution, y*resolution))
				
				if self.chart[x][y] == "land":
					#find out which tile to use by looking at the number of beaches
					beaches = 0
					if self.chart[x-1][y] == "water":
						beaches += 1

					if self.chart[x+1][y] == "water":
						beaches += 1

					if self.chart[x][y-1] == "water":
						beaches += 1

					if self.chart[x][y+1] == "water":
						beaches += 1
					
					#find out how to rotate the tile and print it on the screen
					if beaches == 0:
						#center
						screen.blit(land_center, (x*resolution, y*resolution))

					elif beaches == 1:
						#sides
						if self.chart[x-1][y] == "water":
							screen.blit(land_side, (x*resolution, y*resolution))
						elif self.chart[x+1][y] == "water":
							screen.blit(rot_center(land_side, 180), (x*resolution, y*resolution))
						elif self.chart[x][y-1] == "water":
							screen.blit(rot_center(land_side, 270), (x*resolution, y*resolution))
						elif self.chart[x][y+1] == "water":
							screen.blit(rot_center(land_side, 90), (x*resolution, y*resolution))

					elif beaches == 2:
						#corners
						if (self.chart[x-1][y] == "water") and (self.chart[x][y-1] == "water"):
							screen.blit(land_corner, (x*resolution, y*resolution))
						elif (self.chart[x][y-1] == "water") and (self.chart[x+1][y] == "water"):
							screen.blit(rot_center(land_corner, -90), (x*resolution, y*resolution))
						elif (self.chart[x+1][y] == "water") and (self.chart[x][y+1] == "water"):
							screen.blit(rot_center(land_corner, 180), (x*resolution, y*resolution))
						elif (self.chart[x-1][y] == "water") and (self.chart[x][y+1] == "water"):
							screen.blit(rot_center(land_corner, 90), (x*resolution, y*resolution))
						#bridges
						elif (self.chart[x-1][y] == "water") and (self.chart[x+1][y] == "water"):
							screen.blit(land_bridge, (x*resolution, y*resolution))
						elif (self.chart[x][y-1] == "water") and (self.chart[x][y+1] == "water"):
							screen.blit(rot_center(land_bridge, 90), (x*resolution, y*resolution))

					elif beaches == 3:
						if self.chart[x][y+1] == "land":
							screen.blit(land_peninsula, (x*resolution, y*resolution))
						elif self.chart[x+1][y] == "land":
							screen.blit(rot_center(land_peninsula, 90), (x*resolution, y*resolution))
						elif self.chart[x][y-1] == "land":
							screen.blit(rot_center(land_peninsula, 180), (x*resolution, y*resolution))
						elif self.chart[x-1][y] == "land":
							screen.blit(rot_center(land_peninsula, 270), (x*resolution, y*resolution))
					elif beaches == 4:
						#islands
						screen.blit(land_island, (x*resolution, y*resolution))

	def click(self, pos_x, pos_y):
		self.chart[int(pos_x/resolution)][int(pos_y/resolution)] = "land"
		return

	def rightClick(self, pos_x, pos_y):
		self.chart[int(pos_x/resolution)][int(pos_y/resolution)] = "water"
		return

def main():
	done = False
	#create the world/map-instance
	chartInstance = World()
	chartInstance.update()

	while not done:
		for event in pygame.event.get():
			#handle the "x"/close-button
			if event.type == pygame.QUIT:
				done = True
			#handle mos click pos
			if event.type == pygame.MOUSEBUTTONUP:
				pos_x, pos_y = pygame.mouse.get_pos()
				if event.button == 1:
					chartInstance.click(pos_x, pos_y)
				elif event.button == 3:
					chartInstance.rightClick(pos_x, pos_y)

		chartInstance.update()
		pygame.display.update()

def rot_center(image, angle):
	#rotate an image while keeping its center and size
	orig_rect = image.get_rect()
	rot_image = pygame.transform.rotate(image, angle)
	rot_rect = orig_rect.copy()
	rot_rect.center = rot_image.get_rect().center
	rot_image = rot_image.subsurface(rot_rect).copy()
	return rot_image

main()