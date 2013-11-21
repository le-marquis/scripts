import os
from os import listdir
from os.path import isfile, join
import sys
import MySQLdb
import twobitreader

readfile = sys.argv[-1]

mypath = os.getcwd()
full_path = os.path.realpath(__file__)
print mypath+'/twobit_hg19/hg19.2bit'
#hg19 = twobitreader.TwoBitFile(mypath+'/twobit_hg19/hg19.2bit')
#db=MySQLdb.connect(host="134.245.19.194",user="mruehlemann",
#                  passwd="change@once",db="phenodb")



gene_list = [] # list of all genes in exome

list_of_snps_from_vcf_file # read from vcf.file
for SNP in list:
	gene_ID = ?# get gene ID from UCSC
	