# Conversion of VCF file with multiple samples to file format compatible with rehh (R Package).
# Breaks down phased VCF file into "haplotypes" for each individual and chromosome
# Output are one file for each chromosome with all phased haplotypes of the individual samples
#
# Usage: python vcf_to_rehh-compatible vcf-file.vcf

import os, errno
from os import listdir
from os.path import isfile, join
import sys
import MySQLdb

# Used to create folders to sort output files
def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc: # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else: raise

readfile = sys.argv[-1]
db=MySQLdb.connect(host="localhost",user="",db="test")

full_path = os.path.realpath(__file__)

mypath = os.getcwd()
readpath = mypath+'/'+readfile
readfilename = readfile[:-4]
readfilename = readfilename.split('/')
chromosomes = []
for z in range(1,23):
	chrom = 'chr'+str(z)
	chromosomes.append(chrom)
#chromosomes.append('chrY')
#chromosomes.append('chrX')
#chromosomes.append('chrM')

print chromosomes
line_counter = 0
inputdoc = open(readpath, "r")
#exclude_file = open(mypath+'exclude.txt')
#exclude = []
#for line in exclude_file:
#  marker = line.rstrip()
#  exclude.append(marker)
mkdir_p(mypath+'/'+readfilename[-1])
writepath = mypath+'/'+readfilename[-1]+'/'+readfilename[-1]+'.map_anc.inp'
outputdoc = open(writepath, "w")
counter = 1

#All lines from the input VCF file are added to a list, first entry of the list (index 0) is the header line of the VCF file with all column descriptions
#For every entry an integer is added which corresponds to the ID in the MySQL table for the same entry
all_snps = []
print 'processing file'
for line in inputdoc:
	  splitter = '\t'
	  linesplit = line.split(splitter)
	  if linesplit[0][0] != '#':
	    chr = linesplit[0].split('chr')
	    chr = filter(None, chr)[0]
	    if linesplit[2]!='.':
	      outputdoc.write("%i_%s %s %s 1 2\n" % (counter, linesplit[2], chr, linesplit[1],))
	      counter = counter+1
	    else:
	      outputdoc.write("%s %s %s 1 2\n" % (str(counter), chr, linesplit[1],))
	      counter = counter+1
	  if linesplit[0] == '#CHROM' or linesplit[0][0] != '#':  
		if linesplit[2][:2] == 'rs':
			rsid = linesplit[2][2:].split(';')[0]
			c = db.cursor()
			c.execute('SELECT allele_id FROM Anc_allele WHERE snp_id = "%s" LIMIT 0,1' % (rsid,))
			res = c.fetchone() # check whether reference or variant is ancestral; 
			c.close()
			if res:
			  d = db.cursor()
			  d.execute('SELECT allele FROM Allele WHERE allele_id = "%s" LIMIT 0,1' % (res[0],))
			  anc_al = d.fetchone()
			  if anc_al:
			    if str(anc_al[0]) == str(line[4]):
			      anc_allele=2
			    else:
			      anc_allele=1
			  else:
			      anc_allele=1
			else:
			  anc_allele = 1
		else:
		  anc_allele=1
		linesplit.append(line_counter)
		linesplit.append(anc_allele)
		if line_counter == 1:
		   print linesplit
		all_snps.append(linesplit)
		line_counter = line_counter + 1


writepath_4 = mypath+'/'+readfilename[-1]+'/'+readfilename[-1]+'.logfile.txt'



#Now each chromosome is handled as one

for i in chromosomes:
	print 'processing '+i
	this_chrom = []
	snp_counter = 0
	this_chrom.append(all_snps[0]) # header row from vcf file
	mkdir_p(mypath+'/'+readfilename[-1]+'/'+i)
	writepath_1 = mypath+'/'+readfilename[-1]+'/'+i+'/'+readfilename[-1]+'.'+i+'.rehh-compatible.txt'
	writepath_3 = mypath+'/'+readfilename[-1]+'/'+i+'/'+readfilename[-1]+'.'+i+'.logfile.txt'
	for snp in all_snps: # add all snps to "this_chrom" that belond to the current chromosome
		chr = snp[0].split('chr')
		chr = filter(None, chr)[0]
		chr = 'chr'+chr
		if str(chr) == str(i):
		    variants = snp[4].split(',')
		    if len(variants) == 1:
				this_chrom.append(snp)
				snp_counter = snp_counter + 1
	rehh = open(writepath_1, "w")
	chrom_logfile = open(writepath_3, "w")
	marker_counter_all = 1    
	marker_counter = 1
	
	#for line in this_chrom:
	  #if line[0] != '#CHROM':
	    #if marker_counter_all not in multi_allelic:
		#marker.write('%i_%s %s %s %s %s \n' % (marker_counter, line[2], line[0], line[1], line[3], line[4]))
		#marker_counter = marker_counter + 1
	    #marker_counter_all = marker_counter_all + 1

	sample_counter = 1
	sample_count = len(this_chrom[0])-11
	marker_count = len(this_chrom)-1
	hard_columns = ['#CHROM','POS','ID','REF','ALT','QUAL','FILTER','INFO','FORMAT']
	for element in this_chrom[0][:-2]:
	  if element not in hard_columns:
		print 'processing sample '+str(sample_counter)+' of '+str(sample_count)+': '+element.rstrip()
		write_line_1 = str((sample_counter*2)-1)+' '			# each line corresponds to one chromosome, two chromosomes for each individual
		write_line_2 = str(sample_counter*2)+' '
		x = this_chrom[0].index(element)
		for line in this_chrom[1:]:
		  line[x] = line[x].rstrip()
		  anc_allele = line[-1]
		  if line[x][1] == '|':
			if anc_allele == 1:
				if line[x][0] == '0':
					  write_line_1 = write_line_1 + '1 '
				elif line[x][0] == '1':
					  write_line_1 = write_line_1 + '2 '
				else:
					  print line[-2]+' allele 1 unknown'
					 
				if line[x][2] == '0':
					  write_line_2 = write_line_2 + '1 '
				elif line[x][2] == '1':
					  write_line_2 = write_line_2 + '2 '
				else:
					  print line[-2]+' allele 2 unknown'
			elif anc_allele == 2:
				if line[x][0] == '0':
					  write_line_1 = write_line_1 + '2 '
				elif line[x][0] == '1':
					  write_line_1 = write_line_1 + '1 '
				else:
					  print line[-2]+' allele 1 unknown'
					 
				if line[x][2] == '0':
					  write_line_2 = write_line_2 + '2 '
				elif line[x][2] == '1':
					  write_line_2 = write_line_2 + '1 '
				else:
					  print line[-2]+' allele 2 unknown'
		  else:
			write_line_1 = write_line_1 + '0 '
			write_line_2 = write_line_2 + '0 '
		rehh.write('%s\n%s\n' % (write_line_1, write_line_2,))
		sample_counter = sample_counter + 1

#writepath_2 = mypath+'/'+readfilename[-1]+'/'+readfilename[-1]+'.marker-map.inp' # output file
#marker = open(writepath_2, "w")
#c = db.cursor()
#c.execute('SELECT concat(ID,"_",rsid," ",substr(chr,4)," ",position," 1 2") from exome_analysis where exclude = 0;')




print writepath
counter=1
for line in inputdoc:
  if line[0] != '#':
	linesplit = line.split(' ')
	print linesplit
	#rsid = linesplit[2].split(';')[0]
	#if rsid[:2] == 'rs':
	  #rsid = rsid[2:]
	  #c = db.cursor()
	  #c.execute("SELECT * from Anc_allele where snp_id = %s LIMIT 0,1" % (rsid,))
	  #anc_id = c.fetchone()
	  #c.close()
	  #if anc_id:
	    #d = db.cursor()
	    #d.execute("select allele from Allele where allele_id = %i" % (anc_id[1],))
	    #anc = d.fetchone()
	    #d.close()
	    #if anc[0] == linesplit[3]:
	      #ancestral = 1
	      #derived = 2
	    #elif anc[0] == linesplit[4]:
	      #ancestral = 2
	      #derived = 1
	    #else:
	      #ancestral = 1
	      #derived = 2
	  #else:
	    #ancestral = 1
	    #derived = 2
	#else:
	  #ancestral = 1
	  #derived = 2
	if linesplit[2]!='.':
	  outputdoc.write("%s %s %s 1 2\n" % (linesplit[2], linesplit[0][3:], linesplit[1],))
	  counter = counter+1
	else:
	  outputdoc.write("%s %s %s 1 2\n" % (str(counter), linesplit[0][3:], linesplit[1],))
	  counter = counter+1


