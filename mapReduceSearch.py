import multiprocessing
import string
import cPickle
from fuzzywuzzy import fuzz

# This word count application of map reduce is from:
# http://pymotw.com/2/multiprocessing/mapreduce.html
# Modified for the TEXATA 2014 competition to do fuzzy matching of text

from multiprocessing_mapreduce import SimpleMapReduce

def file_to_words(filename):
    """Read a file and return a sequence of (url, match) values.
    """
    searchPhrase = r'How do I upgrade firmware on Cisco router?'

    print multiprocessing.current_process().name + ':'
    print filename + '\n'
    output = []

    with open(filename, 'rt') as f:
        fileDictionary = cPickle.load(f)
        textMatch = fuzz.token_set_ratio(searchPhrase, ' '.join(fileDictionary['text']))
        output.append( (fileDictionary['url'], textMatch) )

    return output

def count_words(item):
    """Convert the partitioned data for a word to a
    tuple containing the url and the match number.
    """
    word, occurrences = item
    return (word, sum(occurrences))


if __name__ == '__main__':
    import operator
    import glob

    input_files = glob.glob('c:\TEXATA\Finals data\RS\content\*.pickle')
##    input_files = glob.glob('c:\TEXATA\Finals data\Security\content\*.pickle')
    
    mapper = SimpleMapReduce(file_to_words, count_words)
    word_counts = mapper(input_files)
    word_counts.sort(key=operator.itemgetter(1))
    word_counts.reverse()
    
    print '\nTop 10 url by fuzzy match\n'
    top10 = word_counts[:10]
    #longest = max(len(word) for word, count in top10)
    for word, count in top10:
        print word + '  :' + str(count)
    print '*** Number of files searched: ' + str(len(input_files)) +' ***'
