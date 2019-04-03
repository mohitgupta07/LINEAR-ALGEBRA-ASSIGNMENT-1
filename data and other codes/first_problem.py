import argparse
def a(FILE):
    f=open(FILE,'r')
    n,m,A=4,4,[]
    B=list(map(float,f.readline().strip().split()))
    for i in range(0,n):
        A.append(list(map(float,f.readline().strip().split())))
        A[i].append(B[i])
    M=list(map(float,f.readline().strip().split()))
    solver(A,M,n,m,'output_problem1_part1.txt')
    f.close()    
def b(FILE):
    f=open(FILE,'r')
    n,m=map(int,f.readline().strip().split())
    B=list(map(float,f.readline().strip().split()))
    A=[]
    for i in range(0,n):
        A.append(list(map(float,f.readline().strip().split())))
        A[i].append(B[i])
    M=list(map(float,f.readline().strip().split()))
    solver(A,M,n,m,'output_problem1_part2.txt')
    f.close()
    
def solver(A,M,n,m,FILE):#A is augmented Matrix, can simply make m=m+1
    #Step1:- Reduce to Upper Triangler matrix <echolen form> Also memorizing each operation
    Operations,K,I,free,basic,pivot,flag=[],-1,-1,[],[],[],0
    while(K<m and I<(n-1)):#here k<m is correct as k==m is B matrix so it's good.
        I+=1#row for pivot...
        K+=1#Column at which pivot will occur ...worst case k==m
        #if(I==n): either I< n-1 in while loop or use this and make I<n
        #    break
        flag=0
        while(A[I][K]==0):
            flag=0
            for i in range(I+1,n):                
                if(A[i][K]!=0):#checking for non-zero column for pivot possibility
                    Operations.append(['SWITCH',I,i])
                    flag=1
                    A[I],A[i]=A[i],A[I]#perform switch
                    break
                #end of for loop...
            if(flag==0):#add free variable and move on.
                free.append(K)
                K+=1
            if(K>m or I>=n):#I>=n is redundant here. But leave it for now.
                #Ops... No more pivot left.
                flag=2#since I dont know how to add label so better use flag to get out.
                break
        pass#end of while loop.
        if(flag==2):
            break#CRAP! need to exit the loop...
        #We now have a non-zero column entry so add a basic variable to our list
        basic.append(K)
        pivot.append((I,K))
        #Converting the row below the pivot K to 0.
        scale=1/float(A[I][K])
        Operations.append(['MULTIPLY',scale,I])#adding to operations list.
        A[I]=SCALE(A,I,scale)#scaling done...returns a row
        #print(A)
        A,ops=ConvertRowsToZero(A,I,K,n)
        if(len(ops)!=0):#sometimes zero operations can occur
            Operations.append(ops)
    pass#end of outer while loop
    #Add those free variables which were unreachable in step1 and couldnt get added.
    for i in range(basic[-1]+1,m):
        free.append(i)# add i to free list...       
    #Step2:-Convert into identity matrix if possible..simply reduced echolen form...
    #to do so make each column zero which has a basic variable(pivot) in it and obviously except the pivot.
    for i,k in pivot:
        A,ops=MakeItReduced(A,i,k)
        if(len(ops)!=0):#sometimes zero operations can occur
            Operations.append(ops)        
    #Step3:-Get Free variables:THis task is required to be done for question 1.
    isIn=isInconsistent(basic,m)#returns true if inconsistent else false
    maxLimitCrossed=False
    free=list(set(free))
    f=open(FILE,'w')
    if(not(isIn)):
        equations=CreateX(A,free,pivot,n,m)
        X=[1 for i in range(0,m)]
        maxfree=1
        #print(free)
        if m in free:
            free.remove(m)
        #print(free)
        for i in free:
            if i!=m:
                #print M[i]
                maxfree*=M[i]
        xf=len(free)-1#current incrementer.
        maxfree=int(maxfree)
        #print(maxfree)
        for _ in range(0,int(maxfree)):
            #print(_,xf,free[xf],m, free ,"previous X: ", X)
            maxLimitCrossed=False
            for i in equations:
                #print(i)
                exec(i)
            for i in range(0,m):
                if( X[i]>M[i] or X[i]<=0):
                    maxLimitCrossed=True
                    break
                if isinstance(X[i],int):
                    X[i]=round(X[i])
                if isinstance(X[i],float):
                    X[i]=round(X[i],3)
             
            if(maxLimitCrossed==False):
                break
            '''for xf in free:
                #print(xf)
                if xf<m and X[xf]<=M[xf]:
                    X[xf]+=1'''
            
            if  X[free[xf]]<M[free[xf]]:
                X[free[xf]]+=1
            else:
                xk=xf-1
                X[free[xf]]=1
                while xk>=0:
                    if  X[free[xk]]<=M[free[xk]]:
                        X[free[xk]]+=1
                        break
                    else:
                        X[free[xk]]=1
                        xk=xk-1
                    
        if(not(maxLimitCrossed)):
    
            if(len(free)==0):
                print('EXACTLY ONE!')
                sx=' '.join(map(str,X[0:m]))
                print(sx)
                f.writelines(['EXACTLY ONE!\n',sx,'\n'])    
            else:#inf soln...
                print('MORE THAN ONE!')
                sx=' '.join(map(str,X[0:m]))
                print(sx)
                sf='free Variables={'
                for fr in free:
                    sf+=' X['+str(fr)+'],'
                sf+='}'
                sb=sf+' Equations={'
                sb+=' ; '.join(map(str,equations[::-1]))
                sb+='}'
                print(sb)
                f.writelines(['MORE THAN ONE!\n',sx,'\n',sb,'\n'])         
    if(isIn or maxLimitCrossed):#no solution.
        print 'NOT POSSIBLE, SNAPE IS WICKED!'
        f.write('NOT POSSIBLE, SNAPE IS WICKED!\n')
    f.close()#end of COdE solver
def SCALE(A,I,scale):
    return [i*round(scale,10) for i in A[I]]
def ConvertRowsToZero(A,I,K,n):
    ops=[]
    for i in range(I+1,n):
        scale=-1*float(A[i][K])
        if(scale==0):
            continue
        ops.append(['MULTIPLY&ADD',scale,I,i])
        tmpI=SCALE(A,I,scale)#getting scaled value in tmpI.
        A[i]=[round(x+y,10) for x,y in zip(tmpI,A[i])]#element-wise addition. Thanks Python!
    return A,ops        
def MakeItReduced(A,I,K):
    ops=[]
    for i in range(0,I):
        #print(A[i])
        scale=-1*float(A[i][K])
        if(scale==0):
            continue
        ops.append(['MULTIPLY&ADD',scale,I,i])
        tmpI=SCALE(A,I,scale)#getting scaled value in tmpI.
        tmpAdd=[round(x+y,10) for x,y in zip(tmpI,A[i])]#element-wise addition. Thanks Python!
        A[i]=tmpAdd#update the ith row.
    return A,ops
def CreateX(A,free,pivot,n,m):
    equations=[]
    revpivot=pivot[::-1]
    X=[1 for i in range(0,m)]
    for i in free:
        if(i<m):
            X[i]='X['+str(i)+']'
    for i,k in revpivot:
        equation='X['+str(k)+']'+'='+str(A[i][-1])
        for j in range(k+1,m):
            if(A[i][j]==0):
                continue
            equation+='-'+str(A[i][j])+'*'+str(X[j])
        equations.append(equation)
    return equations
def isInconsistent(basic,m):
    for i in basic:
        if(i==m):
            return True
    return False
#parser starts
parser = argparse.ArgumentParser(description='Problem 1.')
parser.add_argument('filename', metavar='<FILENAME.TXT>', type=str,
                    help='file name.txt for the problem1')
parser.add_argument('-part=one', dest='func', action='store_const',
                    const=a, 
                    help='execution of part one')
parser.add_argument('-part=two', dest='func', action='store_const',
                    const=b,
                    help='execution of part two')

args = parser.parse_args()
args.func(args.filename)
#parser ends


'''0.1 0.3 0.2 0.4 27
0.3 0.3 0.2 0.1 21
0.4 0.1 0.4 0.1 22
0.1 0.2 0.1 0.2 16'''

'''
0.1 0.3 0.2 0.4 
0.3 0.3 0.2 0.1 
0.4 0.1 0.4 0.1 
0.1 0.2 0.1 0.2
'''

'''
27 21 22 16
0.1 0.3 0.2 0.4
0.3 0.3 0.2 0.1
0.4 0.1 0.4 0.1
0.1 0.2 0.1 0.2
33 35 46 57
'''

'''
3 2
10 20 30
0.1 0.2
0.3 0.4
0.2 0.2
100 100
'''
