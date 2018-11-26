import sys
from PIL import Image

def encode(visible_image,hidden_image,output_file):
	# create an output image of the same size as the visible image
	output_image = Image.new('RGB',(visible_image.width,visible_image.height))
	# this array will store the rgb values of the encoded file
	pixels = []

	w = hidden_image.width
	h = hidden_image.height

	# encoding width first
	# the indexes (starting from right) in the binary representation of width are stored as :
	# ... ( ~~~~~~(10)(11) ~~~~~~89 ~~~~~~67 ) ( ~~~~~~45 ~~~~~~23 ~~~~~~01 ) 
	for i in range(0,5):
		r,g,b = visible_image.getpixel((i%visible_image.width, i//visible_image.width))
		r = ((r>>2)<<2) + (w>>4)%4
		g = ((g>>2)<<2) + (w>>2)%4
		b = ((b>>2)<<2) + (w)%4
		w = w>>6
		pixels.append((r,g,b))

	# height is encoded the same way as width
	for i in range(5,10):
		r,g,b = visible_image.getpixel((i%visible_image.width, i//visible_image.width))
		r = ((r>>2)<<2) + (h>>4)%4
		g = ((g>>2)<<2) + (h>>2)%4
		b = ((b>>2)<<2) + (h)%4
		h = h>>6
		pixels.append((r,g,b))

	# c counts the number of pixels of hidden image encoded till now.
	c = -1
	for i in range(10, visible_image.height*visible_image.width):
		if (i-1)%3==0:
			c += 1
		if(c<(hidden_image.width*hidden_image.height)):
			# v stores the appropriate (R/G/B) color value depending on the value of i
			v = hidden_image.getpixel((c%hidden_image.width, c//hidden_image.width))[(i-1)%3]
			r,g,b = visible_image.getpixel((i%visible_image.width, i//visible_image.width))
			r = ((r>>2)<<2) + (v>>2)%4
			g = ((g>>2)<<2) + (v>>4)%4
			b = ((b>>2)<<2) + (v>>6)%4
			# the binary representation of a certain value of v is stored as :
			# ( ~~~~~~32 ~~~~~~54 ~~~~~~76 )
			pixels.append((r,g,b))
		else:
			# append the visible_image's pixels without modification.
			pixels.append(visible_image.getpixel((i%visible_image.width, i//visible_image.width)))

	output_image.putdata(pixels)
	output_image.save(output_file)

def check(visible_file, hidden_file, output_file):
	visible_image = Image.open(visible_file).convert('RGB')
	hidden_image = Image.open(hidden_file).convert('RGB')
	# the visible image should be 10 pixels larger than thrice the size of hidden image.
	# thrice larger because 3 pixels of visible image store 1 pixel of hidden image
	# 10 larger because size of the hidden image is stored in 10 initial pixels.
	if visible_image.width*visible_image.height >= 3*(hidden_image.width*hidden_image.height) + 10:
		encode(visible_image,hidden_image,output_file)
	else:
		print "The image to hide is too large. Use a smaller hidden-image or a larger visible-image."
	

if __name__ == '__main__':
	count = len(sys.argv)-1
	if count == 3:
		# output file has been specified
		check(sys.argv[1],sys.argv[2], sys.argv[3])
	elif count == 2:
		# output file has not been specified, 'output.png' is chosen as the default output file
		check(sys.argv[1],sys.argv[2],'output.png')
	else:
		print "Invalid arguments."
		print "Syntax : stegano-encoder.py visible_image.png hidden_image.png [output.png]"

