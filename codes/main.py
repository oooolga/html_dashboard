__author__ = "Olga (Ge Ya) Xu"

import pdb
from html import HTML

import argparse, os, shutil
from time import gmtime, strftime

CURR_TIME = strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime())

class HTMLFramework(object):
	
	def __init__(self,
				page_name,
				html_folder='~/public_html',
				page_title=None):
	
		if not os.path.isdir(html_folder):
			raise('Error: HTML folder does not exit.')
			return 
	
		self.html_folder = html_folder
		self.page_dir = '{}/{}.html'.format(html_folder, page_name)
		
		# create the html page
		with open(self.page_dir, 'w') as f:
			f.write('<!DOCTYPE html>\n')
			self.html_content = HTML('html')
		
		# create title 
		if page_title:
			self.head = self.html_content.head()
			self.head.title(page_title)
		
		self.body = self.html_content.body()
		
		if page_title:
			self.body.h1().text(page_title)
			
	
	def set_text_scroll_box(self, text, width='80%', height='150px', sec_name=None):
	
		'''
		Generate a scrolling text block of content text.
		'''
		
		self.set_sec_header(sec_name)

		div = self.body.div(
			style='width:{};height:{};overflow:{};padding:{};'.format(
			width, height, 'auto', '5px'))
		
		lines = text.split('\n')
		paragraph = div.p()

		for line in lines:
			paragraph.text(line)
			paragraph.br()


	def set_image(self, image_path, alt='', style='width:50%', sec_name=None):

		self.set_sec_header(sec_name)

		self.body.img(src=image_path,
					  alt=alt,
					  style=style)
		
	
	def set_list(self, L, sec_name=None):
	
		self.set_sec_header(sec_name)
		
		ul = self.body.ul()
		for item in L:
			ul.li(str(item))
			
			
	def set_image_table(self, images, width=128, height=128, captions=None, num_col=2, sec_name=None):
		'''
		(HTMLFramework, list of str, list of list of str, int, str) -> None
		
		images is a list of images' path. Make sure the image path is relative to your HTML folder.
				
		captions is a list of lists of captions for each image.
		The dimension of captions should be n x c.
		n = number of images
		c = number of captions for each image
		'''
		
		self.set_sec_header(sec_name)
		
		table = self.body.table()

		num_images = len(images)
		if captions:
			num_captions = len(captions[0])
			if num_images != len(captions):
				raise('Error: number of images does not equal to number of captions.')

		temp = num_images % num_col
		num_row = num_images//num_col if temp==0 else (num_images//num_col)+1
		width_space = 100//num_col

		for i in range(num_row):
			row = table.tr

			for j in range(min(num_col, num_images-(i*num_col))):
				image_i = images[i*num_col+j]
				td = row.td(valign='top', style='width:{}%'.format(width_space))
				td.img(src=image_i, width='{}'.format(width), height='{}'.format(height))

			if captions:
				for k in range(num_captions):
					row = table.tr
					for j in range(min(num_col, num_images-(i*num_col))):
						td = row.td(valign='top', style='width:{}%'.format(width_space))
						td.text(captions[i*num_col+j][k])


	def set_siamese_image_table(self, imagesA, imagesB,
								captions=None, width=128, height=128, sec_name=None):
		self.set_sec_header(sec_name)
		
		table = self.body.table()

		num_images = len(imagesA)
		num_captions = 0
		if captions:
			num_captions = len(captions[0])
			if num_images != len(captions):
				raise('Error: number of images does not equal to number of captions.')

		num_row = num_images//2 if num_images%2==0 else (num_images//2)+1

		width_space = 20

		for i in range(num_row):
			row = table.tr

			td = row.td(valign='top', style='width:{}%'.format(width_space))
			td.img(src=imagesA[i*2], width='{}'.format(width), height='{}'.format(height))

			td = row.td(valign='top', style='width:{}%'.format(width_space))
			td.img(src=imagesB[i*2], width='{}'.format(width), height='{}'.format(height))

			td = row.td(valign='top', style='width:{}%'.format(width_space))
			td.text(' ')

			if i*2+1 < num_images:
				td = row.td(valign='top', style='width:{}%'.format(width_space))
				td.img(src=imagesA[i*2+1], width='{}'.format(width), height='{}'.format(height))

				td = row.td(valign='top', style='width:{}%'.format(width_space))
				td.img(src=imagesB[i*2+1], width='{}'.format(width), height='{}'.format(height))

			for j in range(num_captions):
				row = table.tr 
				td = row.td(valign='top', style='width:{}%'.format(width_space*2), align='center', colspan='2')
				td.text(captions[i*2][j])

				td = row.td(valign='top', style='width:{}%'.format(width_space))
				td.text(' ')

				td = row.td(valign='top', style='width:{}%'.format(width_space*2), align='center', colspan='2')
				td.text(captions[i*2+1][j])


	def add_blank_line(self):
		self.body.br()
		
	
	def set_sec_header(self, sec_name):
		if sec_name:
			self.body.h3().text(sec_name)


	def write_html(self):
		with open(self.page_dir, 'ab') as f:
			f.write(str(self.html_content))
	
	

		
def setFileDirectory(root_directory, foldername):
	folder_path = root_directory + '/' + str(foldername)

	if not os.path.isdir(root_directory):
		raise('Error: saving directory does not exist.')
		return 
	if os.path.exists(folder_path):
		shutil.rmtree(folder_path)
	os.makedirs(folder_path)
	print('Directory \"'+folder_path+'\" made.')

	return folder_path


def saveImagesFromMatrix(save_dir, image_matrix, prefix='', m=None, size=None):
	'''
	Images in image_matrix would be saved to save_dir.

	There are only two type of image_mode: rgb or grey_scale.
	If image_mode == 'rgb', then the expected image_matrix dimension would be n x h x w x 3.
	Else the expected image_matrix dimension would be n x h x w.

	The first m images would be saved. (m<=10000)

	The names would be prefix_xxxx where xxxx is the index of that image.
	
	For example:
		save_dir = '~/public_html'
		prefix = 'mnist_train'
		Then the first image in image_matrix would be saved in the following path:
		~/public_html/mnist_train_0001.jpg
	'''

	import numpy as np 
	from PIL import Image

	save_images = []

	if not os.path.isdir(save_dir):
		raise('Error: saving directory does not exist.')
		return 

	if not m or m>image_matrix.shape[0]:
		m = len(image_matrix.shape[0])

	for img_i in range(m):
		arr= image_matrix[img_i, ::]*255

		img = Image.fromarray(arr.astype(np.uint8))

		# resize image
		if size:
			img = img.resize(size, Image.ANTIALIAS)

		img_dir = '{}/{}{:04d}.png'.format(save_dir, prefix, img_i)
		img.save(img_dir)

		save_images.append('{}{:04d}.png'.format(prefix, img_i))

	print 'Images are saved to {}.'.format(save_dir)

	return save_images

def generateCaptions(pred, label, prob=None, m=None):
	return_list = []

	if not m or m>len(pred):
		m = len(pred)

	for i in range(m):
		return_list.append(['pred: {}'.format(pred[i]), 'label: {}'.format(label[i])])
		if prob != None:
			return_list[i].append('prob: {:.4f}'.format(prob[i]))

	return return_list


def drawGraph(x, y, label, xlabel, ylabel, save_dir, save_name):

	import matplotlib.pyplot as plt
	plt.switch_backend('agg')

	plt.close('all')

	line, = plt.plot(x, y, label=label)
	plt.legend(handles=[line], loc=1)
	plt.xlabel(xlabel)
	plt.ylabel(ylabel)
	plt.savefig('{}/{}.png'.format(save_dir, save_name))