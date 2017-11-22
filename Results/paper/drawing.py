import matplotlib.pyplot as plt
import numpy as np
from pylab import *
import operator


def create_free_vectors(size):
	vector = []
	for i in range(size):
		vector.append([])
	return vector


def read_file(file):
	sin_pesos = ['at' , 'dg', 'gaccs', 'pr', 'sp']
	con_pesos = ['pr_w', 'sp_w', 'stg']

	symmetry = ['sym_l_b_h2', 'sym_l_m_h2', 'sym_h_b_h3', 'sym_h_m_h3',
	'sym_h_m_h2', 'sym_l_b_h3', 'sym_l_m_h3', 'sym_h_b_h2']

	accessibility = ['accs_h2' , 'accs_h3']

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
		elif measure in sin_pesos or measure in symmetry or measure in accessibility:
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



def draw(measure, datos):
	coordenadas = datos[measure]
	dictionary = dict()
	dictionary['pr'] = ('Page Rank' , True)
	dictionary['pr_w'] = ('Page Rank Weights' , False )
	dictionary['dg'] = ('Degree' , True)
	dictionary['stg'] = ('Strenght', False)
	dictionary['sp'] = ('Shortest Path', True)
	dictionary['sp_w'] = ('Shortest Path Weights', False)
	dictionary['at'] = ('Absorption Time', True)
	dictionary['gaccs'] = ('Generalized Accessibility', True) 


	x = [0.5, 0.6, 0.7, 0.8, 0.9, 1, 1.1, 1.3, 1.5, 1.7, 1.9]

	legends = ['10%', '20%', '30%', '40%', '50%']

	colors = ['blue', 'red', 'darkgreen', 'yellow', 'cyan']


	for index, coordenada in enumerate(coordenadas):
		plt.plot(x, coordenada, color=colors[index], linewidth=3.0)


	#plt.plot(x, prueba, color='blue', linewidth=3.0)



	if dictionary[measure][1]:
		plt.legend(legends, loc='upper right')



	plt.xlabel('Inter-edge weight')
	plt.ylabel('Rouge Recall')

	plt.title('MLN-TfIdf ' + dictionary[measure][0])

	
	plt.show()


def draw_weighted(datos, datos2):
	measures = ['pr_w', 'stg', 'sp_w'] 
	coordenadas = []
	coordenadas2 = []
	for i in measures:
		coordenadas.append(datos[i][0])
		coordenadas2.append(datos2[i][0])

	maximos = []
	minimos = []
	for i, j in zip(coordenadas, coordenadas2):
		maximos.append(max(i))
		maximos.append(max(j)) 
		minimos.append(min(i))
		minimos.append(min(j))

	max_limit = max(maximos) 
	min_limit = min(minimos) 
	
	x = [0.5, 0.6, 0.7, 0.8, 0.9, 1, 1.1, 1.3, 1.5, 1.7, 1.9]
	#legends = measures
	legends = ['Page Rank W.' , 'Strength' , 'Shortest Path W.']
	colors = ['blue', 'red', 'darkgreen']

	f, axarr = plt.subplots(1, 2)


	for index, coordenada in enumerate(coordenadas):
		axarr[0].plot(x, coordenada, color=colors[index], linewidth=3.0)
	axarr[0].set_title('MLN-TfIdf ARD-Ribaldo')
	axarr[0].legend(legends, loc='upper right')
	axarr[0].set_xlabel('Inter-edge weight')
	axarr[0].set_ylabel('Rouge Recall')
	axarr[0].set_ylim(min_limit, max_limit)
	


	for index, coordenada in enumerate(coordenadas2):
		axarr[1].plot(x, coordenada, color=colors[index], linewidth=3.0)
	axarr[1].set_title('MLN-TfIdf ARD-Ngrams')
	axarr[1].legend(legends, loc='upper right')
	axarr[1].set_xlabel('Inter-edge weight')
	axarr[1].set_ylabel('Rouge Recall')
	axarr[1].set_ylim(min_limit, max_limit)
	
	'''
	for index, coordenada in enumerate(coordenadas):
		plt.plot(x, coordenada, color=colors[index], linewidth=3.0)
	'''	
	#plt.xlabel('Inter-edge weight')
	#plt.ylabel('Rouge Recall')
	
	plt.show()


def draw_four_non_weighted(exclude, datos, datos2):
	measures = ['pr' ,'dg' ,'sp', 'at' ,'gaccs']
	measures.remove(exclude) ####### tener cuidadooooooo
	x = [0.5, 0.6, 0.7, 0.8, 0.9, 1, 1.1, 1.3, 1.5, 1.7, 1.9]
	colors = ['blue', 'red', 'darkgreen', 'yellow', 'cyan']
	dictionary = dict()
	dictionary['pr'] = 'Page Rank' 
	dictionary['dg'] = 'Degree' 
	dictionary['sp'] = 'Shortest Path'
	dictionary['at'] = 'Absorption Time'
	dictionary['gaccs'] = 'Generalized Accessibility'


	maximos = []
	minimos = []

	for index, measure in enumerate(measures):
		coordenadas = datos[measure]
		coordenadas2 = datos[measure]
		for i , j in zip(coordenadas, coordenadas2):
			maximos.append(max(i))
			minimos.append(min(i)) 

			maximos.append(max(j))
			minimos.append(min(j)) 


	max_limit = max(maximos) 
	min_limit = min(minimos) 


	#measures.remove(exclude) ######## tener cuidadooooo


	legends = ['10%', '20%', '30%', '40%', '50%']


	f, axarr = plt.subplots(2, 2)
	axes = [axarr[0,0] , axarr[0,1], axarr[1,0], axarr[1,1]]
	for index, measure in enumerate(measures):
		coordenadas = datos2[measure] #############
		for index2, coordenada in enumerate(coordenadas):
			axes[index].plot(x, coordenada, color=colors[index2], linewidth=3.0)
		axes[index].set_title(dictionary[measure])
		axes[index].set_ylim(min_limit, max_limit)
		axes[index].legend(legends, loc='upper right')
		axes[index].set_ylabel('Rouge Recall')
	
	plt.show()
	


def symmetry_analysis(type_measure, datos):  # mg bb h2 h3 l h 
	symmetry = ['sym_L_b_h2', 'sym_L_m_h2', 'sym_H_b_h3', 'sym_H_m_h3', 'sym_H_m_h2', 
	'sym_L_b_h3', 'sym_L_m_h3', 'sym_H_b_h2']


	maximos = []
	minimos = []

	for index, measure in enumerate(symmetry):
		coordenadas = datos[measure.lower()]
		for i in coordenadas:
			maximos.append(max(i))
			minimos.append(min(i))

	max_limit = max(maximos) 
	min_limit = min(minimos)


	parameter = '_' + type_measure
	measures = []

	for i in symmetry:
		if i.find(parameter)!=-1:
			measures.append(i.lower())


	x = [0.5, 0.6, 0.7, 0.8, 0.9, 1, 1.1, 1.3, 1.5, 1.7, 1.9]  

	colors = ['blue', 'red', 'darkgreen', 'yellow', 'cyan']
	
	legends = ['10%', '20%', '30%', '40%', '50%']

	f, axarr = plt.subplots(2, 2)
	axes = [axarr[0,0] , axarr[0,1], axarr[1,0], axarr[1,1]]

	for index, measure in enumerate(measures):
		coordenadas = datos[measure]
		for index2 , coordenada in enumerate(coordenadas):
			axes[index].plot(x, coordenada, color=colors[index2], linewidth=3.0)
		axes[index].set_title(measure)
		axes[index].set_ylim(min_limit, max_limit)
		axes[index].legend(legends, loc='upper right')
		axes[index].set_ylabel('Rouge Recall')

	plt.show()


def symmetry_second_analysis(datos):
	symmetry = ['sym_l_b_h2', 'sym_l_m_h2', 'sym_l_b_h3', 'sym_l_m_h3']

	maximos = []
	minimos = []

	for index, measure in enumerate(symmetry):
		coordenadas = datos[measure.lower()]
		for i in coordenadas:
			maximos.append(max(i))
			minimos.append(min(i))

	max_limit = max(maximos) 
	min_limit = min(minimos)
	
	x = [0.5, 0.6, 0.7, 0.8, 0.9, 1, 1.1, 1.3, 1.5, 1.7, 1.9]  
	colors = ['blue', 'red', 'darkgreen', 'yellow', 'cyan']
	legends = ['10%', '20%', '30%', '40%', '50%']

	f, axarr = plt.subplots(2, 2)
	axes = [axarr[0,0] , axarr[0,1], axarr[1,0], axarr[1,1]]

	for index, measure in enumerate(symmetry):
		coordenadas = datos[measure]
		for index2 , coordenada in enumerate(coordenadas):
			axes[index].plot(x, coordenada, color=colors[index2], linewidth=3.0)
		axes[index].set_title(measure)
		axes[index].set_ylim(min_limit, max_limit)
		axes[index].legend(legends, loc='upper right')
		axes[index].set_ylabel('Rouge Recall')

	plt.show()








def accessibility_analysis(datos):
	measures = ['accs_h2' , 'accs_h3'] 
	x = [0.5, 0.6, 0.7, 0.8, 0.9, 1, 1.1, 1.3, 1.5, 1.7, 1.9]
	colors = ['blue', 'red', 'darkgreen', 'yellow', 'cyan']

	f, (ax1, ax2) = plt.subplots(2, sharex=True, sharey=True)

	axes = [ax1, ax2]

	for index, measure in enumerate(measures):
		coordenadas = datos[measure]
		title = measure
		for index2 , coordenada in enumerate(coordenadas):
			axes[index].plot(x, coordenada, color=colors[index2], linewidth=3.0)
		axes[index].set_title(title)

	legends = ['10%', '20%', '30%', '40%', '50%']
	plt.legend(legends, loc='upper right')


	plt.show()









def draw_five_non_weighted(datos):
	measures = ['pr' ,'dg' ,'sp', 'at' ,'gaccs']	
	x = [0.5, 0.6, 0.7, 0.8, 0.9, 1, 1.1, 1.3, 1.5, 1.7, 1.9]
	colors = ['blue', 'red', 'darkgreen', 'yellow', 'cyan']
	dictionary = dict()
	dictionary['pr'] = 'Page Rank' 
	dictionary['dg'] = 'Degree' 
	dictionary['sp'] = 'Shortest Path'
	dictionary['at'] = 'Absorption Time'
	dictionary['gaccs'] = 'Generalized Accessibility'


	f, (ax1, ax2, ax3, ax4, ax5) = plt.subplots(5, sharex=True, sharey=True)

	axes = [ax1, ax2, ax3, ax4, ax5]

	for index, measure in enumerate(measures):
		coordenadas = datos[measure]
		title = dictionary[measure]
		for index2 , coordenada in enumerate(coordenadas):
			axes[index].plot(x, coordenada, color=colors[index2], linewidth=3.0)
		axes[index].set_title(title)

	legends = ['10%', '20%', '30%', '40%', '50%']
	plt.legend(legends, loc='upper right')

	plt.show()


def get_paper_data():
	dictionary_trad = dict()
	dictionary_trad['dg'] = [0.5469, 0.5482, 0.5400, 0.5528]
	dictionary_trad['stg'] = [0.5453, 0.5390, 0.5433, 0.5552]
	dictionary_trad['sp'] = [0.5441, 0.5438, 0.5432, 0.5509]
	dictionary_trad['sp_w'] = [0.5346, 0.5478, 0.5454, 0.5636]
	dictionary_trad['btw'] = [0.5298, 0.5404, 0.5341, 0.5452]
	dictionary_trad['btw_w'] = [0.4763, 0.4745, 0.4901, 0.4790]
	dictionary_trad['pr'] = [0.5501, 0.5367, 0.5426, 0.5435]
	dictionary_trad['pr_w'] = [0.5458, 0.5460, 0.5471, 0.5605]
	dictionary_trad['cc'] = [0.4151, 0.4266, 0.4270, 0.4424]
	dictionary_trad['cc_w'] = [0.4180, 0.4326, 0.4337, 0.4532]

	dictionary_concentrics = dict()
	dictionary_concentrics['conc_1'] = [0.3999, 0.3957, 0.4171, 0.4083]
	dictionary_concentrics['conc_2'] = [0.3943, 0.3895, 0.4157, 0.4057]
	dictionary_concentrics['conc_3'] = [0.4035, 0.4095, 0.4246, 0.4187]
	dictionary_concentrics['conc_4'] = [0.3919, 0.3858, 0.4115, 0.4068]
	dictionary_concentrics['conc_5'] = [0.4204, 0.4214, 0.4376, 0.4324]
	dictionary_concentrics['conc_6'] = [0.4077, 0.4259, 0.4235, 0.4393]
	dictionary_concentrics['conc_7'] = [0.3989, 0.3730, 0.4116, 0.3934]
	dictionary_concentrics['conc_8'] = [0.4179, 0.4276, 0.4283, 0.4432]

	dictionary_accs = dict()
	dictionary_accs['accs_h2'] = [0.4925, 0.5093, 0.5032, 0.5102]
	dictionary_accs['accs_h3'] = [0.4484, 0.4302, 0.4540, 0.4369]
	dictionary_accs['gaccs'] = [0.5489, 0.5478, 0.5395, 0.5494]

	dictionary_sym = dict()
	dictionary_sym['hsymbb_h2'] = [0.4183, 0.4202, 0.4242, 0.4228]
	dictionary_sym['hsymbb_h3'] = [0.4010, 0.4307, 0.4200, 0.4438]
	dictionary_sym['hsymmg_h2'] = [0.4745, 0.4856, 0.4829, 0.4906]
	dictionary_sym['hsymmg_h3'] = [0.4525, 0.4621, 0.4591, 0.4744]
	dictionary_sym['lsymbb_h2'] = [0.5207, 0.5302, 0.5288, 0.5461]
	dictionary_sym['lsymbb_h3'] = [0.4829, 0.4716, 0.4918, 0.4732]
	dictionary_sym['lsymmg_h2'] = [0.4576, 0.4731, 0.4712, 0.4763]
	dictionary_sym['lsymmg_h3'] = [0.4780, 0.4664, 0.4896, 0.4725]

	dictionary_others = dict()
	dictionary_others['at'] =  [0.5435, 0.5449, 0.5441, 0.5534]

	final_dictionary = dict()
	final_dictionary['trad'] = dictionary_trad
	final_dictionary['conc'] = dictionary_concentrics
	final_dictionary['accs'] = dictionary_accs
	final_dictionary['sym'] = dictionary_sym
	final_dictionary['abst'] = dictionary_others

	return final_dictionary





def get_paper_results(model):
	dg = [0.5469, 0.5482, 0.5400, 0.5528]
	stg = [0.5453, 0.5390, 0.5433, 0.5552]
	sp = [0.5441, 0.5438, 0.5432, 0.5509]
	sp_w = [0.5346, 0.5478, 0.5454, 0.5636]
	sp_w2 = [0.5417, 0.5314, 0.5545, 0.5515]
	btw = [0.5298, 0.5404, 0.5341, 0.5452]
	btw_w = [0.4763, 0.4745, 0.4901, 0.4790]
	pr = [0.5501, 0.5367, 0.5426, 0.5435]
	pr_w = [0.5458, 0.5460, 0.5471, 0.5605]
	cc = [0.4151, 0.4266, 0.4270, 0.4424]
	cc_w = [0.4180, 0.4326, 0.4337, 0.4532]
	conc1 = [0.3999, 0.3957, 0.4171, 0.4083]
	conc2 = [0.3943, 0.3895, 0.4157, 0.4057]
	conc3 = [0.4035, 0.4095, 0.4246, 0.4187]
	conc4 = [0.3919, 0.3858, 0.4115, 0.4068]
	conc5 = [0.4204, 0.4214, 0.4376, 0.4324]
	conc6 = [0.4077, 0.4259, 0.4235, 0.4393]
	conc7 = [0.3989, 0.3730, 0.4116, 0.3934]
	conc8 = [0.4179, 0.4276, 0.4283, 0.4432]
	access_h2 = [0.4925, 0.5093, 0.5032, 0.5102]
	access_h3 = [0.4484, 0.4302, 0.4540, 0.4369]
	gaccs = [0.5489, 0.5478, 0.5395, 0.5494]
	hsymbb_h2 = [0.4183, 0.4202, 0.4242, 0.4228]
	hsymbb_h3 = [0.4010, 0.4307, 0.4200, 0.4438]
	hsymmg_h2 = [0.4745, 0.4856, 0.4829, 0.4906]
	hsymmg_h3 = [0.4525, 0.4621, 0.4591, 0.4744]
	lsymbb_h2 = [0.5207, 0.5302, 0.5288, 0.5461]
	lsymbb_h3 = [0.4829, 0.4716, 0.4918, 0.4732]
	lsymmg_h2 = [0.4576, 0.4731, 0.4712, 0.4763]
	lsymmg_h3 = [0.4780, 0.4664, 0.4896, 0.4725]
	abst = [0.5435, 0.5449, 0.5441, 0.5534]
	measures = [dg, stg, sp, sp_w, sp_w2, btw, btw_w, pr, pr_w, cc, cc_w, conc1, conc2, conc3, conc4,
	conc5, conc6, conc7, conc8, access_h2, access_h3, gaccs, hsymbb_h2, hsymbb_h3, hsymmg_h2, hsymmg_h3,
	lsymbb_h2, lsymbb_h3, lsymmg_h2, lsymmg_h3, abst]

	red_noun = []
	red_tfidf = []
	red_noun_ard = []
	red_tfidf_ard = []

	redes = [red_noun, red_tfidf, red_noun_ard, red_tfidf_ard]

	for i in measures:
		for index , j in enumerate(i):
			redes[index].append(j)

	if model == 4:
		return redes
	else:
		return redes[model]

def paper():
	
	
	
	redes = get_paper_results(4)

	for i in redes:
		print i 

	red_noun = redes[0]
	red_tfidf = redes[1]
	red_noun_ard = redes[2]
	red_tfidf_ard = redes[3]


	
	x = [a+1 for a in range(len(red_noun))]
	measures = ['dg', '\nstg', 'sp', '\nsp_w', 'sp_w2', '\nbtw', 'btw_w', '\npr', 'pr_w', '\ncc', 'cc_w', '\nconc1', 'conc2', '\nconc3', 'conc4',
	'\nconc5', 'conc6', '\nconc7', 'conc8', '\naccs2', 'accs3', '\ngaccs', 'hSymB2', '\nhSymB3', 'hSymM2', '\nhSymM3',
	'lSymB2', '\nlSymB3', 'lSymM2', '\nlSymM3', 'absT']


	legends = ['Noun Network', 'TfIdf Network', 'Noun Network + ARD', 'TfIDf Network + ARD']

 
	#legends2 = ['Red TfIdf', 'Red TfIDf + ARD']
	#legends3 = ['Red Noun', 'Red Noun + ARD']
	#legends4 = ['Red Noun + ARD', 'Red TfIDf + ARD']
	
	#legends2 = ['Noun Network + ARD' , 'TfIdf Network + ARD']
	legends2 = ['TfIdf Network', 'TfIdf Network + ARD']

	#colors = ['blue', 'red', 'darkgreen', 'yellow']
	colors = ['lime', 'red' , 'forestgreen' , 'darkred']



	#redes2 = [red_noun_ard, red_tfidf_ard]
	redes2 = [red_tfidf , red_tfidf_ard]
	#redes3 = [red_noun, red_noun_ard]
	#redes4 = [red_noun_ard, red_tfidf_ard]
	


	for index, red in enumerate(redes2):
		#plt.plot(x, red, '--', color=colors[index], linewidth=3.0)
		plt.scatter(x, red, s=30, c=colors[index])#, alpha=0.5)


	#plt.legend(legends, loc='upper right')
	plt.legend(legends2, loc='lower right')
	plt.xlabel('Network measurements')
	plt.ylabel('ROUGE-1 recall')
	#plt.title('Comparing Noun based network and TfIdf based network')
	plt.title('Comparing anti-redundancy detection (ARD) impact on TfIdf based network')
	plt.xticks(x, measures)
	
	plt.show()


def paper2():
	redes = get_paper_results(4)
	red_tfidf_ard = redes[3]
	measures = ['dg', 'stg', 'sp', 'sp_w', 'sp_w2', 'btw', 'btw_w', 'pr', 'pr_w', 'cc', 'cc_w', 'conc1', 'conc2', 'conc3', 'conc4',
	'conc5', 'conc6', 'conc7', 'conc8', 'accs2', 'accs3', 'gaccs', 'hSymB2', 'hSymB3', 'hSymM2', 'hSymM3',
	'lSymB2', 'lSymB3', 'lSymM2', 'lSymM3', 'absT']

	colors = dict()  ### inserirrr trad

	labels = ['a' , 'a' , 'a' , 'a' ,'a' ,'a' ,'a' ,'a' , 'b' , 'b', 'b', 'b','b','b','b','b', 'c', 'c', 'c', 'c', 'c', 'd'
	, 'd', 'd', 'd', 'd', 'd', 'd', 'd', 'd', 'd']

	unique = list(set(labels))

	colors['dg'] = 'green'
	colors['stg'] = 'green'
	colors['sp'] = 'green'
	colors['sp_w'] = 'green'
	colors ['sp_w2'] = 'green'
	colors['btw'] = 'green'
	colors['btw_w'] = 'green'
	colors['pr'] = 'green'
	colors['pr_w'] = 'green'
	colors['cc'] = 'green'
	colors['cc_w'] = 'green'

	colors['conc1'] = 'red'
	colors['conc2'] = 'red'
	colors['conc3'] = 'red'
	colors['conc4'] = 'red'
	colors ['conc5'] = 'red'
	colors['conc6'] = 'red'
	colors['conc7'] = 'red'
	colors['conc8'] = 'red'

	colors['accs2'] = 'blue'
	colors['accs3'] = 'blue'
	colors['gaccs'] = 'blue'

	colors['hSymB2'] = 'yellow'
	colors['hSymB3'] = 'yellow'
	colors['hSymM2'] = 'yellow'
	colors['hSymM3'] = 'yellow'
	colors['lSymB2'] = 'yellow'
	colors['lSymB3'] = 'yellow'
	colors['lSymM2'] = 'yellow'
	colors['lSymM3'] = 'yellow'

	colors['absT'] = 'black'



	dictionary = dict()
	for key , value in zip(measures, red_tfidf_ard):
		dictionary[key] = value



	sorted_dictionary = sorted(dictionary.items(), key=operator.itemgetter(1), reverse=True)

	sorted_names = []
	sorted_y = []

	for i in sorted_dictionary:
		sorted_names.append(i[0])
		sorted_y.append(i[1])


	color_list = []
	for i in sorted_names:
		color_list.append(colors[i])

	print color_list


	sorted_names_adjusted = []
	index = 0

	for i in sorted_names:
		if index%2 != 0:
			i = '\n' + i
		sorted_names_adjusted.append(i)
		index+=1


	x = [a+1 for a in range(len(sorted_y))]

	

	#plt.scatter(x, sorted_y, s=40, c='green')#, alpha=0.5)
	#plt.scatter(x, sorted_y, s=40, c=color_list, label=labels)#, alpha=0.5)
	
	index = 0
	for val_x , val_y in zip(x, sorted_y):
		plt.scatter(val_x, val_y, s=50, c=color_list[index])#, label=labels[index])
		index+=1
	



	plt.xlabel('Network measurements')
	plt.ylabel('ROUGE-1 recall')
	#plt.title('Comparing anti-redundancy detection (ARD) impact on TfIdf based network')
	#plt.legend(loc='upper right')
	plt.xticks(x, sorted_names_adjusted)

	#plt.grid(True)
	plt.show()



def paper3():
	redes = get_paper_results(4)
	red_tfidf_ard = redes[3]
	measures = ['dg', 'stg', 'sp', 'sp_w', 'sp_w2', 'btw', 'btw_w', 'pr', 'pr_w', 'cc', 'cc_w', 'conc1', 'conc2', 'conc3', 'conc4',
	'conc5', 'conc6', 'conc7', 'conc8', 'accs2', 'accs3', 'gaccs', 'hSymB2', 'hSymB3', 'hSymM2', 'hSymM3',
	'lSymB2', 'lSymB3', 'lSymM2', 'lSymM3', 'absT']

	dictionary = dict()
	for key , value in zip(measures, red_tfidf_ard):
		dictionary[key] = value

	sorted_dictionary = sorted(dictionary.items(), key=operator.itemgetter(1), reverse=True)

	sorted_names = []
	sorted_y = []

	for i in sorted_dictionary:
		sorted_names.append(i[0])
		sorted_y.append(i[1])
	
	clases = ['Traditional', 'Traditional', 'Traditional', 'Absorption Time', 'Traditional', 
	'Traditional', 'Traditional', 'Accessibility', 'Symmetry', 'Traditional', 'Traditional', 
	'Accessibility', 'Symmetry', 'Traditional', 'Symmetry','Symmetry','Symmetry','Symmetry',
	'Traditional', 'Symmetry', 'Concentric', 'Traditional', 'Concentric', 'Accessibility', 
	'Concentric', 'Symmetry', 'Concentric','Concentric','Concentric','Concentric','Concentric']

	unique = list(set(clases))

	sorted_names_adjusted = []
	index = 0

	for i in sorted_names:
		if index%2 != 0:
			i = '\n' + i
		sorted_names_adjusted.append(i)
		index+=1


	x = [a+1 for a in range(len(sorted_y))]
	colors = ['green', 'blue', 'red',  'darkorange', 'blueviolet']
	print x 
	print sorted_names
	print sorted_y
	print unique

	for i, u in enumerate(unique):
		xi = [x[j] for j  in range(len(x)) if clases[j] == u]
		yi = [sorted_y[j] for j  in range(len(x)) if clases[j] == u]
		plt.scatter(xi,yi,s=60,c=colors[i], label=str(u))
	plt.legend()
	plt.xticks(x, sorted_names_adjusted)
	plt.title('Comparing network measurements for TfIdf based network')
	plt.xlabel('Network measurements')
	plt.ylabel('ROUGE-1 recall')
	plt.show()  
		

 


def test():

	data = get_paper_data()
	traditionals = data['trad']
	concentrics = data['conc']
	access = data['accs']
	sym = data['sym']
	at = data['abst']


	means_noun = []
	means_tfidf = []
	means_noun_ard = []
	means_tfidf_ard = []
	x_labels = []

	#for i in traditionals:
	for i in sym:
		x_labels.append(i)
		#data = traditionals[i]
		data = sym[i]
		means_noun.append(data[0])
		means_tfidf.append(data[1])
		means_noun_ard.append(data[2])
		means_tfidf_ard.append(data[3])


	labels = ['Noun', 'TfIdf', 'Noun + ARD', 'TfIdf + ARD']

	
	#n_groups = len(traditionals)
	n_groups = len(sym)
	fig, ax = plt.subplots()
	index = np.arange(n_groups)
	bar_width = 0.15
	opacity = 0.9

	rects1 = plt.bar(index, means_noun, bar_width, alpha=opacity, color='b', label=labels[0])
	rects2 = plt.bar(index + bar_width, means_tfidf, bar_width, alpha=opacity, color='g', label=labels[1])
	rects3 = plt.bar(index + 2*bar_width, means_noun_ard, bar_width, alpha=opacity, color='r', label=labels[2])
	rects4 = plt.bar(index + 3*bar_width, means_tfidf_ard, bar_width, alpha=opacity, color='y', label=labels[3])

	plt.xlabel('Measurements')
	plt.ylabel('Rouge')
	plt.title('Scores ???')
	#plt.xticks(index + bar_width, ('A', 'B', 'C', 'D', 'E', 'F', 'G', 'H'))
	plt.xticks(index + bar_width, x_labels)
	plt.legend(loc='upper right')
 
	plt.tight_layout()
	plt.show()







	'''
	n_groups = 8
	means_frank = [90, 55, 40, 65, 20, 70, 1, 23]
	means_guido = [85, 62, 54, 20, 5, 46, 2, 100]
	means_jorge = [95, 80, 90, 65, 10, 50, 3, 56]
	means_andoni = [75, 10, 50, 35, 23, 35, 4, 9]

	# create plot
	fig, ax = plt.subplots()
	index = np.arange(n_groups)
	bar_width = 0.15
	opacity = 0.9

	print index

	rects1 = plt.bar(index, means_frank, bar_width, alpha=opacity, color='b', label='Frank')
	rects2 = plt.bar(index + bar_width, means_guido, bar_width, alpha=opacity, color='g', label='Guido')
	rects3 = plt.bar(index + 2*bar_width, means_jorge, bar_width, alpha=opacity, color='r', label='Jorge')
	rects4 = plt.bar(index + 3*bar_width, means_andoni, bar_width, alpha=opacity, color='y', label='Andoni')

	plt.xlabel('Person')
	plt.ylabel('Scores')
	plt.title('Scores by person')
	plt.xticks(index + bar_width, ('A', 'B', 'C', 'D', 'E', 'F', 'G', 'H'))
	plt.legend(loc='upper right')
 
	plt.tight_layout()
	plt.show()
	'''




		



if __name__ == '__main__':


	#test()

	#paper()

	#paper2()

	paper3()

	
	
	#test = 'CSTNews/1_2_best_rivaldo_AB.csv'
	#test2 = 'CSTNews/3_4_best_ngram_AB.csv'

	#test = 'DUC2002/1_2_best_rivaldo_AB.csv'
	#test2 = 'DUC2002/3_4_best_ngram_AB.csv'

	#test = 'DUC2004/1_2_best_rivaldo_AB.csv'
	#test2 = 'DUC2004/3_4_best_ngram_AB.csv'

	#test = 'CSTNews/symmetry_ribaldo.csv'
	#test = 'DUC2002/symmetry_ribaldo_accs.csv'
	#test = 'DUC2004/symmetry_ribaldo_accs.csv'


	#test = 'CSTNews/accessibility_ribaldo.csv'




	
	#datos_rivaldo = read_file(test)
	#datos_ngrams = read_file(test2)

	
	#'pr' 'dg' 'sp' 'at' 'gaccs'
	#'pr_w' 'stg' 'sp_w'

	#draw('pr' , datos_rivaldo)

	#draw_weighted(datos_rivaldo, datos_ngrams)

	#draw_four_non_weighted('at', datos_rivaldo , datos_ngrams)

	#draw_five_non_weighted(datos)

	#symmetry_analysis('h3', datos_rivaldo) # m b h2 h3 L H 
	#symmetry_second_analysis(datos_rivaldo) # m b h2 h3 L H 

	##accessibility_analysis(datos_rivaldo)


	'''
	- tabla o gragico , puede ser barras para mostrar las mejores medidas con sus parametros
	- ejemplo: (degree,  inter=weight, limiar)
	- manetener solo un grafico de los 3 corpus, el que considere mejor
	- mejorar la calibracion para q este mas clara 

	- indiana,, university di indiana

	isaias 45,2-3

	

	


	
	'''
	





