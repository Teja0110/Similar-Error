# Import nescessary Library
import string
import math
from collections import Counter # To find different characters between two sentences
from difflib import SequenceMatcher 

# input: and essay with plain_text and markup
# output: return a list of similar errors of word_choice with number of error for each
# The related words for that error and the indices (on markup) of that error
def word_choice(input):
    output = []
    check = False
    for i in range(len(input['markup'])):
        error = input['markup'][i]
        check = False
        if error['type'] == 'word choice':
            # Check if we see this error before, update the error_count
            for item in output:
                if ((error['old_text'] in item['words']) or
                    (error['new_text'] in item['words'])):
                    check = True # Set this error already marked
                    item['index'].append(i)
                    item['words'].add(error['old_text'])
                    if error['new_text'] != None and error['new_text'] != '':
                        item['words'].add(error['new_text'])
                    item['error_count'] = item['error_count'] + 1
        
            # The error haven't been seen before
            if check == False:
                if error['new_text'] != None:
                    output.append({'words' : {error['old_text'], error['new_text']},
                                  'index' : [i], 'error_count' : 1})
                else:
                    output.append({'words' : {error['old_text']},
                                  'index' : [i], 'error_count' : 1})


    # Return output
    return output



# Define a set of rules for similar punctuation errors
# The rules we set bases on the markup punctuation error from essay input above
# return a dictionary of all similar errors and numbers of their appearance
def punctuation_error(input):
    output = {}
    # Loop through all errors in an essay then process only punctuation error
    for i in range(len(input['markup'])):
        error = input['markup'][i]
        if (error['type'] == 'punctuation'):
            old_text = error['old_text']
            new_text = error['new_text']
            if new_text != None:
                new_text_trim = new_text.replace(' ', '')
            old_text_trim = old_text.replace(' ', '')
            
            #if old_text == new_text:
            #raise ValueError("Markup error new and old text are the same")
            # Capitalization error: text on old and new word are the same except capilize a character
            if(new_text != None and old_text.lower() == new_text.lower()):
                # check if we already had capitalization error on output
                # Add new if there is not
                if('capitalization_error' not in output):
                    output['capitalization_error'] = {'definition' : 'Errors on capitalization',
                        'index' : [i], 'error_count' : 1}
                else:
                    output['capitalization_error']['index'].append(i)
                    error_cnt = output['capitalization_error']['error_count']
                    output['capitalization_error']['error_count'] = error_cnt + 1
    
            # Error of misleading between 2 punctuations
            elif( new_text != None and  old_text != None and len(old_text) == 1 and  len(new_text) == 1 and old_text in string.punctuation  and new_text in string.punctuation):
                error_name = ''
                if((('misleading ' + old_text + new_text) in output)):
                     error_name = 'misleading ' + old_text + new_text
                elif ((('misleading ' + new_text + old_text) in output)):
                    error_name = 'misleading ' + new_text + old_text
        
                # check if output has this type of error - add new if not
                if(error_name == ''):
                    error_name = 'misleading ' + old_text + new_text
                    error_def = 'Errors of misleading between ' + old_text + ' and ' + new_text
                    output[error_name] = {'definition' : error_def, 'index' : [i], 'error_count' : 1}
                else:
                    output[error_name]['index'].append(i)
                    output[error_name]['error_count'] = output[error_name]['error_count'] + 1
         
            # Error of using wrong a punctuation or missing using an punctuation
            # First case: new_word/old_word contain empty string and/or a punctuation
            elif(new_text !=  None and ((old_text_trim == '' and len(new_text_trim) == 1 and new_text_trim in string.punctuation) or ((new_text_trim == '') and len(old_text_trim) == 1 and old_text_trim in string.punctuation))):
                error_name = 'error_use ' + old_text_trim + new_text_trim
                 # check if output has this type of error - add new if not
                if(error_name not in output):
                    error_def = 'Wrong used or missing using of ' + old_text_trim + new_text_trim
                    output[error_name] = {'definition' : error_def, 'index' : [i], 'error_count' : 1}
                else:
                    output[error_name]['index'].append(i)
                    output[error_name]['error_count'] = output[error_name]['error_count'] + 1
                    # Second case: new_word/old_word contains a sentence with a punctuation
                    # and the other contain the same sentence without that punctuation
            elif(new_text !=  None and abs(len(old_text_trim) - len(new_text_trim)) == 1):
                # Get the different character between old_word and new_word
                # Then check if the different character between them is punctuation or not
                if(len(old_text_trim) > len(new_text_trim)):
                    dif_char = list(Counter(old_text_trim.lower()) - Counter(new_text_trim.lower()))[0]
                else:
                    dif_char = list(Counter(new_text_trim.lower()) - Counter(old_text_trim.lower()))[0]
                                                         
                if(dif_char in string.punctuation):
                    error_name = 'error_use ' + dif_char
                    if(error_name not in output):
                        error_def = 'Wrong used or missing using of ' + dif_char
                        output[error_name] = {'definition' : error_def, 'index' : [i], 'error_count' : 1}
                    else:
                        output[error_name]['index'].append(i)
                        output[error_name]['error_count'] = output[error_name]['error_count'] + 1
                # Otherwise add to other error
                else:
                    error_name = 'other_error'
                    if(error_name not in output):
                        output[error_name] = {'definition' : 'other errors', 'index' : [i], 'error_count' : 1}
                    else:
                        output[error_name]['index'].append(i)
                        output[error_name]['error_count'] = output[error_name]['error_count'] + 1
                                                                                                             
            # The rest add to other error
            else:
                error_name = 'other_error'
                if(error_name not in output):
                    output[error_name] = {'definition' : 'other errors', 'index' : [i], 'error_count' : 1}
                else:
                    output[error_name]['index'].append(i)
                    output[error_name]['error_count'] = output[error_name]['error_count'] + 1
    return output

def sub(str1,str2):
    # initialize SequenceMatcher object with
    # input string
    seqMatch = SequenceMatcher(None,str1,str2)
    
    # find match of longest sub-string
    # output will be like Match(a=0, b=0, size=5)
    match = seqMatch.find_longest_match(0, len(str1), 0, len(str2))
        
        # print longest substring
        if (match.size!=0):
            z=str1[match.a: match.a + match.size]
            return z

def de(str1,str2):
    a=dict()
    for i in str1:
        for j in str2:
            if(i==j and str1.index(i)==str2.index(j)):
                c=str1.replace(i,'')
    a[c]=str1
    return a

a=[error['old_text'] for error in data[0]['markup'] if error['type'] == 'grammar']
b=[error['new_text'] for error in data[0]['markup'] if error['type'] == 'grammar']
print(a)
for i in range(1,len(a)):
    c=sub(a[i-1],a[i])
    if(c!=None):
        print(de(c,a[i-1]))
