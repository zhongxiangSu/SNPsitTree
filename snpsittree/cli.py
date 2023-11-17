import os
import argparse
from snpsittree.src import *
from snpsittree.main import snpsittree_main

def main():
    # argument parse
    parser = argparse.ArgumentParser(prog='SNPsitTree', description='Form snp vcf file to snp sequence file, Used to construct phylogenetic trees')

    parser.add_argument("species_name_and_work_file",
                        help="Species name and work file", type=str)
    parser.add_argument("Chr_name_list_file",
                        help="Chromosome name list file", type=str)
    parser.add_argument("reference_genome",
                        help="Reference genome fasta file", type=str)

    args = parser.parse_args()

    snpsittree_main(args)
    

if __name__ == '__main__':
    main()
