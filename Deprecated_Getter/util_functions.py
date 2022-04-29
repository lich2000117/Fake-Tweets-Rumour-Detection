## Utility function


import re
import os
import json
import matplotlib.pyplot as plt
from collections import defaultdict as dd
import time

NOW_TIME = time.ctime() # current time



def get_current_time():
    """Get current system Time"""
    current_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
    return current_time

def Write_Doc_Head(doc, QUERY):
    """Write the following Specific Format into the doc file"""
    doc.add_paragraph("\n\n##################Start######################\n\n")
    doc.add_paragraph("\n\n\n\n\n\nTime of this Operation:" + str(NOW_TIME))
    if (QUERY):
        doc.add_paragraph("\nSearch Posts for " + QUERY + "\n\n")
    doc.add_paragraph("\n\n")

def Write_Tail_Save_Doc(OUT_DOC_NAME, doc, QUERY, data_set, data_list_of_dict):
    """Write the following Specific Format into the doc tail"""
    doc.add_paragraph("\n\nTime of this Operation:" + str(NOW_TIME))
    doc.add_paragraph("\nTotal Posts got by this Operation:" + str(len(data_list_of_dict)))
    doc.add_paragraph("\nTotal non_duplicated posts in this Operation: " + str(len(data_set))+ '\n\n')
    doc.add_paragraph("\n\n##################End######################\n\n")
    doc.save(OUT_DOC_NAME)

def Load_Json_Existing_Text(data_set, OUT_JSON_NAME):
    """Save data into existing json file: data_set into existing Json file"""
    try:
        with open(OUT_JSON_NAME, 'r') as fp:
            original = json.load(fp)
            out_data = original + list(data_set)
            out_data = set(out_data)
    except:
        out_data = set(data_set)
    with open(OUT_JSON_NAME, 'w') as fp:
        json.dump(list(out_data), fp,  indent=4)

def Load_Json_Text_and_Set_it(IN_JSON_NAME):
    """Load a json file and return the unique set of it."""
    with open(IN_JSON_NAME) as fp:
        #json.dump(data_list_of_dict, fp,  indent=4)
        text_list = json.load(fp)
        text_list = list(set(text_list))
        return text_list

def Remove_URL(original):
    """Remove url link in the text"""
    result = re.sub(r"http\S+", "", original)
    result = re.sub(r"www.\S+", "", result)
    result = re.sub(r"wasap.my+", "", result)
    return result

def Remove_Emoji(original):
    """Remove Emojis in the text"""
    # To avoid decode problem, use unicode-escapec
    result = re.sub(r"[\\u\\U]\S{5}", "", original)
    return result

def Hash_Freq_Count(text, hash_count_dict, EX_LIST):
    """ # HashTag Count of a space seperated text file.
        EX_LIST: excluded word list
        """
    hashtag_pattern = re.compile(r'#\S{3,15}')
    for word in re.findall(hashtag_pattern, text):
        word = word.strip().lower()
        #remove useless words
        if word[1:] not in EX_LIST:
            hash_count_dict[word]+=1


def Analyse_Frequency(data_set, doc, EX_LIST, TOP_FREQUENCY, sav_dir):
    """# Get frequency of important data, and write into docx, export graphs of frequency
        ## now getting word frequency and hashtag frequency"""
    word_count_dict = dd(int)
    hash_count_dict = dd(int)
    for text in data_set:
        text = text.lower()
        # replace special characters
        for ch in '$&()*+,-./:;<=>?[\\]^_{|}·~‘’':
            text = text.replace(ch," ")
        Word_Freq_Count(text, word_count_dict, EX_LIST)
        Hash_Freq_Count(text, hash_count_dict, EX_LIST)
    WordFrequencyWrite(word_count_dict, doc, TOP_FREQUENCY)
    HashTagFrequencyWrite(hash_count_dict, doc, TOP_FREQUENCY)
    WordCloudGraph(word_count_dict, os.path.join(sav_dir,"Word_Frequency"))
    WordCloudGraph(hash_count_dict, os.path.join(sav_dir,"HashTag_Frequency"))

def Word_Freq_Count(text,word_count_dict, EX_LIST=[]):
    """ #Word Count of a space seperated text file. Bag of words, exclude in the EX_LIST"""
    txt_pattern = re.compile(r'\s([A-Za-z]{3,15})\s')
    for word in re.findall(txt_pattern,text):
        word = word.strip().lower()
        #remove useless words
        if word not in EX_LIST:
            word_count_dict[word]+=1

def WordFrequencyWrite(word_count_dict, doc, TOP_FREQUENCY):
    """ ## Word Frequency Count, Print to docx """
    txt_count_list = list(word_count_dict.items())
    txt_count_list.sort(key=lambda x:x[1],reverse=True)
    doc.add_paragraph("\n\nWord Count List: ")
    for i in range(TOP_FREQUENCY):
        try:
            word,count = txt_count_list[i]
            doc.add_paragraph("{0:<10}{1:>5}".format(word,count))
        except:
            pass

def HashTagFrequencyWrite(hash_count_dict, doc, TOP_FREQUENCY):
    """## Hash TagFrequency Count, Print to docx"""
    hash_count_list = list(hash_count_dict.items())
    hash_count_list.sort(key=lambda x:x[1],reverse=True)
    doc.add_paragraph("\n\nHashTag Count List: ")
    for i in range(TOP_FREQUENCY):
        try:
            word,count = hash_count_list[i]
            doc.add_paragraph("{0:<10}{1:>5}".format(word,count))
        except:
            pass

