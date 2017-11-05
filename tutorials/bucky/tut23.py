fw = open('sample.txt', 'w')
fw.write('elo elo 3 2 0\n')
fw.write('jutro z bara wchodze bez gadania\n')
fw.close()

fr = open('sample.txt', 'r')
text = fr.read()
print(text)
fr.close()
