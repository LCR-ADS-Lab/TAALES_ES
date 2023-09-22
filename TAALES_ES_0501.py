#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb  3 12:35:38 2020

@author: kkyle2
"""

#TAALES_ES
import glob
import math
import pickle
from lexical_diversity import lex_div as ld #see https://github.com/kristopherkyle/lexical_diversity
import spacy
nlp = spacy.load("es_core_news_sm")


def spacy_morph(tag_string):
	morph_list = []
	morphs = tag_string.split("|") #slit the morphology output into a list
	for x in morphs: #iterate through the morpheme information
		#print(x)
		if "Mood" in x: #This will be Indicative or Subjunctive (I think), 
			#print(x)
			morph_list.append(x.split("=")[-1])
		if "Tense" in x: #this includes aspect - present, past, perfect, etc.
			morph_list.append(x.split("=")[-1])
		
		if len(morph_list) == 0 and "VerbForm" in x: #this is to mark infinitives
			morph_list.append(x.split("=")[-1])
	
	if len(morph_list) > 0: 
		return("_" + "_".join(morph_list))
	else:
		return("")
		

def spcy_process(flnm): #other options are "raw","lemma"
	out_dict = {"lemma_pos":[],"content_lemma_pos":[],"verb_lemma_pos":[],"noun_lemma_pos":[],"raw":[],"raw_content":[],"combined":[],"raw_bigram":[],"bigram":[],"dep_bigram":[]}
	doc = nlp(open(flnm,errors = "ignore").read(), disable = ["ner"])
	for sent in doc.sents:
		prev_lemm = None #for bigram calculation later
		prev_raw = None
		
		for token in sent:
			if token.pos_ in ["PUNCT","SYM", "NUM", "PROPN","X", "SPACE" ]:
				continue
			if token.text in ["[","]","(",")"]:
				continue
			
			#raw words
			raw_form = token.text.lower()
			out_dict["raw"].append(token.text.lower()) #add raw word to list in dictionary
			
			#raw_bigrams
			if prev_raw == None:
				prev_raw = raw_form
			else:
				out_dict["raw_bigram"].append(prev_raw + "-" + raw_form)
				prev_raw = raw_form
			
			#lemmas
			if token.pos_ == "VERB":
				tags = "_VERB" + spacy_morph(token.tag_)
			elif token.pos_ == "AUX":
				tags = "_AUX" + spacy_morph(token.tag_)
			else:
				tags = "_" + token.pos_
			
			if token.pos_ == "PRON":
				lemma_form = token.text.lower()+tags
			else:
				lemma_form = token.lemma_.lower()+tags
			out_dict["lemma_pos"].append(lemma_form)
			out_dict["combined"].append([lemma_form,raw_form])
			
			if prev_lemm == None:
					prev_lemm = lemma_form

			else:
				out_dict["bigram"].append(prev_lemm + "-" + lemma_form)
				prev_lemm = lemma_form

			#content words:
			if "ADJ" in lemma_form:
				out_dict["content_lemma_pos"].append(lemma_form)
				out_dict["raw_content"].append(raw_form)
			elif "NOUN" in lemma_form:
				out_dict["content_lemma_pos"].append(lemma_form)
				out_dict["noun_lemma_pos"].append(lemma_form)
				out_dict["raw_content"].append(raw_form)

			elif "VERB" in lemma_form:
				out_dict["content_lemma_pos"].append(lemma_form)
				out_dict["verb_lemma_pos"].append(lemma_form)
				out_dict["raw_content"].append(raw_form)

			elif "ADV" in lemma_form:
				out_dict["content_lemma_pos"].append(lemma_form)
				out_dict["raw_content"].append(raw_form)

				
	return(out_dict)


def index_calc_spl(item_l,item_d,index_name,fg_dict,lgrm = False):
	fg_dict[index_name] = [] #create list for items
	
	denom = 0
	numerator = 0
	for item in item_l:
		if item in item_d:
			denom += 1
			if lgrm == True:
				numerator += math.log(item_d[item])
				fg_dict[index_name].append(str(math.log(item_d[item])))
			else:	
				numerator += item_d[item]
				fg_dict[index_name].append(str(item_d[item]))
		else:
			fg_dict[index_name].append("n/a")
	
	if denom == 0:
		outvar = 0
	else:
		outvar = numerator/denom
	
	return(str(outvar))

#kris start here!!!
def index_calc_psychol(item_l,item_d,index_name,fg_dict,lgrm = False):
	fg_dict[index_name] = [] #create list for items

	denom = 0
	numerator = 0
	for item in item_l:
		lemma = item[0].split("_")[0]
		raw = item[1]
		#need to add raw with plural removed
		
		#lemmas
		if lemma in item_d:
			denom += 1
			numerator += item_d[lemma]
			fg_dict[index_name].append(str(item_d[lemma]))
			#print(raw, item_d[lemma])
		#simple raw
		elif raw in item_d:
			denom += 1
			numerator += item_d[raw]
			fg_dict[index_name].append(str(item_d[raw]))
			#print(raw, item_d[raw])
		elif raw[-1] == "s" and raw[:-1] in item_d:
			denom += 1
			numerator += item_d[raw[:-1]]
			fg_dict[index_name].append(str(item_d[raw[:-1]]))
			#print(raw, item_d[raw[:-1]])
		elif raw[-2:] == "es" and raw[:-2] in item_d:
			denom += 1
			numerator += item_d[raw[:-2]]
			fg_dict[index_name].append(str(item_d[raw[:-2]]))
			#print(raw, item_d[raw[:-2]])
		else:
			fg_dict[index_name].append("n/a")
			continue
		# add elif without plural s

	if denom == 0:
		outvar = 0
	else:
		outvar = numerator/denom
	
	return(str(outvar))

#double check this!
def index_calc_max(item_l,item_d,item_d2,index_name,fg_dict,lgrm = False):
	fg_dict[index_name] = [] #create list for items

	denom = 0
	numerator = 0
	for item in item_l:
		if item in item_d:
			denom += 1
			if lgrm == True:
				numerator += math.log(max(item_d[item],item_d2[item]))
				fg_dict[index_name].append(str(math.log(max(item_d[item],item_d2[item]))))

			else:	
				numerator += max(item_d[item],item_d2[item])
				fg_dict[index_name].append(str(max(item_d[item],item_d2[item])))
		else:
			fg_dict[index_name].append("n/a")

	
	if denom == 0:
		outvar = 0
	else:
		outvar = numerator/denom
	
	return(str(outvar))


def indexer(index_value, index_name, index_list, name_list):
	index_list.append(index_value)
	name_list.append(index_name)
	
def dict_maker(spreadsheet, key_id, value_id,sep):
	outd = {}
	for x in spreadsheet:
		if x[0] == "#":
			continue
		else:
			row = x.split(sep)
			outd[row[key_id]] = float(row[value_id])
	return(outd)

def attested_words(attested_dict, text_list): #this is for the calculation of lexical diversity. It ensures that misspellings and other mistakes don't count towards diversity
	clean_list = []
	
	for x in text_list:
		if x in attested_dict:
			clean_list.append(x)
	
	return(clean_list)
	
#####################################################
### This is where the program calculation starts! ###
#####################################################	

freq_list = open("escowax01_pos_freq.txt").read().split("\n") #open the frequency list
freq_dict = dict_maker(freq_list,0,1,"\t")

psycho_list = open("ESM_database.txt").read().split("\n") #open the pscyholinguistic database
val_dict = dict_maker(psycho_list,0,1,"\t")
aro_dict = dict_maker(psycho_list,0,2,"\t")
conc_dict = dict_maker(psycho_list,0,3,"\t")
imag_dict = dict_maker(psycho_list,0,4,"\t")
avail_dict = dict_maker(psycho_list,0,5,"\t")
fam_dict = dict_maker(psycho_list,0,6,"\t")

bi_list = open("escowax01_bi_soa.txt").read().split("\n") #open the frequency list
bi_dp_LR = dict_maker(bi_list,0,1,"\t")
bi_dp_RL = dict_maker(bi_list,0,2,"\t")
bi_MI = dict_maker(bi_list,0,3,"\t")
bi_T = dict_maker(bi_list,0,4,"\t")
bi_freq = dict_maker(bi_list,0,5,"\t")

def output_writer(fname,raw_l,lem_l,out_d,index_list, writefile):	
	
	for index, value in enumerate(raw_l):
		row = [fname,value,lem_l[index]]
		for x in index_list:
			row.append(out_d[x][index])
		writefile.write("\n" + "\t".join(row))
		
	
def TAALES_ES(in_folder, outname):
	filenames = glob.glob(in_folder + "*.txt") #filename goes here
	outf = open(outname, "w")
	
	word_output_dict = {} #for fine-grained output
	bigram_output_dict = {} #for fine-grained output
	null_output_dict = {}
	
	#for fine-grained results
	outf2 = open(outname[:-4] + "_" + "word_level_results.txt","w")
	wrd_index_list = "filename raw_word lemma lemma_frequency_log_AW".split(" ")
	outf2.write("\t".join(wrd_index_list))
	
	outf3 = open(outname[:-4] + "_" + "content_word_level_results.txt","w")
	content_index_list = "filename raw_word lemma lemma_frequency_log_CW valency_CW arousal_CW concreteness_CW imageability_CW availability_CW familiarity_CW".split(" ")
	outf3.write("\t".join(content_index_list))

	outf4 = open(outname[:-4] + "_" + "bg_level_results.txt","w")
	bg_index_list = "filename raw_bg lemma_bg bigram_freq_log bigram_soa_dp_LR bigram_soa_dp_RL bigram_soa_dp_max bigram_soa_MI bigram_soa_T".split(" ")
	outf4.write("\t".join(bg_index_list))

	for idx,filename in enumerate(filenames):
		#print("Processing " + str(idx+1) + " of " + str(len(filenames)) + " files")
		outname = filename.split("/")[-1]
		print(outname)
		values = [outname]
		headers = ["filename"]
		token_dict = spcy_process(filename)
		#print(ld)
		
		word_output_dict = {} #for fine-grained output
		bigram_output_dict = {} #for fine-grained output
		content_output_dict = {}
		null_output_dict = {}

		
		indexer(str(len(token_dict["lemma_pos"])),"nwords",values,headers)
		indexer(str(len(token_dict["content_lemma_pos"])),"ncontentwords",values,headers)
		indexer(str(ld.mattr(attested_words(freq_dict,token_dict["lemma_pos"]))),"MATTR_lemmas",values,headers)
		indexer(index_calc_spl(token_dict["lemma_pos"],freq_dict,"lemma_frequency_log_AW",word_output_dict,True),"lemma_frequency_log_AW",values,headers)
		indexer(index_calc_spl(token_dict["content_lemma_pos"],freq_dict,"lemma_frequency_log_CW",content_output_dict,True),"lemma_frequency_log_CW",values,headers)
		indexer(index_calc_spl(token_dict["verb_lemma_pos"],freq_dict,"lemma_frequency_log_verbs",null_output_dict,True),"lemma_frequency_log_verbs",values,headers)
		indexer(index_calc_spl(token_dict["noun_lemma_pos"],freq_dict,"lemma_frequency_log_nouns",null_output_dict,True),"lemma_frequency_log_nouns",values,headers)

		indexer(index_calc_spl(token_dict["bigram"],bi_freq,"bigram_freq_log",bigram_output_dict,True),"bigram_freq_log",values,headers)
		indexer(index_calc_spl(token_dict["bigram"],bi_dp_LR,"bigram_soa_dp_LR",bigram_output_dict,False),"bigram_soa_dp_LR",values,headers)
		indexer(index_calc_spl(token_dict["bigram"],bi_dp_RL,"bigram_soa_dp_RL",bigram_output_dict,False),"bigram_soa_dp_RL",values,headers)
		indexer(index_calc_max(token_dict["bigram"],bi_dp_LR,bi_dp_RL,"bigram_soa_dp_max",bigram_output_dict,False),"bigram_soa_dp_max",values,headers)
		indexer(index_calc_spl(token_dict["bigram"],bi_MI,"bigram_soa_MI",bigram_output_dict,False),"bigram_soa_MI",values,headers)
		indexer(index_calc_spl(token_dict["bigram"],bi_T,"bigram_soa_T",bigram_output_dict,False),"bigram_soa_T",values,headers)
		
		indexer(index_calc_psychol(token_dict["combined"],val_dict,"valency_CW",content_output_dict),"valency_CW",values,headers)
		indexer(index_calc_psychol(token_dict["combined"],aro_dict,"arousal_CW",content_output_dict),"arousal_CW",values,headers)
		indexer(index_calc_psychol(token_dict["combined"],conc_dict,"concreteness_CW",content_output_dict),"concreteness_CW",values,headers)
		indexer(index_calc_psychol(token_dict["combined"],imag_dict,"imageability_CW",content_output_dict),"imageability_CW",values,headers)
		indexer(index_calc_psychol(token_dict["combined"],avail_dict,"availability_CW",content_output_dict),"availability_CW",values,headers)
		indexer(index_calc_psychol(token_dict["combined"],fam_dict,"familiarity_CW",content_output_dict),"familiarity_CW",values,headers)
		
		output_writer(outname,token_dict["raw"],token_dict["lemma_pos"],word_output_dict,wrd_index_list[3:], outf2)
		output_writer(outname,token_dict["raw_content"],token_dict["content_lemma_pos"],content_output_dict,content_index_list[3:], outf3)
		output_writer(outname,token_dict["raw_bigram"],token_dict["bigram"],bigram_output_dict,bg_index_list[3:], outf4) #need to fix this piece!
		
		if idx == 0:
			outf.write(",".join(headers))
		outf.write("\n" + ",".join(values))
	
	outf.flush()
	outf.close()
	
	outf2.flush()
	outf2.close()

	outf3.flush()
	outf3.close()

	outf4.flush()
	outf4.close()

	
	print("Finished!")	 

#iterate through all folders, provide output
# big_fnames = glob.glob("Langsnap Text/*_clean")
# for x in glob.glob("Langsnap Text/*_clean"):
# 	simple = x.split("/")[-1] + "_TAALES_ES_05.csv" #create filename
# 	TAALES_ES(x+"/",simple)
#TAALES_ES("Langsnap Text/post_1_clean/","TAALES_ES_05_test.csv")
