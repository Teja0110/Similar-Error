from difflib import SequenceMatcher 
  
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