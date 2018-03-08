#!/usr/bin/python
import re
import sys
def eng_tokenizer(abbrev):
    abbrevList = [] # initialize a list to contain abbreviation words provided by abbrev
    """
    read and clean input abbreviation file
    """
    abbrevList = [line.rstrip('\r\n') for line in open(abbrev)]
    abbrevList = list(filter(None, abbrevList))
    
    for line in sys.stdin.readlines():
        wordlist = [] # initialize a list to contain tokens splitted by whitespace only
        wordlist = line.split() # split each line into tokens by whitespace
        wordlist_modified = [[' ']]*len(wordlist) # initialize a list to contain tokenized tokens
        word_comma = ''
        for i in range(len(wordlist)):
            """
            First case: consider is if the token is followed by only one punctuation. If it is, then separate them.
            Special consideration is given to the case where the token is from the abbreviation list. If so, do nothing
            """
            if len(re.findall('^.+\.?[,\.\?\!]$',wordlist[i])) != 0: #check if re can find in current element
                word_comma = wordlist[i]
    
                if wordlist[i] not in abbrevList:
                    word_comma = ''.join(word_comma)
                    word_comma = [word_comma[:-1]+' '+word_comma[-1:]]
                    wordlist_modified[i] = word_comma
                else:
                    wordlist_modified[i] = [word_comma]
            """
            Second case: consider if the token is preceded by only one punctuation. If so, separate them.
            Special consideration
            """
            if len(re.findall('^[\"\'\`]\w+$',wordlist[i])) != 0:
                word_comma = wordlist[i]
                word_comma = ''.join(word_comma)
                wordlist_modified[i] = [word_comma[0]+' '+word_comma[1:]]
        
            """
            Third case: consider if the token is preceded and succeded by only one punctuation. If so, separate them.
            """
            if len(re.findall('^[\"\'\`].+[\"\'\`]$',wordlist[i])):
                word_comma = wordlist[i]
                word_comma = ''.join(word_comma)
                if word_comma[1] == '$':
                    wordlist_modified[i] = [word_comma[0] + ' ' + word_comma[1] + ' ' + word_comma[2:-1] + ' '+ word_comma[-1:]]
                else:
                    wordlist_modified[i] = [word_comma[0] + ' ' + word_comma[1:-1] + ' ' +word_comma[-1:]]
            
            """
            Fourth case: consider "Ph.D.\"", where an abbreviation is followed by a quotation. Or, the last token is a
            quoted sentence. This also handles numbers and other things ending in 
            """
            if len(re.findall('^.+[,\.\?!][\"\'\`]$',wordlist[i])):
                word_comma = wordlist[i]
                word_comma = ''.join(word_comma)
                if word_comma[:-1] not in abbrevList:
                    wordlist_modified[i] = [word_comma[:-2] + ' ' + word_comma[-2:-1] + ' ' + word_comma[-1:]]
                else:
                    word_comma = [word_comma[:-1]+' '+word_comma[-1:]]
                    wordlist_modified[i] = word_comma
                
            """
            Fifth case: numbers and special numbers such as -4, 1.23, 3/4 etc. without any punctuations 
            around them (in 1st case, it does) are handled in previous cases. In this case, we consider numbers that 
            are preceded by $. 
            """
            if len(re.findall('^\$.+$',wordlist[i])) != 0:
                word_comma = wordlist[i]
                word_comma = ''.join(word_comma)
                wordlist_modified[i] = [word_comma[0] + ' ' + word_comma[1:]]
            
            """
            Sixth case: in this case, we look for dashes.
            """
            if len(re.findall('^.+\-\-.+$',wordlist[i])) != 0:
                word_comma = wordlist[i]
                word_comma = ''.join(word_comma)
                j = 0
                while word_comma[j] != '-':
                    j = j+1
                wordlist_modified[i] = [word_comma[:j] + ' ' + word_comma[j:j+2] + ' ' + word_comma[j+2:]]
                
            """
            Seventh case: handle clitization such as father's, should've
            """
            if len(re.findall('^\w+\'[(ll)(ve)(re)(s)(d)]$',wordlist[i])) != 0:
                word_comma = wordlist[i]
                word_comma = ''.join(word_comma)
                j = 0
                while word_comma[j] != '\'':
                    j = j+1
                wordlist_modified[i] = [word_comma[:j] + ' ' + word_comma[j:]]
            """
            Eighth case: this case handles clitized words preceded by a quotation
            """    
            if len(re.findall('^[\"\'\`]\w+\'\w+$',wordlist[i])) != 0:
                word_comma = wordlist[i]
                word_comma = ''.join(word_comma)
                j = 0
                while word_comma[j] != '\'':
                    j = j+1
                wordlist_modified[i] = [word_comma[0] + ' ' + word_comma[1:j] + ' ' + word_comma[j:]]
                
            """
            Ninth case: this case handles clitized words followed by a quotation
            """    
            if len(re.findall('^\w+\'\w+[\"\'\`]$',wordlist[i])) != 0:
                word_comma = wordlist[i]
                word_comma = ''.join(word_comma)
                j = 0
                while word_comma[j] != '\'':
                    j = j+1
                wordlist_modified[i] = [word_comma[:j] + ' ' + word_comma[j:-1] + ' ' + word_comma[-1:]]

            """
            Tenth case: consider words followed by a single quotation mark
            """
            if len(re.findall('^.+[\"\'\`]$',wordlist[i])) != 0:
                word_comma = wordlist[i]
                word_comma = ''.join(word_comma)
                wordlist_modified[i] = [word_comma[:-1]+' '+word_comma[-1:]]

            """
            Eleventh case: handle clitization such as hasn't
            """
            if len(re.findall('^\w+n\'t$',wordlist[i])) != 0:
                word_comma = wordlist[i]
                word_comma = ''.join(word_comma)
                j = 0
                while word_comma[j] != 'n':
                    j = j+1
                wordlist_modified[i] = [word_comma[:j] + ' ' + word_comma[j:]]
    
        for i in range(len(wordlist)):
            if wordlist_modified[i] == [' ']:
                wordlist_modified[i] = [wordlist[i]]
        
        wordlist_tokenized = [None]*len(wordlist_modified)
        for i in range(len(wordlist_modified)):
            a = wordlist_modified[i]
            a = ''.join(a)
            wordlist_tokenized[i] = a

        print(' '.join(wordlist_tokenized))
     

if __name__ == "__main__":
    eng_tokenizer(sys.argv[1])
