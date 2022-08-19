from typing import List

from Bio import SeqIO
from loguru import logger


def read_file(file: str, read_index: List) -> List:
    phred_nums = []
    with open(file) as handle:
        record = SeqIO.parse(handle, "fastq")
        index = 0
        logger.info("line information")
        for lin in record:
            if index < read_index[0]:
                continue
            if index >= read_index[1]:
                break
            phred_nums.append(lin.letter_annotations['phred_quality'])
            index += 1

    return phred_nums
