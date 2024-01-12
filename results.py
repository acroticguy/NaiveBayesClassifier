import matplotlib.pyplot as plt
import plotly.graph_objects as go
import csv
def calculate(res):
    try:
        acc = (res[0][0]+res[1][1])/(res[0][0]+res[0][1]+res[1][0]+res[1][1])
    except:
        acc = 0
    try:
        p1 = res[0][0]/(res[0][0]+res[1][0])
    except:
        p1 = 0
    try:
        r1 = res[0][0]/(res[0][0]+res[0][1])
    except:
        r1 = 0
    try:
        p2 = res[1][1]/(res[1][1]+res[0][1])
    except:
        p2 = 0
    try:
        r2 = res[1][1]/(res[1][1]+res[1][0])
    except:
        r2 = 0
    try:
        f1 = (2*(p1*r1))/(p1+r1)
    except:
        f1 = 0
    try:
        f2 = (2*(p2*r2))/(p2+r2)
    except:
        f2 = 0
    return acc,p1,r1,p2,r2,f1,f2
def save(string,name,x,y1,y2,label):
    write_csv(string,name,x,y1,y2)
    plt.title(name)
    plt.xlabel('Number of training examples')
    plt.ylabel(name)
    axes = plt.gca()
    axes.set_ylim([0,1.1])
    line1 = plt.plot(x, y1,label=label)
    line2 = plt.plot(x, y2,label="training")
    plt.legend(fancybox=True, framealpha=1, shadow=True, borderpad=1)
    plt.savefig(string+"_res\\"+name+"_"+string+".png")
    plt.close('all')
#x,acc1,acc2,prec_pos1,prec_pos2,recall_pos1,recall_pos2,prec_neg1,prec_neg2,recall_neg1,recall_neg2,f1_score_pos1,f1_score_pos2,f1_score_neg1,f1_score_neg2
def plot_results(label, string, x,resAlt,resTrain):
    acc1 = []
    prec_pos1 = []
    recall_pos1 = []
    prec_neg1 = []
    recall_neg1 = []
    f1_score_pos1 = []
    f1_score_neg1 = []
    acc2 = []
    prec_pos2 = []
    recall_pos2 = []
    prec_neg2 = []
    recall_neg2 = []
    f1_score_pos2 = []
    f1_score_neg2 = []
    for i,j in zip(resAlt,resTrain):
        acc,p1,r1,p2,r2,f1,f2 = calculate(i)
        acc1.append(acc)
        prec_pos1.append(p1)
        recall_pos1.append(r1)
        prec_neg1.append(p2)
        recall_neg1.append(r2)
        f1_score_pos1.append(f1)
        f1_score_neg1.append(f2)
        acc,p1,r1,p2,r2,f1,f2 = calculate(j)
        acc2.append(acc)
        prec_pos2.append(p1)
        recall_pos2.append(r1)
        prec_neg2.append(p2)
        recall_neg2.append(r2)
        f1_score_pos2.append(f1)
        f1_score_neg2.append(f2)
    #Acc
    save(string,"Accuracy",x,acc1,acc2,label)
    
    #Precision pos
    save(string,'Precision_for_pos',x,prec_pos1,prec_pos2,label)
    
    #Precision neg
    save(string,'Precision_for_neg',x,prec_neg1,prec_neg2,label)
    
    #Recall pos
    save(string,'Recall_for_pos',x,recall_pos1,recall_pos2,label)
    
    #Recall neg
    save(string,'Recall_for_neg',x,recall_neg1,recall_neg2,label)
    
    #F1 score pos
    save(string,'F1_score_for_pos',x,f1_score_pos1,f1_score_pos2,label)
    
    #F1 score neg
    save(string,'F1_score_for_neg',x,f1_score_neg1,f1_score_neg2,label)

def write_csv(string,fname,x,y1,y2):
    with open(string+"_res\\"+fname+".csv", 'w', newline='') as employee_file:
        writer = csv.writer(employee_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(['x', 'test', 'training'])
        for k, l, m in zip(x,y1,y2):
            writer.writerow([k,l,m])