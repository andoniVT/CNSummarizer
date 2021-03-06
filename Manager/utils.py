import codecs
import unicodedata
from nltk import word_tokenize , sent_tokenize
import string
import xml.etree.ElementTree as ET
import re
import cPickle
from random import shuffle, choice
from collections import Counter
from gensim import matutils
from scipy import spatial
from configuration import extras, final_results, some_parameters
from igraph import *
from subprocess import call
import subprocess
#import random
#random.choice
import os
import shutil
import matplotlib.pyplot as plt
import numpy as np
from pylab import *
import csv
from sklearn.feature_extraction.text import CountVectorizer
import nltk
from scipy.spatial import distance

def write_data_to_disk(file, data):
    with open(file, 'wb') as fid:
        cPickle.dump(data, fid)

def load_data_from_disk(file):
    with open(file, 'rb') as fid:
        data = cPickle.load(fid)
    return data

def parameter_extractor(network_type, data):
    parameters = dict()
    size_parameter = len(data)

    mln_type = None
    sw_removal = None
    limiar_value = None
    limiar_type = None
    size_d2v = None
    inter_edge = None
    intra_edge = None

    '''
    dictionary['network'] = ('mln', ['noun', [1.7, 1.9], [0.4, 0.45, 0.5]]) # size:3
    dictionary['network'] = ('mln', ['tfidf', [1.7, 1.9], [0.4, 0.45, 0.5]])  # inter - limiar remocion  # size:3
    dictionary['network'] = ('mln', ['d2v', False, ('limiar', [0.3]), 300, [1.7, 1.9], [0.4, 0.45, 0.5]])  # size:6
    '''

    if network_type == 'mln':
        mln_type = data[0]
        if size_parameter == 6:
            sw_removal = data[1]
            limiar_type = data[2][0]
            limiar_value = data[2][1]
            size_d2v = data[3]
            inter_edge = data[4]
            intra_edge = data[5]
        else:
            inter_edge = data[1]
            intra_edge = data[2]
    else:
        # []  0
        # [('limiar', [0.10, 0.15])]  1
        # [False, ('limiar', [0.15]), 200]  3
        if size_parameter != 0:
            if size_parameter == 3:
                sw_removal = data[0] #ok
                limiar_type = data[1][0]
                limiar_value = data[1][1]
                size_d2v = data[2]
            else:
                limiar_type = data[0][0]
                limiar_value = data[0][1]
            #distance = data[2]
            #if size_parameter == 5:
            #    size_d2v = data[3]
            #    inference_d2v = data[4]

    parameters['mln_type'] = mln_type
    parameters['sw_removal'] = sw_removal
    parameters['limiar_type'] = limiar_type
    parameters['limiar_value'] = limiar_value
    #parameters['distance'] = distance
    parameters['size_d2v'] = size_d2v
    #parameters['inference_d2v'] = inference_d2v
    parameters['inter_edge'] = inter_edge
    #parameters['intra_edge'] = intra_edge
    parameters['limiar_mln'] = intra_edge

    return parameters

def read_document(file, language='ptg'):
    document = codecs.open(file, encoding="utf-8", errors='ignore')
    #document = codecs.open(file, encoding="utf-8")
    content = ""
    for i in document:
        i = i.rstrip()
        i = unicodedata.normalize('NFKD', i).encode('ascii', 'ignore')
        content += i + " "

    content = content[:-1]
    content = " ".join(content.split())
    if language == 'ptg':
        sentences = sent_tokenize(content, language='portuguese')
    else:
        sentences = sent_tokenize(content, language='english')
    return sentences

def read_document_extract_cst(file, language='ptg'):
    sentences = read_document(file, language)
    new_sentences = []
    new_sentences.append(sentences[0])
    for i in range(1,len(sentences)):
        sent = sentences[i]
        sent = sent[sent.find('>')+2:]
        if len(sent)!= 0:
            new_sentences.append(sent)
    return new_sentences




def remove_portuguese_caracteres(sentence):
    news = []
    for word in sentence:
        news.append(unicodedata.normalize('NFKD', word).encode('ascii', 'ignore'))
    return news


def wordCountString(source):
    for c in string.punctuation:
        source =source.replace(c, "")
    return len(word_tokenize(source))


def count_words(file, language):
	sentences = read_document(file, language)
	words=0
	for i in sentences:
		words+= wordCountString(i)
	return words


def clean_sentences(sentences):
    result = []
    signos = '`"\''
    for i in sentences:
        i = i.replace('\n', ' ')
        for c in signos:
            i = i.replace(c, "")
        result.append(i)
    return result

def read_document_english(document):
    data = ""
    tree = ET.parse(document)
    root = tree.getroot()
    for i in root.iter('TEXT'):
        data+= i.text + " "
    data = re.sub("\s\s+", " ", data)
    data = ''.join(data)
    data = " ".join(data.split())

    sentences = sent_tokenize(data)
    sentences = clean_sentences(sentences)

    return sentences

def permutate_data(data):
    shuffle(data)
    return data

def has_common_elements(vec, vec2):
    value = 0
    for i in vec:
        if i in vec2:
            value+=1
    return value


def cosineSimilarity(sentence1, sentence2):
   a_vals = Counter(sentence1)
   b_vals = Counter(sentence2)
   words = list(set(a_vals) | set(b_vals))
   a_vect = [a_vals.get(word, 0) for word in words]
   b_vect = [b_vals.get(word, 0) for word in words]
   len_a = sum(av * av for av in a_vect) ** 0.5
   len_b = sum(bv * bv for bv in b_vect) ** 0.5
   dot = sum(av * bv for av, bv in zip(a_vect, b_vect))
   cosine = dot / (len_a * len_b)
   return cosine

'''
        return matutils.cossim(vec_tfidf, vec_tfidf2)  gemsim
        from scipy import spatial
        return 1 - spatial.distance.cosine(vec_sentence1, vec_sentence2)  doc2vec
        '''

#def calculate_similarity(vec_sentence1 , vec_sentence2, network_type, distance_method):
def calculate_similarity(vec_sentence1 , vec_sentence2, network_type):
    embeddings = ['d2v', 'gd2v', 'fastT', 'gloVe', 's2v']
    if network_type=='tfidf':
        return matutils.cossim(vec_sentence1, vec_sentence2)
    #if network_type=='d2v' or network_type=='gd2v':
    if network_type in embeddings:
        return 1 - spatial.distance.cosine(vec_sentence1, vec_sentence2)



def euclidian_similarity(vec_sentence1 , vec_sentence2):
    print vec_sentence1
    print vec_sentence2
    print  1/float(1 + distance.euclidean(vec_sentence1, vec_sentence2))

def calculate_similarity_v2(vec_sentence1 , vec_sentence2, network_type):
    return 1/float(1 + distance.euclidean(vec_sentence1, vec_sentence2))


def sortList(vector):
    return [i[0] for i in sorted(enumerate(vector), key=lambda x:x[1])]


def specialSortList(vector):
    return vector[::-1]

def reverseSortList(vector):
    return [i[0] for i in sorted(enumerate(vector), key=lambda x:x[1], reverse=True)]


def average(lenghts):
    result = 0.0
    N = len(lenghts)
    for i in lenghts:
        if i == float('inf'):
            N-=1
        else:
            result+=i
    if result == 0:
        return 99999
    else:
        return result/N

'''
['dg', 'gaccs', 'accs_h2', 'ccts', 'sym']
['dg', 'pr', 'accs_h2', 'ccts_2_h2', 'sym_h_b_h3']
'''


def find_term(measures, parameter):
    for i in measures:
        if i.find(parameter)!=-1:
            return True
    return False



def manage_vector(measures, parameter):
    print "managing vector measures"
    #parameter = 'ccts'
    allConcentrics = parameter in measures
    if allConcentrics:
        print "todasssss"
        return measures

    others = []
    concentrics = ""

    for i in measures:
        if i.find(parameter)!=-1:
            i = i[i.find('_')+1:]
            concentrics+=i + "_"
        else:
            others.append(i)
    concentrics = concentrics[:-1]
    concentrics = parameter + '_' + concentrics
    others.append(concentrics)
    return others

def save_file(data, file_name):
	with codecs.open(file_name , "w" , "utf-8" , errors='replace') as temp:
		temp.write(data)

def generate_net(graph):
    location = extras['NetAux']
    graph.write_pajek(location)
    #print location


def generate_xnet(graph):
    result = "#vertices " + str(graph.vcount()) + " nonweighted \n"
    result = result + "#edges nonweighted undirected \n"
    lista = graph.get_edgelist()
    for i in lista:
        edge = str(i[0]) + " " + str(i[1]) + "\n"
        result = result + edge
    save_file(result, extras['XNetAux'])



def execute_concentric(command):
    # tener cuidado,, single ok ,, multi noseeeee
    #print command
    sub_espace = command[command.find('..'):]
    sub_espace = sub_espace[:sub_espace.rfind('..') - 1]
    first_part = command[:command.find('..') - 1]
    second_part = command[command.rfind('..'):]
    values = first_part.split(' ')
    values.append(sub_espace)
    values.extend(second_part.split(' '))
    call(values)

def execute_symmetry(command):
    # os.system(command)  # cuando es singleeeeeeeeeeeeeeeee

    sub_espace = command[command.find('..'):]
    sub_espace = sub_espace[:sub_espace.rfind('..')-1]
    first_part = command[:command.find('..')-1]
    second_part = command[command.rfind('..'):]
    values = first_part.split(' ')
    values.append(sub_espace)
    values.append(second_part)
    print values
    call(values)


def  read_dat_file(file):
    h2 = []
    h3 = []
    file = open(file)
    for i in file:
        i = i.rstrip("\n")
        values = i.split(' ')
        values = values[:len(values)-1]
        if 2 < len(values):
            h2.append(float(values[2]))
        else:
            h2.append(0.0)
        if 3 < len(values):
            h3.append(float(values[3]))
        else:
            h3.append(0.0)
    return [h2, h3]

def read_dat_files():
    base = extras['FolderAux']
    result = []
    for i in range(8):
        file =  base + 'OutNet_hier' + str(i+1) + '.dat'
        result.append(read_dat_file(file))
    return result


def read_csv_file():
    base = extras['CSVAux']
    file = open(base, 'r')
    aux=0
    backbone_h2 = []
    merged_h2 = []
    backbone_h3 = []
    merged_h3 = []
    for i in file:
        i = i.rstrip("\n")
        i = " ".join(i.split())
        if aux!=0:
            values = i.split(" ")
            backbone_h2.append(float(values[0]))
            merged_h2.append(float(values[1]))
            backbone_h3.append(float(values[2]))
            merged_h3.append(float(values[3]))
        aux+=1
    return [[backbone_h2, backbone_h3] , [merged_h2,  merged_h3]]

def get_terminal_values(command):
    #values = command.split(' ')  ### cuando es single !!!!!!!!!!

    sub_space = command[command.rfind('/')+1:]
    sub_normal = command[:command.rfind('/')+1]
    values = sub_normal.split(' ')
    values[3] = values[3] + sub_space

    output = subprocess.Popen(values, stdout=subprocess.PIPE).communicate()[0]
    #print 'test' , output
    return output


def inverse_weights(weights):
    nuevo = []
    nuevo2 = []
    maximo = max(weights)
    for i in weights:
        if i==0:
            nuevo.append(0)
            nuevo2.append(0)
        else:
            nuevo.append(maximo-i+1)
            nuevo2.append(1/float(i))

    return [nuevo, nuevo2]


def remove_punctuation(sentence):
    for c in string.punctuation:
        sentence = sentence.replace(c,"")
    return sentence


def selectSentencesSingle(sentences, measures, resumo_size):
    limit = 0
    result = []
    name_measure = measures[0]
    ranked = measures[1]
    for index, sents in enumerate(sentences):
        index_selected = ranked[index]
        selected = sentences[index_selected]
        result.append(selected)
        selected = remove_punctuation(selected)
        #result.append(selected)
        limit+=len(word_tokenize(selected))
        if limit > resumo_size:
            break
    return (name_measure,result)

def selectSentencesSingle_bytes(sentences, measures, resumo_size):
    limit = 0
    result = []
    name_measure = measures[0]
    ranked = measures[1]
    for index, sents in enumerate(sentences):
        index_selected = ranked[index]
        selected = sentences[index_selected]
        result.append(selected)
        limit += len(selected)
        if limit > resumo_size:
            break

    result = remove_extra_caracters(result)
    #print 'summary size: ', get_size_sentences(result)
    return (name_measure, result)


def isRedundant(index, psentences, selected, limit):
    actual_sentence = psentences[index]
    for i in selected:
        sentence = psentences[i]
        similarity = cosineSimilarity(actual_sentence, sentence)  ##### verificar si aplicando los vectores ya calculado faz diferencia
        if similarity > limit:
            return True
    return False

def extract_only_sentences(sentences):
    result = []
    for i in sentences:
        result.append(i[0])
    return result


def selectSentencesMulti_ribaldo(sentences, ranking, resumo_size, threshold, pSentences):
    selected = []
    name_measure = ranking[0]
    ranked = ranking[1]
    initial_index = ranked[0]
    selected.append(initial_index)
    sentences_sin_punct = remove_punctuation(sentences[initial_index])
    pSentences = extract_only_sentences(pSentences)

    size_sentence = len(word_tokenize(sentences_sin_punct))
    for i in range(1, len(ranked)):
        index = ranked[i]
        if not isRedundant(index, pSentences, selected, threshold):
            selected.append(index)
            #selected = remove_punctuation(selected)
            #auxi = sentences[index]
            sentences_sin_punct = remove_punctuation(sentences[index])
            #size_sentence+= len(word_tokenize(sentences[index]))
            size_sentence += len(word_tokenize(sentences_sin_punct))

        if size_sentence > resumo_size:
            break

    selected_sentences = []
    for i in range(len(selected)):
        index = selected[i]
        sentence = sentences[index]
        selected_sentences.append(sentence)

    return (name_measure, selected_sentences)


def get_size_sentences(sentences):
    size = 0
    for i in sentences:
        size+=len(i)
    return size

def remove_extra_caracters(sentences):
    size = 0
    for i in range(len(sentences) - 1):
        size += len(sentences[i])

    final_sentence = sentences[-1]
    sentences.pop()
    new_size = 665 - size
    new_sentence = final_sentence[:new_size]
    sentences.append(new_sentence)
    return sentences



def selectSentencesMulti_ribaldo_bytes(sentences, ranking, resumo_size, threshold, pSentences):
    print 'waaaaaa!'
    selected = []
    name_measure = ranking[0]
    ranked = ranking[1]
    initial_index = ranked[0]
    selected.append(initial_index)
    pSentences = extract_only_sentences(pSentences)
    #size_sentence = len(word_tokenize(sentences_sin_punct))
    size_sentence = len(sentences[initial_index])
    for i in range(1, len(ranked)):
        index = ranked[i]
        if not isRedundant(index, pSentences, selected, threshold):
            selected.append(index)
            #selected = remove_punctuation(selected)
            #auxi = sentences[index]
            sentences_sin_punct = remove_punctuation(sentences[index])
            #size_sentence+= len(word_tokenize(sentences[index]))
            size_sentence += len(sentences[index])

        if size_sentence > resumo_size:
            break

    selected_sentences = []
    for i in range(len(selected)):
        index = selected[i]
        sentence = sentences[index]
        selected_sentences.append(sentence)

    #print 'summary size: ' , get_size_sentences(selected_sentences)
    selected_sentences = remove_extra_caracters(selected_sentences)
    return (name_measure, selected_sentences)


def n_gram_sim(sentence1 , sentence2):
    N = 4
    weights = [0.1 , 0.2 , 0.3 , 0.4]
    similarity = 0
    for i in range(N):
        ngrams_s1 = nltk.ngrams(sentence1.split(), i+1)
        conjunto_s1 = set()
        for j in ngrams_s1:
            grama = extract_gramas(j)
            conjunto_s1.add(grama)
        ngrams_s2 = nltk.ngrams(sentence2.split(), i+1)
        conjunto_s2 = set()
        for j in ngrams_s2:
            grama = extract_gramas(j)
            conjunto_s2.add(grama)
        union = conjunto_s1 | conjunto_s2
        interseccion = conjunto_s1 & conjunto_s2
        similarity += weights[i] * (len(interseccion) /float(len(union)))
    return similarity


def special_proccesing_sentence(sentence):
    text = sentence.lower()
    for c in string.punctuation:
        text = text.replace(c, '')
    text = ''.join([i for i in text if not i.isdigit()])
    return text


def isRedundantNgrams(index, sentences, selected):
    threshold_ngrams = 0.1
    actual_sentence = sentences[index]
    actual_sentence = special_proccesing_sentence(actual_sentence)
    for i in selected:
        sentence = sentences[i]
        sentence = special_proccesing_sentence(sentence)
        similarity = n_gram_sim(actual_sentence, sentence)
        if similarity >= threshold_ngrams:
            #print actual_sentence
            #print sentence
            #print similarity
            #print ''
            return True
    return False




def selectSentencesMulti_ngrams(sentences, ranking, resumo_size):
    selected = []
    name_measure = ranking[0]
    ranked = ranking[1]
    initial_index = ranked[0]
    selected.append(initial_index)
    sentences_sin_punct = remove_punctuation(sentences[initial_index])
    size_sentence = len(word_tokenize(sentences_sin_punct))



    for i in range(1, len(ranked)):
        index = ranked[i]
        isRedundantNgrams(index, sentences, selected)
        if not isRedundantNgrams(index, sentences, selected):
            selected.append(index)
            sentences_sin_punct = remove_punctuation(sentences[index])
            size_sentence += len(word_tokenize(sentences_sin_punct))

        if size_sentence > resumo_size:
            break

    selected_sentences = []
    for i in range(len(selected)):
        index = selected[i]
        sentence = sentences[index]
        selected_sentences.append(sentence)
    return (name_measure, selected_sentences)


def selectSentencesMulti_ngrams_bytes(sentences, ranking, resumo_size):
    selected = []
    name_measure = ranking[0]
    ranked = ranking[1]
    initial_index = ranked[0]
    selected.append(initial_index)
    size_sentence = len(sentences[initial_index])
    for i in range(1, len(ranked)):
        index = ranked[i]
        if not isRedundantNgrams (index, sentences, selected):
            selected.append(index)
            size_sentence += len(sentences[index])
        if size_sentence > resumo_size:
            break

    selected_sentences = []
    for i in range(len(selected)):
        index = selected[i]
        sentence = sentences[index]
        selected_sentences.append(sentence)

    # print 'summary size: ' , get_size_sentences(selected_sentences)
    selected_sentences = remove_extra_caracters(selected_sentences)
    return (name_measure, selected_sentences)


def selectSentencesMulti(sentences, ranking, resumo_size, anti_redundancy, threshold, pSentences):


    if anti_redundancy==0:
        print "Seleccion sin anti-redundancia"
        if resumo_size == 665:
            return selectSentencesSingle_bytes(sentences, ranking, resumo_size)
        else:
            return selectSentencesSingle(sentences, ranking, resumo_size)
    elif anti_redundancy==1:
        print "Seleccion Rivaldo"
        if resumo_size == 665: # resumo size in words
            return selectSentencesMulti_ribaldo_bytes(sentences, ranking, resumo_size, threshold, pSentences)
        else:
            return selectSentencesMulti_ribaldo(sentences, ranking, resumo_size, threshold, pSentences)

    elif anti_redundancy==2:
        print "Seleccion Ngrams"
        if resumo_size == 665:
            return selectSentencesMulti_ngrams_bytes(sentences, ranking, resumo_size)
        else:
            return selectSentencesMulti_ngrams(sentences, ranking, resumo_size)




def folder_creation(dictionary_rankings, type):
    #random.choice
    print dictionary_rankings.keys()
    #key = random.choice(dictionary_rankings.keys())
    key = choice(dictionary_rankings.keys())
    dict_measures = dictionary_rankings[key]
    measures = []
    for i in dict_measures[0].items(): #### modificacion aqui ,
        measures.append(i[0])
    #measures.append('random')
    #measures.append('top')

    #if type is None:
    #    measures.append('top')
    index = 1

    for i in range(len(dict_measures)):
        for j in measures:
            path = extras['Automatics'] + str(index) + '/' + j
            if not os.path.exists(path):
                os.makedirs(path)
            #print path
        index+=1


    ''' 
    for i in measures:
        #path = "Automatic/" + i
        path = extras['Automatics'] + i
        print path
        #if not os.path.exists(path):
        #    os.makedirs(path)
    '''


'''
file = codecs.open('PRUEBA.txt',  'w', 'utf-8')
for i in sentences:
    file.write(i + '\n')
'''


def saveSummary(location, summary_sentences):
    file = open(location, 'w')
    #file = codecs.open(location, 'w', 'utf-8')
    for i in summary_sentences:
        file.write(i + "\n")


def summary_creation(resumo_name, selected_sentences, index):
    print "Generacion de sumarios en file"
    print resumo_name
    location = extras['Automatics'] + str(index) + '/'
    for i in selected_sentences.items():
        measure = i[0]
        sentences = i[1]
        path = location + measure + '/' + resumo_name
        print path
        saveSummary(path, sentences)



def summary_random_top_creation(resumo_name, sentences, resumo_size):
    print "Creando random y top baseline for SDS"
    ranking_top = [x for x in range(len(sentences))]
    ranking_random = ranking_top[:]
    shuffle(ranking_random)

    #path = "Automatic/top/" + resumo_name
    path = extras['Automatics'] + 'top/' + resumo_name
    path2 = extras['Automatics'] + 'random/' + resumo_name

    measures = ('top' , ranking_top)
    sentences_top = selectSentencesSingle(sentences, measures, resumo_size)[1]

    measures2 = ('random', ranking_random)
    sentences_random = selectSentencesSingle(sentences, measures2, resumo_size)[1]

    saveSummary(path, sentences_top)
    saveSummary(path2, sentences_random)



def summary_random_top_creation_mds(resumo_name, sentences, resumo_size, top_sentences):
    print "Creando random y top baseline for MDS"
    ranking_top = [x for x in range(len(sentences))]
    ranking_random = ranking_top[:]
    random.shuffle(ranking_random)
    path = extras['Automatics'] + 'random/' + resumo_name
    measures = ('random', ranking_random)
    sentences_random = selectSentencesSingle(sentences, measures, resumo_size)[1]
    saveSummary(path, sentences_random)

    ranking_top2 = [x for x in range(len(top_sentences))]
    ranking_random2 = ranking_top2[:]
    random.shuffle(ranking_random2)
    path2 = extras['Automatics'] + 'top/' + resumo_name
    measures2 = ('top', ranking_random2)
    sentences_top = selectSentencesSingle(top_sentences, measures2, resumo_size)[1]
    saveSummary(path2, sentences_top)




def deleteFiles(type):
    files = os.listdir(type)
    for f in files:
        os.remove(type +f)

def delete_dsStore(vector):
    special = '.DS_Store'
    if special in vector: vector.remove(special)
    return vector


def deleteFolders(location):
    files = os.listdir(location)
    files = delete_dsStore(files)
    for f in files:
        shutil.rmtree(location + f)




def get_csv_values(file):
    avg_precision = 0
    avg_recall = 0
    avg_fmeasure = 0
    doc = open(file, 'r')
    index = 0
    for i in doc:
        if index != 0:
            fila = i.split(',')
            recall = float('0.' + fila[4])
            precision = float('0.' + fila[6])
            fmeasure = float('0.' + fila[8])
            avg_recall += recall
            avg_precision += precision
            avg_fmeasure += fmeasure
        index += 1
    print index
    return round(avg_precision / (index - 1), 4), round(avg_recall / (index - 1), 4), round(avg_fmeasure / (index - 1),
                                                                                            4)


def sort_results(matrix):
    dictionary = dict()
    dictionary_positions = dict()
    pos = 0
    for i in matrix:
        dictionary[i[0]] = i[2]
        dictionary_positions[i[0]] = pos
        pos+=1
    sorted_x = sorted(dictionary.items(), key=operator.itemgetter(1), reverse=True)
    ordered_matrix = []
    titles = ['MEASURE', 'P', 'R', 'F']
    ordered_matrix.append(titles)
    for i in sorted_x:
        key = i[0]
        position = dictionary_positions[key]
        ordered_matrix.append(matrix[position])

    return ordered_matrix

def sort_network(edges, weights):
	dictionary = dict()
	for index,  edge in  enumerate(edges):
		key = str(edge[0]) + '-' +str(edge[1])
		dictionary[key] = weights[index]
	sorted_x = sorted(dictionary.items(), key=operator.itemgetter(1), reverse=True)
	return sorted_x


def draw_graph(g):
    size  = g.vcount()
    vec = [x for x in range(size)]
    layout = g.layout("kk")
    visual_style = {}
    visual_style["vertex_label"] = vec
    visual_style["vertex_size"] = 15
    visual_style["layout"] = layout
    visual_style["bbox"] = (800, 600)
    visual_style["margin"] = 70
    plot(g, **visual_style)


def get_weights(edgesList, weight_list):
    dictionary = dict()
    for index in range(len(edgesList)):
        edge = edgesList[index]
        weight = weight_list[index]
        key = str(edge[0]) + '-' + str(edge[1])
        dictionary[key] = weight
    return dictionary

def get_class_label(sentence, dictionary):
    if sentence in dictionary:
        return True
    else:
        return False

def tag_sentence(document_sentences, index, class_labels = None):
    tagged = []
    if class_labels is not None:
        for i in document_sentences:
            tagged.append((i , index, get_class_label(i, class_labels)))
    else:
        for i in document_sentences:
            tagged.append((i , index, None))
    return tagged



def naive_tag(document_sentences, class_labels = None):
    tagged = []
    if class_labels is not None:
        for i in document_sentences:
            tagged.append((i, None, get_class_label(i,class_labels)))
    else:
        for i in document_sentences:
            tagged.append((i, None, None))
    return tagged

def vector_normalize(lista):
    normalized = []
    maximo = max(lista)
    for i in lista:
        value = i/float(maximo)
        normalized.append(value)
    return normalized

def assign_mln_weight(normalized, flag_list, inter, intra):
    weights = []
    for i in range(len(normalized)):
        if flag_list[i]:
            weights.append(normalized[i]*intra)
        else:
            weights.append(normalized[i]*inter)
    return weights

def generate_comparative_graphic(matrix, x):
    plt.plot(x, matrix[0], color='blue', linewidth=3.0)  ##4.0
    plt.plot(x, matrix[1], color='red', linewidth=3.0)
    plt.plot(x, matrix[2], color='darkgreen', linewidth=3.0)  ## 2.0
    plt.plot(x, matrix[3], color='black', linewidth=3.2)
    plt.plot(x, matrix[4], color='yellow', linewidth=3.3)  ## 6.0
    plt.plot(x, matrix[5], color='brown', linewidth=3.0)
    plt.plot(x, matrix[6], color='cyan', linewidth=3.0)  ## 8.0
    plt.plot(x, matrix[7], color='m', linewidth=3.3)
    plt.plot(x, matrix[8], color='y', linewidth=3.0)
    plt.plot(x, matrix[9], color='deeppink', linewidth=3.0)

    plt.ylim(0.450, 0.480)
    plt.legend(['dg', 'stg', 'pr', 'pr_w', 'sp', 'sp_w', 'gaccs', 'at', 'kats', 'btw'], loc='upper right')
    plt.xlabel('Number of removed edges (%)')
    # plt.xlabel('K (3-19)')
    # plt.xlabel('K (3-21)')
    plt.ylabel('Rouge Recall')
    plt.title('Portuguese SDS - Limiares')
    # plt.title('Portuguese SDS - Knn network')
    # plt.title('Portuguese MDS - Limiares')
    # plt.title('Portuguese MDS - Knn network')
    plt.show()


'''
def sort_results(matrix):
    pos = 0
    dictionary = dict()
    dictionary_positions = dict()
    for i in matrix:
        dictionary[i[0]] = i[2]
        dictionary_positions[i[0]] = pos
        pos+=1
    sorted_x = sorted(dictionary.items(), key=operator.itemgetter(1), reverse=True)
    ordered_matrix = []
    titles = ['MEASURE', 'P', 'R', 'F']
    ordered_matrix.append(titles)
    for i in sorted_x:
        key = i[0]
        position = dictionary_positions[key]
        ordered_matrix.append(matrix[position])

    return ordered_matrix
'''

def sort_recall_results(results):
    dictionary = dict()
    for i in results:
        element = i[0]
        dictionary[element[0]] = element[1]
    sorted_x = sorted(dictionary.items(), key=operator.itemgetter(1), reverse=True)
    return sorted_x



def generate_excel_simple(excel_name, results):
    print 'Generating Excel Simple Version'
    print excel_name
    results_sorted = sort_recall_results(results)
    first_row = ['Measurement' , 'Recall']
    myfile = open(excel_name, 'wb')
    wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
    wr.writerow(first_row)

    for i in results_sorted:
        print i
        to_write = [i[0], i[1]]
        wr.writerow(to_write)



def generate_excel_d2v_mln(excel_name, results, parameters_table):
    print 'Generating Excel Limiars and Inter-edges Version'
    print excel_name
    print results
    print parameters_table
    pesos_inter_edge_mln = parameters_table[0]
    limiares = parameters_table[1]

    first_row = ['Inter-edge Weight MLN' , 'Measurement']
    for i in limiares:
        first_row.append(str(i))

    pesos_mln_table = []


    if pesos_inter_edge_mln is not None:
        divisions = len(results) / len(pesos_inter_edge_mln)
        for i in pesos_inter_edge_mln:
            peso = i
            for j in range(divisions):
                pesos_mln_table.append(peso)
    else:
        pesos_mln_table = ['None' for x in results]

    print first_row
    myfile = open(excel_name, 'wb')
    wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
    wr.writerow(first_row)

    for index, actual_result in enumerate(results):
        measure = actual_result[0][0]
        recalls = []
        for j in actual_result:
            recalls.append(j[1])

        write_line = [pesos_mln_table[index], measure]
        write_line.extend(recalls)
        wr.writerow(write_line)
        print write_line


def get_w2v_vector(vocabulary_vectors, sentence):
    w2v_vectors = []
    count = 0
    for word in sentence:
        if word in vocabulary_vectors:
            count+=1
            vector =  vocabulary_vectors[word]
            w2v_vectors.append(vector)

    if count==0:
        final_vector = np.repeat(999999999999999, 300)
    else:
        final_vector = np.mean(w2v_vectors, axis=0)

    return final_vector

def extract_gramas(gramas):
    if len(gramas)==1:
        return gramas[0]
    else:
        value = ''
        for i in gramas:
            value+=i + ' '
        value = value[:-1]
        return value


def save_vector_to_file(ranking):
    file = open(final_results['vectors'], 'a')
    file.write(str(ranking) + '\n')

def join_sentences(sentences):
    joined = ''
    for i in sentences:
        joined  += i + ' '
    joined = joined[:-1]
    return joined

def extract_all_sentences(documents):
    sentence_list = []
    for sentences in documents:
        for sentence in sentences:
            sentence_list.append(sentence)
    return sentence_list


def save_sentences(input_file, documents):
    file = open(input_file, 'w')
    for sentences in documents:
        for sentence in sentences:
            pSentence = special_proccesing_sentence(sentence)
            file.write(pSentence + '\n')

def save_sentences_v2(input_file, sentences):
    pSentences = []
    file = open(input_file,'w')
    for sentence in sentences:
        pSentence = special_proccesing_sentence(sentence)
        file.write(pSentence + '\n')
        pSentences.append(pSentence)
    return pSentences

def save_processed_sentences(input_file, allSentences ,pAllSentences):
    sentences = extract_all_sentences(allSentences)
    pSentences = []
    file = open(input_file, 'w')
    index = 0
    for document in pAllSentences:
        for sentence in document:
            extracted_sentence =  ' '.join(sentence[0])
            extracted_sentence = unicodedata.normalize('NFKD', extracted_sentence).encode('ascii', 'ignore')
            file.write(extracted_sentence + '\n')
            pSentences.append(extracted_sentence)
            index+=1

    dictionary = dict()
    for i , j in zip(sentences, pSentences):
        dictionary[i] = j
    return dictionary

def save_processed_sentences_v2(input_file, allSentences, dictionary_sentence_list):
    pSentences = []
    file = open(input_file, 'w')
    for i in allSentences:
        pSentence = dictionary_sentence_list[i]
        pSentences.append(pSentence)
        file.write(pSentence + '\n')
    return pSentences


'''
def get_fast_test_vector(command, position):
    p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    out, error = p.communicate()
    recovered_data = out.split()
    data = recovered_data[position:]
    return map(float, data)
'''

def get_fast_test_vector(sentences, pSentences, test_file, use_pre_trained=False, language='ptg'):
    #command = './fasttext print-sentence-vectors model.bin < ' + test_file
    if use_pre_trained:
        if language=='ptg':
            command = './fasttext print-sentence-vectors ' + some_parameters['ptg_wiki_ft_vec'] + ' < ' + test_file
        else:
            command = './fasttext print-sentence-vectors ' + some_parameters['eng_wiki_ft_vec'] + ' < ' + test_file
    else:
        command = './fasttext print-sentence-vectors ' + some_parameters['model'] + '.bin < '  + test_file

    p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    output, error = p.communicate()

    lines = output.split('\n')
    lines.pop()

    vector_dictionary = dict()
    for index, line  in enumerate(lines):
        sentence = sentences[index]
        pSentence = pSentences[index]
        position = len(pSentence.split())
        data = line.split()
        vector = map(float, data[position:])
        vector_dictionary[sentence] = vector

    return vector_dictionary

def get_fast_test_vector_s2v(sentences, test_file, use_pre_trained=False, language='ptg'):

    if use_pre_trained:
        if language=='ptg':
            command = './fasttext2 print-sentence-vectors ' + some_parameters['ptg_wiki_ft_vec'] + ' < ' + test_file
        else:
            command = './fasttext2 print-sentence-vectors ' + some_parameters['eng_wiki_ft_vec'] + ' < ' + test_file
    else:
        command = './fasttext2 print-sentence-vectors ' + some_parameters['model_v2'] + '.bin < ' + test_file

    p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    output, error = p.communicate()

    lines = output.split('\n')
    lines.pop()

    vector_dictionary = dict()
    for index, line in enumerate(lines):
        sentence = sentences[index]
        data = line.split()
        vector = map(float, data)
        vector_dictionary[sentence] = vector

    return vector_dictionary


def get_fast_test_vector_v2(model, sentence):
    #words = word_tokenize(sentence) #ideal!!!!!
    words = sentence.split() ## worst
    vectors = []
    for word in words:
        vectors.append(model[word])
    return np.mean(vectors, axis=0)


def get_dictionary_values(dictionary):
    result = dict()

    key = choice(dictionary.keys())
    number_of_vectors = len(dictionary[key])

    for i in range(number_of_vectors):
        result[i] = []

    for measure in dictionary:
        vector = dictionary[measure]
        for index, value in enumerate(vector):
            vector = result[index]
            vector.append(value)
            result[index] = vector

    return result


def get_prediction(probabilities, classes):
    predictions = []
    for i in probabilities:
        if i[0] > i[1]:
            predictions.append((classes[0] , i[0]))
        else:
            predictions.append((classes[1], i[1]))
    return predictions

def get_prediction_svm(distances, classes):
    predictions = []
    for i in distances:
        if i <= 0:
            predictions.append((classes[0], abs(i)))
        else:
            predictions.append((classes[1], i))
    return predictions

'''
features = np.array([[10, 20, 25], [30, 40, 23], [11, 21, 5], [32, 42, 4], [50, 60, 70], [70, 70, 12], [3, 5, 10], [1,1,2], [3,3,5], [10,10,11]])
labels = np.array([True, False, False, False, True, True, False, True, False, True])
'''

def get_labels(document_data):
    labels = []
    #labels = np.empty((0))
    for i in document_data:
        labels.append(i[2])
        #labels = np.append(labels, i[2])
    return labels

def get_rankings(allRankings):
    rankings = []
    for i in allRankings:
        rankings.append(allRankings[i])
    return rankings


def rank_predictions(predictions):
    trues = dict()
    falses = dict()
    ranking = []
    for index, pair in enumerate(predictions):
        if pair[0]:
            trues[index] = pair[1]
        else:
            falses[index] = pair[1]
    sorted_trues = sorted(trues.items(), key=operator.itemgetter(1), reverse=True)
    for i in sorted_trues:
        ranking.append(i[0])
    sorted_falses = sorted(falses.items(), key=operator.itemgetter(1))
    for i in sorted_falses:
        ranking.append(i[0])
    return ranking


def list_split(vector, lengths):
    result = []
    index = 0
    for i in lengths:
        auxiliar = []
        for j in range(i):
            auxiliar.append(vector[index])
            index+=1
        result.append(auxiliar)
    return result


def get_ml_rankings(doc_names, partitions):
    dictionary = dict()
    for name, values in zip(doc_names, partitions):
        # print name, rank_predictions(values)
        actual = dict()
        actual['all_ml'] = rank_predictions(values)
        dictionary[name] = [actual]
    return dictionary


def extract_sentences(document_sentences, p_type):
    sentences = []
    if p_type:
        for i in document_sentences:
            sentences.append(i[0])
    else:
        for i in document_sentences:
            sentences.append(special_proccesing_sentence(i).split())

    return sentences


def get_word_glove_vector(word, dictionary, vectors):
    if  word in  dictionary:
        index = dictionary[word]
        return vectors[index]
    else:
        print "upss!"
        a = input()
        return []


def get_glove_matrix(sentences, dictionary, vectors):
    matrix = []
    for sentence in sentences:
        word_vectors = []
        for word in sentence:
            word_vector = get_word_glove_vector(word, dictionary, vectors)
            word_vectors.append(word_vector)
        final_vector = np.mean(word_vectors, axis=0)
        matrix.append(final_vector)
    return matrix



if __name__ == '__main__':


    sentence1 = 'hola yo me llamo jorge andoni valverde tohalino'
    sentence2 = 'jorge valverde tiene una mac y se va a brasil'
    sentence3 = 'a b c'

    print n_gram_sim(sentence1, sentence3)





    '''
    sentence1 = 'hola yo me llamo jorge andoni valverde tohalino'
    sentence2 = 'jorge valverde tiene una mac y se va a brasil'
    sentence3 = 'hola yo me llamo que se llama jorge andoni valverde tohalino'

    set1 = {'hola' , 'yo' ,  'me' ,  'llamo' ,  'jorge' ,  'andoni' ,  'valverde' , 'tohalino'}

    set2 = {'jorge' , 'valverde' , 'tiene' , 'una' , 'mac' , 'y' , 'se' ,  'va' , 'a' , 'brasil'}

    #print set1 | set2
    #print set1 & set2

    print n_gram_sim(sentence1, sentence3)

    c1 = {1, 2, 3, 4, 5, 6}
    c2 = {2, 4, 6, 8, 10}
    c3 = {1, 2, 3}
    c4 = {4, 5, 6}
    '''



    #print c1 | c2
    #print c1 & c2
    #calculate_similarity_v2([1, 2, 3], [1, 2, 33], '')