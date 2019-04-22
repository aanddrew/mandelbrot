import pygame
import math

pygame.init()

#increase this value to increase zoom
pixelsPerUnit = 100000

#defines the scale for the graph to be drawn at
#this number translates into how many 'x' units for each pixel on the screen
scale = 1.0/pixelsPerUnit

#change these values to change where to zoom in on.
dispCenter = (-0.761574,-0.0847596)

display_width = 800
display_height = 600
dimensions = (display_width, display_height)
display = pygame.display.set_mode(dimensions)
center = (display_width /2 - pixelsPerUnit*dispCenter[0], \
					display_height/2 + pixelsPerUnit*dispCenter[1])

done = False

#this class represents our complex number which is really just a 2d vector
class Complex:
	#real and imaginary components
	r = 0.0
	i = 0.0

	#these are used by the mandelbrot calculations
	#in the equation z_n+1 = (z_n)^2 + C
	#the original values of r and i are used as the constant
	r_start = 0.0
	i_start = 0.0

	def __init__(self, r, i):
		self.r = r
		self.i = i
		self.r_start = r
		self.i_start = i

	#this plugs the complex number into the equation:
	#z_n+1 = (z_n)^2 + C
	def mandelize(self):
		a = self.r
		b = self.i
		self.r = a*a - b*b + self.r_start
		self.i = 2*a*b + self.i_start

	#pythagorean formula
	def size(self):
		return math.sqrt(self.r*self.r + self.i*self.i)

	#for debugging, not used in the program
	def disp(self):
		print(str(self.r) +  " + " + str(self.i) + "i")


#this is not super necessary, about to be overwritten
display.fill((100,100,100))
pygame.display.update()

#for every pixel on the screen
for r in range(0,display_height):
	for c in range(0, display_width):
		print (r,c)
		x = -1*(center[0] - c) * scale
		y = (center[1] - r) * scale

		#create a new complex number at these x and y coordinates
		comp = Complex(x, y)

		black = True
		counter = 0
		#we iterate over the formula to see if the formula diverges at this point
		max = 200
		while black and counter < max:
			#apply the formula iteratively
			comp.mandelize()
			#if the number goes out of a circle of radius two, we know it will be
			#unbounded here. This is math that I don't understand, but I know
			#it is a nice shortcut for our calculations
			if comp.size() > 2:
				black = False
			counter += 1

		#assume its black
		color = (0,0,0)
		#if it's not black, we have a weird color picking process
		if not black:
			red = 0.0
			green = 0.0
			blue = 0.0
			red = counter*255/100
			if counter > max/3:
				red = 255
				green = (counter % (max/3)) *255/100
			if counter > 2*max/3:
				red = 255
				green = 255
				blue = (counter % (max/3)) *255/100
			color = (red,green,blue)
		pygame.draw.rect(display, color, pygame.Rect(c,r,1,1))
		# pygame.display.update()

pygame.display.update()
#now we display the result to the user until they want to quit
while not done:
	for event in pygame.event.get():
	  if event.type == pygame.QUIT:
	  	done = True

	#the display actually doesnt need to be updated anymore
	# pygame.display.update()