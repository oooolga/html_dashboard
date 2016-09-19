__author__ = "Olga (Ge Ya) Xu"

from os import listdir
import os
import codes.main

import pdb
from time import gmtime, strftime, ctime
CURR_TIME = strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime())

class DirectoryHTML(codes.main.HTMLFramework):
	def __init__(self, directory, html_name='index'):
		if not os.path.isdir(directory):
			print('Error: directory does not exist.')

		super(DirectoryHTML, self).__init__(page_name=html_name,
											html_folder=directory,
											page_title='Index of {}'.format(directory))

		self.body.text('Site last modified on {}.'.format(CURR_TIME))

		self.files = listdir(self.html_folder)

		table = self.body.table()

		header_row = table.tr

		header_row.th().text('Name')
		header_row.th().text('Last Modified')
		header_row.th().text('Size Description')

		for f in self.files:
			row = table.tr
			row.td().a(href='{}'.format(f)).text('{}'.format(f))
			row.td(align='right').text('{}'.format(ctime(os.path.getmtime('{}/{}'.format(directory, f)))))
			row.td(align='right').text('{}'.format(os.path.getsize('{}/{}'.format(directory, f))))