import subprocess
from matplotlib import image, pyplot
from numpy import asarray

dict={'nhưng':4, 'sự':7, 'thực_hiện':5, 'sự_thực':7, 'hiện':7, 'vẫn':6, 'còn':6, 'chưa':4, 'phù_hợp':6}
s = "nhưng sự thực hiện vẫn còn chưa phù hợp"
def makeSymbols(dictionary):
	f = open('sym.txt', "wt", encoding='utf-8')
	i = 0
	f.write('# {}\n'.format(i))
	for word in dictionary:
		i += 1
		f.write("{} {}\n".format(word, i))
	f.close()

def WFSTSegmentation(dictionary, sent):
	words = sent.split()
	f = open("tmp.txt", "wt", encoding='utf-8')
	nwords = len(words)
	i = 0
	for i in range(nwords):
		for j in range(4):
			if i + j >= nwords:
				break
			word = words[i]
			for k in range(1, j+1):
				word = word + "_" + words[i+k]
			weight = dict.get(word)
			if weight == None:
				continue
			f.write("{} {} {} {} {}\n".format(i, i+j+1, word, word, weight))
	f.write("{}".format(nwords))
	f.close()

	process = subprocess.Popen(["fstcompile", "-isymbols=sym.txt", "-osymbols=sym.txt", "tmp.txt", "tmp.fst"])
	process.wait()
	process = subprocess.Popen(["fstdraw", "-portrait", "-isymbols=sym.txt", "-osymbols=sym.txt", "tmp.fst", "tmp.dot"])
	process.wait()
	process = subprocess.Popen(["dot", "-Tpng", "tmp.dot", "-otmp.png"])
	process.wait()
	img = image.imread("tmp.png")
	pyplot.imshow(img)
	pyplot.axis('off')
	pyplot.show()

	process = subprocess.Popen(["fstshortestpath", "tmp.fst", "path.fst"])
	process.wait()
	process = subprocess.Popen(["fstdraw", "-portrait", "-isymbols=sym.txt", "-osymbols=sym.txt", "path.fst", "path.dot"])
	process.wait()
	process = subprocess.Popen(["dot", "-Tpng", "path.dot", "-opath.png"])
	process.wait()
	img = image.imread("path.png")
	pyplot.imshow(img)
	pyplot.axis('off')
	pyplot.show()
	
makeSymbols(dict)
WFSTSegmentation(dict, s)
