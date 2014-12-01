import multiprocessing
import string
import cPickle
from nltk import pos_tag

def fileToTokenDictionary(filename):
##   Read a file and return a tokenized dictionary.
##    Run once on a text file and save as a cPickle file.
    # List of words to remove
    stopWords = set([
            'a', 'an', 'and', 'are', 'as', 'be', 'by', 'for', 'if', 'in', 
            'is', 'it', 'of', 'or', 'py', 'that', 'the', 'to', 'with',
            'quot', 'nbsp', 'http'])
    
    # List of punctuation to remove
    punctuationList = string.maketrans(string.punctuation, ' ' * len(string.punctuation))
    
    # Diagnostic statements
    print multiprocessing.current_process().name + ':'
    print filename + '\n'
    
    # Initialize the output dictionary
    output = dict([('url', ''), ('text', []), ('authors', []), ('statistics', '')])
    
    # Main loop for reading one file and tokenizing the text
    # Creates the output dictionary and then saves it as a cPickle file
    with open(filename, 'rt') as f:
        # Read in the entire text of the file line by line
        dictKey = ''
        for line in f:
            line = line.strip()
            if line == '':
                continue
            elif line.startswith('Title:'):
                dictKey = 'text'
                continue
            elif line.startswith('URL:'):
                dictKey = 'url'
                continue
            elif line.startswith('Statistics:'):
                output['statistics'] = line.split(' ',1)[1]
                continue
            elif line.startswith('Description:') or line.startswith('Reply:'):
                dictKey = 'text'
                line = line.split(r'/')
                output['authors'].append(line[0].split(' ', 1)[1].strip())
                continue
            if not dictKey == '':
                if dictKey == 'url':
                    output[dictKey] = line.strip()
                    dictKey = ''
                elif dictKey == 'text':
                    line = line.translate(punctuationList) # Strip out punctuation
                    textList = []
                    for word in line.split():
                        word = word.lower()
                        if word not in stopWords:
                            textList.append(word)
                    dictKey = ''
                    for word in textList:
                        if word not in output['text']:
                            output['text'].append(word)
        # Tag the word types
        taggedWords = []
        for word in output['text']:
            try:
                taggedWords.append(pos_tag([word])[0])
            except:
                pass
            
        # Filter out the nouns and verbs and cardinal numbers
        nounsVerbs = []
        for tw in taggedWords:
            if tw[1].startswith('CD') or tw[1].startswith('V') or tw[1].startswith('N'):
                nounsVerbs.append(tw[0])
        
        output['text'] = nounsVerbs
                    
# Output files are saved in the same directory as input files with the same filename,
# except .pickle is appended to the filename.
    with open(filename + '.pickle', 'wb') as f:
        cPickle.dump(output, f)
              
# Main program starts the multiple processes

if __name__ == '__main__':
    import operator
    import glob

# Input file location
    input_files = glob.glob('c:\TEXATA\Finals data\RS\content\*.txt')
#    input_files = glob.glob('c:\TEXATA\Finals data\Security\content\*.txt')

# Set up and start the processor pool.
    pool = multiprocessing.Pool()
    for fileName in input_files:
##        p = multiprocessing.Process(target=fileToTokenDictionary, args=(fileName,))
##        p.start()
        pool.apply_async(fileToTokenDictionary, args=(fileName,))
    pool.close()
    pool.join()

    
    

