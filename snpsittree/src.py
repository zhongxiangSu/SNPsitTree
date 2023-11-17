import os 
import pandas as pd
from Bio import SeqIO

def judege_file(file):
    if os.path.exists(file):
        return False
    else:
        return True
    
def get_input_file(work_file_list_file):
    work_file = {}
    with open(work_file_list_file, 'r') as f:
        for line in f:
            work_file[line.strip().split('\t')[0].replace(' ','')] = (line.strip().split('\t')[1].replace(' ','')).replace('\t','')
    return work_file

def get_Chr_name(Chr_name_list_file):
    Chr_name_list = []
    with open(Chr_name_list_file, 'r') as f:
        for line in f:
            Chr_name_list.append(line.strip())
    return Chr_name_list

def read_vcf(vcf_file, Chr_name_list):
    df = pd.read_csv(vcf_file, sep='\t', comment='#', header=None)
    df = df[~df[0].str.startswith('##')]
    df.reset_index(drop=True, inplace=True)
    snp_info = {}
    for name in Chr_name_list:
        snp_info[name] = {}
    for index in df.index:
        info = df.loc[index][7]
        info = info.split(';')
        if info[1] == 'AF=1.00':
            chr_name = df.loc[index][0]
            if chr_name in Chr_name_list:
                pos = df.loc[index][1]
                ref = df.loc[index][3]
                alt = df.loc[index][4]
                snp_info[chr_name][pos] = [ref, alt]
    return snp_info

def read_fasta_to_dict(fasta_file):
    output_dict = {}  
    for record in SeqIO.parse(fasta_file, "fasta"):
        output_dict[record.id] = str(record.seq)
    return output_dict


def write_snpseqence(out_put_file, name, ZGeB_snp_seq_dict, Chr_name_list):
    with open (out_put_file, 'a') as f:
        f.write('\n' + '>' + name + '\n')
        for i in Chr_name_list:
            x = ''.join(ZGeB_snp_seq_dict[i])
            f.write(x)


def get_snp_seqence(Chr_name_list,union_snp_sit_dict,reference_dict,sample_snp_dict):
    ZGeB_snp_seq_dict = {}
    for chr_name in Chr_name_list:
        ZGeB_snp_seq_chr_list = []
        for pos in union_snp_sit_dict[chr_name]:
            if pos in sample_snp_dict[chr_name] and sample_snp_dict[chr_name][pos][0] == reference_dict[chr_name][pos-1]:
                ZGeB_snp_seq_chr_list.append(sample_snp_dict[chr_name][pos][1]) 
            
            else:
                ZGeB_snp_seq_chr_list.append(reference_dict[chr_name][pos-1])

        ZGeB_snp_seq_dict[chr_name] = ZGeB_snp_seq_chr_list
    return ZGeB_snp_seq_dict


def get_reference_seq(Chr_name_list, union_snp_sit_dict, reference_dict):
    reference_snp_dict = {}
    for chr_name in Chr_name_list:
        reference_snp_dict[chr_name] = []
        for i in union_snp_sit_dict[chr_name]:
            reference_snp_dict[chr_name].append(reference_dict[chr_name][i-1])
    return reference_snp_dict


def get_snp_dict(species_name_and_work_file, Chr_name_list_file, reference_file):
    out_put_file = os.getcwd() + 'snp_seq.fa' 
    if judege_file(out_put_file) == True:
        Chr_name_list= get_Chr_name(Chr_name_list_file)
        work_file_dict = get_input_file(species_name_and_work_file)
        sample_snp_dict = {}
        union_snp_sit_dict = {}
        reference_dict = read_fasta_to_dict(reference_file)
        for i in work_file_dict:
            sample_snp_dict[i] = read_vcf(work_file_dict[i], Chr_name_list)
            break
        for chr_name in Chr_name_list:
            union_snp_sit_dict[chr_name] = []
            for sample in sample_snp_dict:
                union_snp_sit_dict[chr_name].extend(list(sample_snp_dict[sample][chr_name].keys()))
            union_snp_sit_dict[chr_name] = list(set(union_snp_sit_dict[chr_name]))
            union_snp_sit_dict[chr_name].sort()
        reference_snp_dict = get_reference_seq(Chr_name_list, union_snp_sit_dict, reference_dict)

        for sample_name in sample_snp_dict:
            snp_seq_dict = get_snp_seqence(Chr_name_list, union_snp_sit_dict, reference_dict, sample_snp_dict[sample_name])
            write_snpseqence(out_put_file, sample_name, snp_seq_dict, Chr_name_list)
        write_snpseqence(out_put_file, 'reference', reference_snp_dict, Chr_name_list)
    else:
        print('The output_file already exists')
        os.sys.exit()   # type: ignore