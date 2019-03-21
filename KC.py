from collections import Counter
import numpy as np
import os


def KernelFrom2ListsK3RN3L(A,B):
	ret=0
	if(len(A)<len(B)):
		for pair in A.keys():
			a=A[pair]
			b=B[pair]
			if(a<b):
				ret+=a/b
			else:
				ret+=b/a
	else:
		for pair in B.keys():
			a=A[pair]
			b=B[pair]
			if(a<b):
				ret+=a/b
			else:
				ret+=b/a
	return ret
	
def KernelFrom2ListsIntersect(A,B):
	ret=0
	if(len(A)<len(B)):
		for pair in A.keys():
			a=A[pair]
			b=B[pair]
			if(a<b):
				ret+=a
			else:
				ret+=b
			# ret+=min(A[pair],B[pair])
	else:
		for pair in B.keys():
			a=A[pair]
			b=B[pair]
			if(a<b):
				ret+=a
			else:
				ret+=b
	return ret
def KernelFrom2ListsSpectrum(A,B):
	ret=0
	if(len(A)<len(B)):
		for pair in A.keys():
			ret+=A[pair]*B[pair]
	else:
		for pair in B.keys():
			ret+=A[pair]*B[pair]
	return ret
def KernelFrom2ListsPresence(A,B):
	ret=0
	if(len(A)<len(B)):
		for pair in A.keys():
			if(B[pair]!=0):
				ret+=1
	else:
		for pair in B.keys():
			if(B[pair]!=0):
				ret+=1
	return ret
def File2Pgrams(file,pgram=2):
	oneLongTweet = open(file,encoding='utf8').read()
	oneLongTweet = oneLongTweet.lower()
	oneLongTweet=' '.join(oneLongTweet.split())
	return Counter([oneLongTweet[i:i + pgram] for i in range(0, len(oneLongTweet )-pgram +1 )])
	

Dirs=[entry for entry in os.listdir('.') if os.path.isdir(entry)]
assert 'test' in Dirs

X_Train=[]
Y_Train=[]
X_Test=[]

for counter,dir in enumerate(Dirs):
	files=os.listdir(dir)
	for file in files:
		if dir=='test':
			X_Test.append(dir+'/'+file)
		else:
			X_Train.append(dir+'/'+file)
			Y_Train.append(counter)

N_Train=len(X_Train)
N_Test=len(X_Test)
N=N_Train+N_Test



#Make kernel
Kernel=np.empty([N,N], dtype=float)
Cache=np.empty([N, ],dtype=object)

i=0
for file in X_Train+X_Test:
	Cache[i]=File2Pgrams(file)
	norma=1+sum(Cache[i].values())
	for pair in Cache[i].keys():
		Cache[i][pair]/=norma
	i=i+1
	
	
	
for i in range(N):
	for j in range(i,N):
		Kernel[i][j]=KernelFrom2ListsK3RN3L(Cache[i],Cache[j])
		Kernel[j][i]=Kernel[i][j]

#normalizare
from math import sqrt
for i in range(N):
	for j in range(N):
		if(i!=j):
			Kernel[i][j]/=sqrt(Kernel[i][i]*Kernel[j][j]+1)

for i in range(N):
	Kernel[i][i]=1

	
Y_Train=np.array(Y_Train)

from sklearn.svm import NuSVC

nu=0.1
for _ in range(1):
	clf = NuSVC(nu,kernel='precomputed', )#,#verbose =True,      shrinking=False,
	
	# #Bun de kfold
	#from sklearn.cross_validation import LeaveOneOut
	# pr=[]
	# loo = LeaveOneOut(N_Train)
	# for train, test in loo:
		# clf.fit(Kernel[np.ix_(train,train)], Y_Train[train])
		# pr.append(clf.predict(Kernel[np.ix_(test,train)])==Y_Train[test])
	# print(np.array(pr).mean())
	
	clf.fit(Kernel[0:N_Train,0:N_Train], Y_Train[0:N_Train])
	AccTrain=(clf.predict(Kernel[0:N_Train,0:N_Train])==Y_Train[0:N_Train]).mean()
	# AccTest=(clf.predict(Kernel[N_Train:,0:N_Train])==Y[N_Train:]).mean()
	Preds=clf.predict(Kernel[N_Train:,0:N_Train])
	for i in range(0,len(Preds)):
		print(X_Test[i],'->',Dirs[Preds[i]])
	AccTest=0
	print('nu= ',nu,' acc pe train: ' ,AccTrain,' Acc pe test: ',AccTest)
	nu*=0.8