import MySQLdb
import sys
import os

readfile = sys.argv[-1]


full_path = os.path.realpath(__file__)



mypath = os.getcwd()
readpath = mypath+'/'+readfile
readfilename = readfile[:-4]
readfilename = readfilename.split('/')
inputdoc = open(readpath, "r")
writepath = mypath+'/'+readfilename[-1]+'.map_anc.inp'
outputdoc = open(writepath, "w")

db=MySQLdb.connect(host="localhost",user="",
                  passwd="",db="test")

print writepath
counter=1
for line in inputdoc:
  if line[0] != '#':
	linesplit = line.split('   ')
	rsid = linesplit[2].split(';')[0]
	if rsid[:2] == 'rs':
	  rsid = rsid[2:]
	  c = db.cursor()
	  c.execute("SELECT * from Anc_allele where snp_id = %s LIMIT 0,1" % (rsid,))
	  anc_id = c.fetchone()
	  c.close()
	  if anc_id:
	    d = db.cursor()
	    d.execute("select allele from Allele where allele_id = %i" % (anc_id[1],))
	    anc = d.fetchone()
	    d.close()
	    if anc[0] == linesplit[3]:
	      ancestral = 1
	      derived = 2
	    elif anc[0] == linesplit[4]:
	      ancestral = 2
	      derived = 1
	    else:
	      ancestral = 1
	      derived = 2
	  else:
	    ancestral = 1
	    derived = 2
	else:
	  ancestral = 1
	  derived = 2
	if linesplit[2]!='.':
	  outputdoc.write("%s %s %s %s %s\n" % (linesplit[2], linesplit[0][3:], linesplit[1], str(ancestral), str(derived)))
	else:
	  outputdoc.write("%s %s %s %s %s\n" % (str(counter), linesplit[0][3:], linesplit[1], str(ancestral), str(derived)))
	  counter = counter+1