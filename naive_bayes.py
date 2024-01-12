import math

def calc_prob(Xs,sum_rev,sum_pos_rev):#upologismos pithanothtwn
    new_Xs = {}
    for key in Xs.keys():
        existspos = (Xs[key][1]+1)/(sum_pos_rev+2)#pithanothta na uparxei dedomenou oti exw pos
        existsneg = (Xs[key][0]-Xs[key][1]+1)/(sum_rev-sum_pos_rev+2)#pithanothta na uparxei dedomenou oti exw neg
        new_Xs[key] = [existspos,existsneg]
    return new_Xs
def naive_bayes(review,Xs,vocabulary):
    prob_pos = 0.5

    p0 = 0#pos
    p1 = 0#neg
    for key in Xs.keys():#gia kathe leksi tou lexikou
        index = vocabulary[key]
        if(review[index]>0):#uparxei h leksi sto review afto
            p0 += math.log(Xs[key][0])
            p1 += math.log(Xs[key][1])
        else:#den uparxei h leksi
            p0 += math.log(1-Xs[key][0])
            p1 += math.log(1-Xs[key][1])
    p0 += math.log(prob_pos)
    p1 += math.log(1-prob_pos)
    return p0, p1
def naive_bayes_run(vec_review,typ,Xs,vocabulary):
    
    ans_typ=[]
    res = [[0, 0], [0, 0]]
    for i in range(len(typ)):#gia kathe review
        #vres apantisi naive bayes
        p_pos, p_neg = naive_bayes(vec_review[i],Xs,vocabulary)
        ans = "pos" if p_pos>p_neg else "neg"
        if (ans=='pos'):
            if(ans == typ[i] ):
                res[0][0] += 1#truepositive
            else:
                res[1][0] += 1#falsepositive
        else:
            if(ans == typ[i] ):
                res[1][1] += 1#truenegative
            else:
                res[0][1] += 1#falsenegative
        ans_typ.append(ans)
    return res, ans_typ