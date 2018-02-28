import os
import re
import json

def clean(s):
    reg_clean_0 = re.compile('\t\t\t', flags=re.U | re.DOTALL)
    reg_clean_1 = re.compile('\t\t', flags=re.U | re.DOTALL)
    reg_clean_2 = re.compile('\t', flags=re.U | re.DOTALL)
    
    clean_t = reg_clean_0.sub(" ", s)
    clean_t = reg_clean_1.sub(" ", clean_t)
    clean_t = reg_clean_2.sub(" ", clean_t)
    
    return clean_t

def convert(s):
    num=''
    for i in s:
        if i==' ':
            break
        num += i

    lemma=''
    reg_exp = re.compile('{.*?}', flags=re.U | re.DOTALL)
    tpl = re.findall(reg_exp, s, flags=0)   
    for i in tpl:
         lemma += i[1:len(i)-1] + ' '

    clc=''
    reg_exp = re.compile(' .*?{', flags=re.U | re.DOTALL)
    tpl = re.findall(reg_exp, s, flags=0)   
    for i in tpl:
         clc += i[1:len(i)-1] + ' '
    
    return int(num), lemma[0:len(lemma)-1], clc[0:len(clc)-1]


fin = open('3grams-3.txt', 'r', encoding='utf-8')
fout = open('input.txt', 'w', encoding='utf-8')

for line in fin:
    s = clean(line)
    print(s, end='', file=fout)    
    
fin.close()
fout.close()            
 
os.system(r"C:\Users\User\Desktop\mystem.exe C:\Users\User\Desktop\input.txt C:\Users\User\Desktop\output.txt -cd")

fin = open('output.txt', 'r', encoding='utf-8')

dct={}
for line in fin:
    num, lemma, clc = convert(line)
    dct[clc] = [lemma, num]  
fin.close()

json.dump(dct, open('output_dct.json', 'w', encoding='utf-8'))

dct = json.load(open('output_dct.json', 'r', encoding='utf-8'))

new_dct={}
new_value=''
for key in dct:
    new_value = key + ' ' + str(dct[key][1])
    new_key = dct[key][0]

    if new_dct.get(new_key) != None:
        lst = new_dct[new_key]
        lst.append(new_value)
        new_dct[new_key] = lst
    else:
        new_dct[new_key] = [new_value]

json.dump(new_dct, open('output_verse_dct.json', 'w', encoding='utf-8'))
