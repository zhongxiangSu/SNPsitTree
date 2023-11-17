from snpsittree.src import *
import os

def snpsittree_main(args):
    species_name_and_work_file = args.species_name_and_work_file
    Chr_name_list_file = args.Chr_name_list_file
    reference_genome = args.reference_genome
    get_snp_dict(species_name_and_work_file, Chr_name_list_file, reference_genome)

if __name__ == "__main__":
    pass