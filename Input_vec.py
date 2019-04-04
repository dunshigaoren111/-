import copy
import random
import tensorflow as tf
def produce_inputs(infile,skip_window,num_skips):
    XS=[]
    YS=[]
    fin=open(infile,'r')
    lines=fin.readlines()
    for line in lines:
        line=line.strip().split()
        Xs, Ys=get_XYs(line,skip_window,num_skips)
        XS+=Xs
        YS+=Ys
    fin.close()
    return XS,YS


def get_XYs(line,skip_window,num_skips):
    Ys=[]
    Xs=[]
    for i in range(len(line)):
        if(i<skip_window and i+skip_window<len(line)):
            lin = copy.deepcopy(line[:i]) + copy.deepcopy(line[i + 1: i+1+skip_window])

        elif(i>=skip_window and i+skip_window<len(line)):
            lin = copy.deepcopy(line[i -skip_window:i])+copy.deepcopy(line[i +1:i+1+skip_window])

        elif(i>=skip_window and i+skip_window>len(line)):
            lin = copy.deepcopy(line[i - skip_window:i]) + copy.deepcopy(line[i + 1:])

        else:
            lin = copy.deepcopy(line[:i]) + copy.deepcopy(line[i + 1:])


        result= get_Ys(lin, num_skips)
        Xs += [int(line[i]) for j in range(len(result))]
        Ys +=result
    return Xs,Ys




def get_Ys(lin,num_skips):
    result=[]
    if(num_skips>=len(lin)):
        return [int(lin[i]) for i in range(len(lin))]
    else:
        for i in range(num_skips):
            index=random.randint(0,len(lin)-1)
            result.append(int(lin.pop(index)))
    return result

def test():
    a=[1,2,3]
    # a.append(1)
    # b=int(a)

    print(tf.shape(a))
# test()