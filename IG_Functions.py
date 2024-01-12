import math
import sys
import operator
#entropia
def H(pc0,pc1): 
    if (pc0>0 and pc1>0):
        return (-1)*(pc0*math.log2(pc0)+pc1*math.log2(pc1))
    elif(pc0>0):
        return (-1)*(pc0*math.log2(pc0))
    elif(pc1>0):
        return (-1)*(pc1*math.log2(pc1))
    else:
        return 0 #mhdenikh entropia,ara full vevaiothta
#kerdos pliroforias
def IG(key,word,sum_mes,sum_pos_mes): 
    pexists = word[0]/sum_mes #sunolo twn mhnumatwn pou uparxei h leksi/sunono twn mhnumatwn
    try:
        ppos_exists = word[1]/word[0] #sunolo twn pos emfanisewn ths leksis/sunolo twn emfanisewn ths leksis
    except:
        ppos_exists = 0
    try:
        ppos_notexists = (sum_pos_mes-word[1])/(sum_mes-word[0])#sunolo twn pos mhnumatwn pou uparxei den leksi/sunolo mhnumatwn p den emfanizetai h leksi
    except:
        ppos_notexists = 0
    pc0 = H(ppos_exists, 1-ppos_exists) #pithanothta na exw pos | uparxei h leksi, pithtanothta na exw neg | uparxei h leksi
    pc1 = H(ppos_notexists,1-ppos_notexists)#pithanothta na exw pos | den uparxei h leksi, pithtanothta na exw  | den uparxei h leksi
    
    return pexists*pc0 + (1-pexists)*pc1
#upologismos kerdous pliroforias gia tis lekseis tou leksikou
def calculate_IGs(voc,sum_mes,sum_pos_mes):
    pc0 = sum_pos_mes/sum_mes #pithanothta na einai pos
    pc1 = (sum_mes-sum_pos_mes)/sum_mes #pithanothta na einai neg
    Hbefore = H(pc0,pc1)
    IGs = dict.fromkeys(voc.keys(), 0)#word->IG
    for key in voc:
        IGs[key] = Hbefore - IG(key,voc[key],sum_mes,sum_pos_mes)
    sorted_IGs = dict(sorted(IGs.items(), key=operator.itemgetter(1),reverse=True))
    return sorted_IGs