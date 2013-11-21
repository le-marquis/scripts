# -*- coding: utf-8 -*-
"""
Created on Wed Aug  7 13:40:40 2013

@author: malte
"""
from os import listdir
from os.path import isfile, join
import MySQLdb
import urllib,urllib2

db_ucsc = MySQLdb.connect(host="genome-mysql.cse.ucsc.edu",user="genome",db="hg19")
d = db_ucsc.cursor()
db=MySQLdb.connect(host="134.245.19.194",user="mruehlemann",
                  passwd="change@once",db="phenodb")
c = db.cursor()
c.execute("SELECT * FROM exome_analysis where multi_allelic = 0")
all_snps = c.fetchall()
for snp in all_snps:
	chrom = snp[2]
	coord = int(snp[3])
	d.execute('SELECT geneSymbol FROM knownGene, kgXref WHERE chrom="%s" and txStart<%i and txEnd>%i and name = kgID' % (chrom, coord, coord,))
	all_genes = d.fetchall()
	print snp[0]
	for gene in all_genes:
		c.execute("SELECT count(*), gene_id FROM gene_table where gene_id = '%s'" % (gene[0]))
		entry  = c.fetchone()
		count = entry[0]
		if count == 0:
			c.execute("Insert into gene_table (gene_id) values ('%s');" % (gene[0]))
			db.commit()
		c.execute("SELECT ID FROM gene_table where gene_id = '%s'" % (gene[0]))	
		ID = c.fetchone()[0]
		c.execute("Insert ignore into snpXgene (snp_id, gene_id) values (%i, %i);" % (snp[0], ID))
		db.commit() 

# 
# for line in readfile:
#     splitline = line.split(' ')
#     splitline[4] = splitline[4][:-1]
#     chrom = splitline[2]
#     try:
#         reg_start = int(splitline[3])
#         reg_end = int(splitline[4])
#         d.execute('SELECT geneSymbol FROM knownGene, kgXref WHERE chrom="%s" and txStart>%i and txEnd<%i and name = kgID' % (chrom, reg_start, reg_end,))
#         all_genes = d.fetchall()
#         
#         for gene in all_genes:
#             if gene[0] not in all_symbols:
#                 all_symbols.append(gene[0])
#         print chrom, reg_start, reg_end
#     except:
#         pass
# 
# all_symbols = " \n".join(all_symbols)
# writefile.write('%s' % (all_symbols))