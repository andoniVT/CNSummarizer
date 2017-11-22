import matplotlib.pyplot as plt
import numpy as np
from pylab import *



def create_free_vectors(size):
	vector = []
	for i in range(size):
		vector.append([])
	return vector

def read_file(file):
	sin_pesos = ['dg', 'pr', 'sp', 'accs_h2' , 'gaccs', 'at', 'sym_l_b_h2', 'sym_h_b_h2']
	con_pesos = ['stg' , 'pr_w', 'sp_w']

	dictionary = dict()
	document = open(file, 'r')
	for i in document:
		i = i.rstrip('\n')
		i = i.rstrip('\r')
		datos =  i.split(',') 
		datos = datos[1:]
		measure = datos[0]
		results = datos[1:]
		results = [float(i) for i in results]
		if measure in con_pesos:
			if measure in dictionary:
				vector = dictionary[measure]
				vector[0].append(results[0])
				dictionary[measure] = vector
			else:
				vector = [[]]
				vector[0].append(results[0])
				dictionary[measure] = vector
		elif measure in sin_pesos:
			if measure in dictionary:
				vector = dictionary[measure]
				for j in range(len(results)):
					vector[j].append(results[j]) 
				dictionary[measure] = vector
			else:
				vector = create_free_vectors(5)
				for j in range(len(results)):
					vector[j].append(results[j]) 
				dictionary[measure] = vector
		else:
			pass

	return dictionary

def merge(set1, set2):
	merged = []
	for i , j in zip(set1, set2):
		if i > j:
			merged.append(i)
		else:
			merged.append(j)
	return merged


def merge_results(set_ribaldo, set_ngrams):
	remove = 'sym_h_b_h2'
	dictionary = dict()
	for ribaldo, ngram  in zip(set_ribaldo.items(), set_ngrams.items()):
		measure = ribaldo[0]
		if measure != remove:
			datos_ribaldo = ribaldo[1]
			datos_ngrams = ngram[1]
			datos_merged = []
			for d_r , d_n in zip(datos_ribaldo, datos_ngrams):
				merged = merge(d_r, d_n)
				datos_merged.append(merged)
			dictionary[measure] = datos_merged
	return dictionary 


def get_max_min(dictionary):
	maximos = []
	minimos = []

	for i in dictionary.items():
		coordenadas = i[1]
		for j in coordenadas:
			maximos.append(max(j))
			minimos.append(min(j))   
	
	return [max(maximos), min(minimos)] 


def make_title_dictionary():
	dictionary = dict()
	keys = ['dg', 'pr', 'sp', 'accs_h2' , 'gaccs', 'at' , 'sym_l_b_h2', 'stg' , 'pr_w', 'sp_w']
	values = ['Degree', 'Page Rank', 'Shortest Path' ,'Accessibility', 'G. Accessibility', 'Absorption Time',
	'Symmetry', 'Strength', 'Page Rank W.', 'Shortest Path W.']

	for k , v in zip(keys, values):
		dictionary[k] = v 
	return dictionary


def analyze_non_weighted(measures, set_ribaldo, set_ngrams, language='ptg'): # measures maximo tamanio 4
	datos_merged = merge_results(set_ribaldo, set_ngrams)


	#for i in datos_merged.items():
	#	print i [0],  datos_merged[i [0]] 
	#	print ''


	if language!='ptg':
		measures.remove('at')


	#max_min_parameters = get_max_min(datos_merged)
	#max_limit = max_min_parameters[0]
	#min_limit = max_min_parameters[1]

	x = [0.5, 0.6, 0.7, 0.8, 0.9, 1, 1.1, 1.3, 1.5, 1.7, 1.9]
	#colors = ['blue', 'red', 'darkgreen', 'yellow', 'cyan']
	#colors = ['cyan', 'lime', 'orange', 'red', 'indigo']
	colors = ['blue', 'darkgreen', 'orange', 'red', 'indigo']
	legends = ['10%', '20%', '30%', '40%', '50%']

	titles = make_title_dictionary()



	f, axarr = plt.subplots(2, 2)
	axes = [axarr[0,0] , axarr[0,1], axarr[1,0], axarr[1,1]]

	for index, measure in enumerate(measures):
		coordenadas = datos_merged[measure]
		for index2 , coord in enumerate(coordenadas):
			axes[index].plot(x, coord, color=colors[index2], linewidth=3.5)
		axes[index].set_title(titles[measure])
		#axes[index].set_ylim(min_limit, max_limit)
		axes[index].legend(legends, loc='upper right')
		#axes[index].set_ylabel('Rouge Recall')


	plt.show()


def analyze_weighted(set_ribaldo, set_ngrams):
	datos_merged = merge_results(set_ribaldo, set_ngrams)
	


	#max_min_parameters = get_max_min(datos_merged)
	#max_limit = max_min_parameters[0]
	#min_limit = max_min_parameters[1]
	titles = make_title_dictionary()


	measures = ['stg', 'sp_w', 'pr_w']
	x = [0.5, 0.6, 0.7, 0.8, 0.9, 1, 1.1, 1.3, 1.5, 1.7, 1.9]
	colors = ['blue', 'red', 'darkgreen']
	legends = []
	for i in measures:
		legends.append(titles[i])



	'''
	for index, measure in enumerate(measures):
		coordenadas = datos_merged[measure][0]
		plt.plot(x, coordenadas, color=colors[index], linewidth=3.0)
	plt.legend(legends, loc='upper right')
	plt.title('Non-weighted measurements')
	'''

	f, axarr = plt.subplots(2, 2)
	axes = [axarr[0,0] , axarr[0,1], axarr[1,0], axarr[1,1]]

	for index, measure in enumerate(measures):
		coordenadas = datos_merged[measure][0]
		axes[0].plot(x, coordenadas, color=colors[index], linewidth=3.0)
	axes[0].set_title('Non-weighted measurements')
	#axes[0].set_ylim(min_limit, max_limit)
	axes[0].legend(legends, loc='lower right')
	#axes[0].legend(legends, loc='upper right')
		
		


	plt.show()

		

if __name__ == '__main__':
	
	path_ribaldo_cst = 'CSTNews/cst_news_ribaldo.csv'
	path_ngrams_cst = 'CSTNews/cst_news_ngrams.csv'

	path_ribaldo_duc2002 = 'DUC2002/duc2002_ribaldo.csv'
	path_ngrams_duc2002 = 'DUC2002/duc2002_ngrams.csv'

	path_ribaldo_duc2004 = 'DUC2004/duc2004_ribaldo.csv'
	path_ngrams_duc2004 = 'DUC2004/duc2004_ngrams.csv'



	#datos_ribaldo = read_file(path_ribaldo_cst)
	#datos_ngrams = read_file(path_ngrams_cst)

	#datos_ribaldo = read_file(path_ribaldo_duc2002)
	#datos_ngrams = read_file(path_ngrams_duc2002)

	

	datos_ribaldo = read_file(path_ribaldo_duc2004)
	datos_ngrams = read_file(path_ngrams_duc2004)



	'''
	'dg', 'pr', 'sp', 'at'  , 'accs_h2' , 'gaccs', 'sym_l_b_h2'
	'stg' , 'pr_w', 'sp_w'
	'sym_h_b_h2' ---> ya no 
	'''

	#measures = ['dg', 'pr', 'sp', 'accs_h2']
	measures = ['gaccs', 'sym_l_b_h2', 'at'] 
	


	analyze_non_weighted(measures, datos_ribaldo, datos_ngrams) 



	#analyze_weighted(datos_ribaldo, datos_ngrams)








