import sys
from PIL import image

def check(visible_image, hidden_image, output):
	print "Visible = ",visible_image
	print "Hidden = ",hidden_image
	print "Output = ",output
	vis = Image.open(visible_image)
	img.show()
	

if __name__ == '__main__':
	count = len(sys.argv)-1
	print count
	if count == 3:
		check(sys.argv[1],sys.argv[2], sys.argv[3])
	elif count == 2:
		check(sys.argv[1],sys.argv[2],'output.jpg')
	else:
		print "Invalid arguments."
		print "Syntax : stegano-encoder.py visible_image.jpg hidden_image.jpg [output.jpg]"
