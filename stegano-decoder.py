import sys
from PIL import Image

def decode(encoded_file,output_file):
	# image representation of the encoded file
	encoded_image = Image.open(encoded_file)
	# this array will store the pixels of the hidden file
	pixels = []
	
	width, height = 0,0
	# reading width from the first 5 pixels
	for i in range(4,-1,-1):
		r,g,b = encoded_image.getpixel((i%encoded_image.width, i//encoded_image.width))
		width = (4*width)+r%4
		width = (4*width)+g%4
		width = (4*width)+b%4
	# reading height from the next 5 pixels
	for i in range(9,4,-1):
		r,g,b = encoded_image.getpixel((i%encoded_image.width, i//encoded_image.width))
		height = (4*height)+r%4
		height = (4*height)+g%4
		height = (4*height)+b%4

    # image representation of the hidden file
	output_image = Image.new('RGB',(width,height))

	r,g,b=0,0,0
	for i in range(10, 3*(height*width) + 10):
		# l,m,n store the rgb values of a pixel in the encoded file
		l,m,n = encoded_image.getpixel((i%encoded_image.width, i//encoded_image.width))
		# the corresponding value (r/g/b) of the hidden image is read from 1 entire pixel (all 3 rgb values) of the encoded file
		# %4 is used because only the last two bits of a color value store the information of the hidden file
		# once we get 2 bits, we shift the bits to the left to accomodate new bits.
		v = 0
		v += n%4
		v <<= 2
		v += m%4
		v <<= 2
		v += l%4
		v <<= 2
		if i%3==1:
			r=v
		elif i%3==2:
			g=v
		else:
			b=v
			# we get one entire pixel of the hidden file after reading every 3 pixels of the encoded file
			pixels.append((r,g,b))

	output_image.putdata(pixels)
	output_image.save(output_file)

if __name__ == '__main__':
	count = len(sys.argv)-1
	if count == 1:
	    # decoded file has not been specified. 'decoded.png' is used as default decoded file.
		decode(sys.argv[1], 'decoded.png')
	elif count == 2:
	    # decoded file has been specified.
		decode(sys.argv[1], sys.argv[2])
	else:
		print "Invalid arguments."
		print "Syntax : stegano-decoder.py encoded.png [decoded.png]"
