import re
import json
import os

def convert(s):
    reg_exp = re.compile('[а-яА-Я,:;-]+', flags=re.U | re.DOTALL)
    lst = re.findall(reg_exp, s, flags=0)
    lst_final=[]
    for i in lst:
        if i[len(i)-1] in [',',':',';','-']:
            ss=''
            for j in range(0, len(i)-1):
                ss += i[j]
                if i[j+1] in [',',':',';','-']:
                    ss += ' '
            ss += i[len(i)-1]
            lst_final.append(ss)
        else:
            lst_final.append(i)            
    return lst_final

def make_trigram(lst):
    lst_final=[]
    for i in range(1, len(lst)-1):
        trigram = lst[i-1] + ' ' + lst[i] + ' ' + lst[i+1]
        lst_final.append(trigram)       
    return lst_final

def make_lemma(s):
    fout = open('line_in.txt', 'w', encoding='utf-8')
    print(s, file=fout)
    fout.close()

    os.system(r"C:\Users\User\Desktop\mystem.exe C:\Users\User\Desktop\line_in.txt C:\Users\User\Desktop\line_out.txt -cd")

    fin = open('line_out.txt', 'r', encoding='utf-8')
    ss=''
    for line in fin:
        ss = line
        break
    fin.close()

    reg_exp = re.compile('{.*?}', flags=re.U | re.DOTALL)
    lst = re.findall(reg_exp, ss, flags=0)
    
    st=''
    for i in lst:
        st += i[1: len(i)-1] + ' '
    return st[0:len(st)-1]


def correction(tri, lemmas):
    final_tri=''
    common_num = 0

    for s in lemmas:
        reg_exp = re.compile('[0-9]+', flags=re.U | re.DOTALL)
        num = re.findall(reg_exp, s, flags=0)
        st = s[0:len(s)-len(num[0])-1]
        if tri == st:
            return tri
    
    for s in lemmas:
        reg_exp = re.compile('[а-яА-Я]+', flags=re.U | re.DOTALL)
        lst_ans = re.findall(reg_exp, s, flags=0)
        lst_tri = re.findall(reg_exp, tri, flags=0)
        num = 0
        for j in range(3):
            if lst_ans[j] == lst_tri[j]:
                num += 1
        if num > common_num:
            common_num, final_tri = num, s

    reg_exp = re.compile('[0-9]+', flags=re.U | re.DOTALL)
    lst = re.findall(reg_exp, final_tri, flags=0)
    
    final_tri = final_tri[0:len(final_tri)-len(lst[0])-1]
    return final_tri

def new_trigram(trigram, answer, l, r):
    reg_exp = re.compile('[а-яА-Я,:;-]+', flags=re.U | re.DOTALL)
    lst_1 = re.findall(reg_exp, trigram, flags=0)
    lst = re.findall(reg_exp, answer, flags=0)

    new_tri=''
    if l == 0 and r == 2:
        w = 0
        for i in lst:
            if 'а' <= i[0] <= 'я' or 'А' <= i[0] <= 'Я':
                w += 1
            if w > 1:
                new_tri += i + ' '
        w = 0
        for i in lst_1:
            if w == 2:
                new_tri += i + ' '
            if 'а' <= i[0] <= 'я' or 'А' <= i[0] <= 'Я':
                w += 1

    if l == 1 and r  == 3:
        w = 0
        for i in lst_1:
            if 'а' <= i[0] <= 'я' or 'А' <= i[0] <= 'Я':
                w += 1
            if w < 2:
                new_tri += i + ' '

        w = 0
        for i in lst:
            if 'а' <= i[0] <= 'я' or 'А' <= i[0] <= 'Я':
                w += 1
            if w < 3:
                new_tri += i + ' '

    if l == 2 and r == 3:
        w = 0
        for i in lst_1:
            if 'а' <= i[0] <= 'я' or 'А' <= i[0] <= 'Я':
                w += 1
            if w < 3:
                new_tri += i + ' '
        new_tri += lst[0] + ' '


    if l == 0 and r == 1:
        new_tri += lst[len(lst)-1] + ' '

        w = 0
        for i in lst_1:
            if w >= 1:
                new_tri += i + ' '
            if 'а' <= i[0] <= 'я' or 'А' <= i[0] <= 'Я':
                w += 1
                
    return new_tri[0:len(new_tri)-1]

def make_sentence(trigrams):
    sentence=''
    i = 0
    for i in range (0, len(trigrams), 3):
        if i >= len(trigrams):
            break
        sentence += trigrams[i] + ' '

    print(len(trigrams))
    reg_exp = re.compile('[а-яА-Я,:;-]+', flags=re.U | re.DOTALL)
    lst = re.findall(reg_exp, trigrams[len(trigrams) - 1], flags=0)
    if i + 3 == len(trigrams):
        w = 0
        for j in lst:
            if w >= 1:
                sentence += j + ' '
            if 'а' <= j[0] <= 'я' or 'А' <= j[0] <= 'Я':
                w += 1
            
    if i + 2 == len(trigrams):
        w = 0
        for j in lst:
            if w >= 2:
                sentence += j + ' '
            if 'а' <= j[0] <= 'я' or 'А' <= j[0] <= 'Я':
                w += 1     
    
    return sentence[0:len(sentence)-1]

def find_commas(s):
    commas=''
    for i in range(len(s)-1, 0, -1):
        if 'а' <= s[i] <= 'я' or 'А' <= s[i] <= 'Я':
            break
        commas += s[i]
    return commas[::-1]
    

dct = json.load(open('output_verse_dct.json', 'r', encoding='utf-8'))

fin = open('input_text.txt', 'r', encoding='utf-8')
fout = open('output_text.txt', 'w', encoding='utf-8')
for line in fin:
    lst = convert(line)
    trigrams = make_trigram(lst)
    commas = find_commas(line)
    #print(trigrams)
    
    answer = ''
    for i in range(len(trigrams)):
        lemma = make_lemma(trigrams[i])
        #print(lemma)
        lemmas = dct.get(lemma)
        if lemmas != None:
            answer = correction(trigrams[i], lemmas)
            #print('yes', answer)
            #print(lemmas)
        else:
            answer = trigrams[i]
            #print('none')

        if answer != trigrams[i]:
            if i - 1 >= 0:
                new = new_trigram(trigrams[i-1], answer, 1, 3)
                trigrams[i-1] = new
            if i + 1 < len(trigrams):
                new = new_trigram(trigrams[i+1], answer, 0, 2)
                trigrams[i+1] = new
            if i - 2 >= 0:
                new = new_trigram(trigrams[i-2], answer, 2, 3)
                trigrams[i-2] = new
            if i + 2 < len(trigrams):
                new = new_trigram(trigrams[i+2], answer, 0, 1)
                trigrams[i+2] = new
            trigrams[i] = answer

    sentence = make_sentence(trigrams)
    sentence += find_commas(line)
    print(sentence, file = fout)
 
fin.close()
fout.close()
