import codes
import threading, time
import argparse

def update_html(folder='/u/oooolga/public_html/results_folder', html_name='index'):
	dir_html = codes.list_directory.DirectoryHTML(folder, html_name)
	dir_html.write_html()


def get_args():
	'''This function parses and return arguments passed in'''
	parser = argparse.ArgumentParser(        
		description='Script to make an index page for the folder.')

	parser.add_argument('dir', type=str, help='Directory to make the file listing page.')
	parser.add_argument('-n', '--html-name', type=str, help='html link name',
		required=False, default='index')

	args = parser.parse_args()
	save_dir = args.dir
	html_name = args.html_name
	

	return save_dir, html_name


if __name__ == '__main__':
	save_dir, html_name = get_args()
	update_html(save_dir, html_name)