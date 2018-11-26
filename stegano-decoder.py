import sys
from PIL import Image

def decode(encoded_file,output_file):
	encoded_image = Image.open(encoded_file)
	pixels = []
	
	width, height = 0,0
	for i in range(4,-1,-1):
		r,g,b = encoded_image.getpixel((i%encoded_image.width, i//encoded_image.width))
		width = (4*width)+r%4
		width = (4*width)+g%4
		width = (4*width)+b%4
	for i in range(9,4,-1):
		r,g,b = encoded_image.getpixel((i%encoded_image.width, i//encoded_image.width))
		height = (4*height)+r%4
		height = (4*height)+g%4
		height = (4*height)+b%4

	output_image = Image.new('RGB',(width,height))

	r,g,b=0,0,0
	for i in range(10, 3*(height*width) + 10):
		l,m,n = encoded_image.getpixel((i%encoded_image.width, i//encoded_image.width))
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
			pixels.append((r,g,b))

	output_image.putdata(pixels)
	output_image.save(output_file)

if __name__ == '__main__':
	count = len(sys.argv)-1
	if count == 1:
		decode(sys.argv[1], 'decoded.png')
	elif count == 2:
		decode(sys.argv[1], sys.argv[2])
	else:
		print "Invalid arguments."
		print "Syntax : stegano-decoder.py encoded.png [decoded.png]"
