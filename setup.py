# coding utf8
import setuptools
from snpsittree.versions import get_versions

with open('README.md') as f:
    LONG_DESCRIPTION = f.read()


setuptools.setup(
    name='SNPsitTree',
    version=get_versions(),
    author="zhongxiang Su",
    author_email="suzhongxiang@mail.kib.ac.cn",
    description="Form snp vcf file to snp sequence file, Used to construct phylogenetic trees",
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    url="https://github.com/zhongxiangSu/SNRsitTree",
    
    entry_points={
        'console_scripts': [
            'SNPsitTree = snpsittree.cli:main',
        ],
    },
    packages=setuptools.find_packages(),
    install_requires=[
        'pandas>=1.1.5',
        'numpy>=1.19.5',
        'biopython>=1.78',
    ],
    python_requires='>=3.5',
)
