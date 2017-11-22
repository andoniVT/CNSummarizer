import matplotlib.pyplot as plt
import numpy as np
from pylab import *

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


def barras(data):
	means_noun = []
	means_tfidf = []
	means_noun_ard = []
	means_tfidf_ard = []
	x_labels = []

	for i in data:
		x_labels.append(i)
		values = data[i]
		means_noun.append(values[0])
		means_tfidf.append(values[1])
		means_noun_ard.append(values[2])
		means_tfidf_ard.append(values[3])

	labels = ['Noun', 'TfIdf', 'Noun + ARD', 'TfIdf + ARD']

	n_groups = len(data)
	fig, ax = plt.subplots()
	index = np.arange(n_groups)
	bar_width = 0.15
	opacity = 0.9

	

	#rects1 = plt.bar(index, means_noun, bar_width, alpha=opacity, color='b', label=labels[0])
	rects2 = plt.bar(index + bar_width, means_tfidf, bar_width, alpha=opacity, color='g', label=labels[1])
	#rects3 = plt.bar(index + 2*bar_width, means_noun_ard, bar_width, alpha=opacity, color='r', label=labels[2])
	rects4 = plt.bar(index + 3*bar_width, means_tfidf_ard, bar_width, alpha=opacity, color='y', label=labels[3])


	plt.xlabel('Measurements')
	plt.ylabel('Rouge')
	plt.title('Scores ???')
	plt.xticks(index + bar_width, x_labels)
	plt.legend(loc='lower right')
	plt.tight_layout()
	plt.show()
		


	

#if __name__ == '__main__':

import matplotlib.pyplot as plt

x=[1,2,3,4]
y=[5,6,7,8]
classes = [2,4,4,2]
unique = list(set(classes))

colors = ['green', 'red', 'blue', 'yellow', 'black']

print unique 
print ''
for i, u in enumerate(unique):
    xi = [x[j] for j  in range(len(x)) if classes[j] == u]
    yi = [y[j] for j  in range(len(x)) if classes[j] == u]
    print xi , yi 

    plt.scatter(xi, yi, c=colors[i], label=str(u))
plt.legend()

plt.show()








