#!python3
"""
Module to find jaccard distance and cosine distance of given utility matrix. The input is given in file ratings.txt.
A '0' rating means no rating has been given by user for that item
"""
from collections import OrderedDict
from itertools import combinations
import math

# configuration parameters
HIGEST_RATE = 5
LOWEST_RATE = 1
FILE_NAME = "ratings.txt"
HIGH_RATINGS = [3,4,5]
LOW_RATINGS = [1,2]
SEP = 135
fformat = '.3f'

def printJD(res):
	print("The Jaccard distance of all pairs is:")
	for grp in res:
		print(grp, "Jaccard Similarity:", format(float(res[grp][0]/res[grp][1]), fformat), "Jaccard Distance:", 
			format(float((res[grp][1] - res[grp][0])/res[grp][1]), fformat), sep='\t')
	print('\n')

def printCD(res):
	print("The Cosine distance of all pairs is:")
	for grp in res:
		print(grp, "Cosine Distance:", format(res[grp], fformat), sep='\t')
	print('\n')

def printMat(mat):
	ratings = OrderedDict()
	
	for user in mat:
		ratings['cols'] = [item for item in mat[user]]
		ratings['cols'] = '\t|\t'.join(ratings['cols'])
		break

	for user in mat:
		ratings[user] = [str(format(mat[user][item], fformat)) if mat[user][item] is not 0 else ' ' for item in mat[user]]
		ratings[user] = '\t|\t'.join(ratings[user])

	print('='*SEP)
	print('\t', ratings['cols'])
	print('='*SEP)
	for row in ratings:
		if row is not 'cols':
			print(row, '|' + ratings[row], sep='\t')
	print('\n')

def getMatrix(filename):
	f = open(filename, 'r')
	mat = OrderedDict()
	for line in f:
		if not line.startswith('#'):
			data = line.strip().split(' ')
			if data[0] not in mat.keys():
				mat[data[0]] = OrderedDict()
			mat[data[0]][data[1]] = int(data[2])

	return mat


def getBoolmat(mat, highrate=range(1, HIGEST_RATE+1)):
	boolMat = OrderedDict()
	for user in mat:
		if user not in boolMat.keys():
			boolMat[user] = OrderedDict()
		for item in mat[user]:
			if mat[user][item] in highrate:
				boolMat[user][item] = 1
			else:
				boolMat[user][item] = 0
	return boolMat

def getNormalizedMat(mat):
	normMat = OrderedDict()
	for user in mat:
		if user not in normMat.keys():
			normMat[user] = OrderedDict()
		count = 0
		sumi = 0
		for item in mat[user]:
			if mat[user][item] > 0:
				count += 1
				sumi += mat[user][item]

		for item in mat[user]:
			if mat[user][item] > 0:
				normMat[user][item] = float(float(mat[user][item]) - float(sumi/count))
			else:
				normMat[user][item] = 0

			# if mat[user][item] in highrate:
			# 	boolMat[user][item] = 1
			# else:
			# 	boolMat[user][item] = 0
	return normMat

def getJaccardD(mat):

	grps = combinations(mat.keys(),2)
	res = OrderedDict()
	for grp in grps:
		interset = 0
		union = 0
		for item in mat[grp[0]]:
			if mat[grp[0]][item] and mat[grp[1]][item]:
				interset += 1
			if mat[grp[0]][item] or mat[grp[1]][item]:
				union += 1
		res[grp] = (interset, union)

	return res


def getCosineD(mat):

	grps = combinations(mat.keys(),2)
	res = OrderedDict()
	for grp in grps:
		num = 0
		den1 = 0.00
		den0 = 0.00
		for item in mat[grp[0]]:
			num += mat[grp[0]][item] * mat[grp[1]][item]
			den0 += mat[grp[0]][item]*mat[grp[0]][item]
			den1 += mat[grp[1]][item]*mat[grp[1]][item]

		den0 = math.sqrt(den0)
		den1 = math.sqrt(den1)
		res[grp] = float(num/(den0*den1))

	return res


def main():
	uMat = getMatrix(FILE_NAME)
	print("Given matrix is:")
	printMat(uMat)
	print('-'*SEP)

	boolMat = getBoolmat(uMat)
	boolJd = getJaccardD(boolMat)
	boolCd = getCosineD(boolMat)
	print("The boolean matrix is:")
	printMat(boolMat)
	printJD(boolJd)
	printCD(boolCd)
	print('-'*SEP)

	customBoolMat = getBoolmat(uMat, HIGH_RATINGS)
	customBoolJd = getJaccardD(customBoolMat)
	customBoolCd = getCosineD(customBoolMat)
	print("The rounded data matrix is:")
	printMat(customBoolMat)
	printJD(customBoolJd)
	printCD(customBoolCd)
	print('-'*SEP)

	normMat = getNormalizedMat(uMat)
	#normJd = getJaccardD(normMat)
	normCd = getCosineD(normMat)
	print("The normalized matrix is:")
	printMat(normMat)
	#printJD(normJd)
	printCD(normCd)
	print('-'*SEP)


if __name__ == '__main__':
	main()
