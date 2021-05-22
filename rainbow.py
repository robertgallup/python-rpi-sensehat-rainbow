#!/usr/bin/env python3

from sense_hat import SenseHat
import time, math, random

# Various options
class option(object):
	CORNERS = [ \
		{'a': False, 'b': True}, \
		{'a': True, 'b': False}, \
		{'a': True, 'b': True},  \
		{'a': False, 'b': False}  ]

	RAINBOW_SPEED  = .07
	MATRIX_WIDTH   = 8
	MATRIX_HEIGHT  = 8
	ANIMATION_REPS = 3

# Calculate a color based on a position (0-255)
# 0-255 is divided into 3 regions. In each region
# R, G, and B are rising or falling between 0-255
# The color range begins and ends on red to create
# a smooth transition from 255 back to zero
def color_rainbow (color):
	color = abs(color) % 256
	edge = color // 85
	color = 3 * (color % 85)
	if edge is 0: return (255 - color, color, 0)
	if edge is 1: return (0, 255 - color, color)
	return (color, 0, 255 - color)

# Create the sense hat object
sense = SenseHat()
sense.low_light = True

last_corner = -1
corner = last_corner

# Loop continuously
while True:

	color = 0
	# Choose the corner the rainbow eminates from
	while corner == last_corner:
		corner = random.choice(option.CORNERS)
	last_corner = corner

	# Calculate the rainbow color list (length depends on the
	# animation direction
	num_colors = option.MATRIX_WIDTH + (-1 if corner['b'] else 1)
	colors = [color_rainbow(c) for c in range(0, 255, int(255/num_colors))]
	reps = option.ANIMATION_REPS * num_colors

	# Iterate the animations the specified number of times
	for reps in range(reps):
		# Start with an empty pixel color list
		pixels = []
		# For each row and column, set the next pixel to the next color in
		# the color list
		for c in range(8):
			for r in range(8):
				pixels = pixels + [colors[color]] if corner['a'] else [colors[color]] + pixels
				color = (color + 1) % num_colors
		# The pixel list is complete, use it to set the Sense Hat pixels
		sense.set_pixels(pixels)
		# Take a short break
		time.sleep(option.RAINBOW_SPEED)
