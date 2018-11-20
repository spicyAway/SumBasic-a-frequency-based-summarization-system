from __future__ import division
import string
import sys
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from nltk import FreqDist
from nltk import sent_tokenize
import operator

def remove_symbol(filepath):
    with open(filepath, 'r') as file:
        data = file.read().splitlines()
        data = [line for line in data if line is not '']
    all_ascii = []
    for line in data:
        ascii = ''.join(char for char in line if ord(char) < 128)
        all_ascii.append(ascii)
    return all_ascii

def print_dic(dic):
    for key, value in dic.iteritems():
        print "key: " + str(key) + "  value: " + str(value) + "\n"

def split_sentences(data):
    sentences = []
    for line in data:
        sent_text = sent_tokenize(line)
        sentences += sent_text
    return sentences

def preprocess(data):
    lemmatizer = WordNetLemmatizer()
    result = []
    for line in data:
        new_line = []
        line = line.split(" ")
        for word in line:
            if word not in stopwords.words('english'):
                new_line.append(lemmatizer.lemmatize(word.lower()))
        new_line = " ".join(str(item) for item in new_line if item is not "")
        new_line_punc = new_line.translate(None, string.punctuation)
        result.append(new_line_punc)
    return result

def calculate_prob(preprocessed_data):
    passage = " ".join(preprocessed_data)
    passage_without_punc = passage.translate(None, string.punctuation)
    tokens = passage_without_punc.split(" ")
    fdist = FreqDist(tokens)
    total = len(fdist)
    fdist = {k: v / total for k, v in fdist.iteritems()}
    return fdist

def find_max(dic):
    return max(dic, key=dic.get)

def calculate_score(sentences, dic, max_token):
    max_score = 0
    max_index = -1
    for i in range(0, len(sentences)):
        if max_token in sentences[i]:
            score = 0
            tokens = sentences[i].split(" ")
            for word in tokens:
                score += dic[word]
            score = score / len(tokens)
            if score > max_score:
                max_score = score
                max_index = i
    return max_index

def update_prob(selected_sentence, dic):
    tokens = selected_sentence.split()
    uniq = set(tokens)
    for word in uniq:
        dic[word] = dic[word] * dic[word]
    return dic

def check_length(summary):
    tokens = summary.split()
    if len(tokens) >= 100:
        return True
    return False

def original(file_path):
    data = remove_symbol(file_path)
    sentences = split_sentences(data)
    preprocessed_data = preprocess(sentences)
    freq = calculate_prob(preprocessed_data)
    summary = ""
    while not check_length(summary):
        max_index = calculate_score(preprocessed_data, freq, find_max(freq))
        summary += sentences[max_index]
        summary += " "
        freq = update_prob(preprocessed_data[max_index], freq)
    return summary

def main():
  if len(sys.argv) != 4:
	  print "Wrong input: [version eg: simplified] [input_file_path] [output_file_path]"
	  exit()
  version = sys.argv[1]
  file_path = sys.argv[2]
  output_path = sys.argv[3]
  if version == 'orig':
	  result = original(file_path)
	  with open(output_path, "w") as text_file:
    		text_file.write(result)
  else:
	  print("More features coming!")

if __name__== "__main__":
  main()
