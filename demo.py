import demo
import codes

import argparse
from time import gmtime, strftime

def get_args():
	'''This function parses and return arguments passed in'''
	parser = argparse.ArgumentParser(        
		description='Script to run the HTML dashboard demo.')

	parser.add_argument('dir', type=str, help='Directory to save demo files.')

	args = parser.parse_args()
	save_dir = args.dir

	return save_dir

if __name__ == '__main__':
	save_dir = get_args()

	# create demo folder
	demo_folder = codes.main.setFileDirectory(save_dir, 'mnist_demo')

	# run demo
	start_time = strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime())
	model_results, log_path = demo.MNIST_demo.train_script(demo_folder)
	end_time = strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime())

	# creat html page
	web_log = codes.main.HTMLFramework('demo', html_folder=demo_folder, page_title='MNIST demo')

	web_log.add_blank_line()

	# write a list for start and end time and other information about the model
	web_log.set_list(['Start time: {}'.format(start_time),
					  'End time: {}'.format(end_time),
					  'lr: {}, number of conv layers: {}, batch size: {}'.format('1e-4', 2, 50)],
					  sec_name='Model info')

	web_log.add_blank_line()

	# display loss and acc graph
	codes.main.drawGraph(xrange(0, 5000, 100), model_results['train_loss'], 'train', 'iters', 'loss',
				demo_folder, 'loss_graph')
	web_log.set_image('loss_graph.png')
	codes.main.drawGraph(xrange(0, 5000, 100), model_results['train_acc'], 'train', 'iters', 'acc',
				demo_folder, 'acc_graph')
	web_log.set_image('acc_graph.png')

	web_log.add_blank_line()

	# write log section
	with open(log_path, 'r') as f:
		web_log.set_text_scroll_box(f.read(), sec_name='Log')
	

	web_log.add_blank_line()

	# create a demo table with images
	train_images = codes.main.saveImagesFromMatrix(demo_folder, model_results['train_images'],
									prefix='mnist_train', m=40, size=(64, 64))
	test_images = codes.main.saveImagesFromMatrix(demo_folder, model_results['test_images'],
									prefix='mnist_test', m=40, size=(64, 64))

	train_captions = codes.main.generateCaptions(model_results['train_pred'],
									model_results['train_label'], m=40)
	test_captions = codes.main.generateCaptions(model_results['test_pred'],
									model_results['test_label'], m=40)

	web_log.set_image_table(train_images, width=64, height=64, captions=train_captions, 
							num_col=5, sec_name='Training Examples')
	web_log.add_blank_line()
	web_log.set_image_table(test_images, width=64, height=64, captions=test_captions, 
							num_col=5, sec_name='Testing Examples')

	# write html
	web_log.write_html()
	print '\nThe html page is saved to {}'.format(web_log.page_dir)

	# Direcotry html
	dir_html = codes.list_directory.DirectoryHTML(demo_folder)
	dir_html.write_html()

