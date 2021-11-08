import os
from multiprocessing import Pool
import codecs
import subprocess

import numpy as np
from tqdm import tqdm
import re
from num2words import num2words

from text import _clean_text

def has_numbers(str):
    return any(char.isdigit() for char in str)

def has_alpha(str):
    return any(char.isalpha() for char in str)

def process_speaker(config, speaker, trl):
    in_dir = config["path"]["corpus_path"]
    out_dir = config["path"]["raw_path"]
    sampling_rate = config["preprocessing"]["audio"]["sampling_rate"]
    max_wav_value = config["preprocessing"]["audio"]["max_wav_value"]
    
    os.makedirs(os.path.join(out_dir, speaker), exist_ok=True)

    trl_lines = codecs.open(trl, "r", "ISO-8859-1").readlines()
    for i, line in enumerate(trl_lines):
        if ";" in line and ":" in line:
            utt_id = line.replace("; ", "").replace(":", "").strip()
            base_name = f"GE{speaker}_{utt_id}"
            utt_file = os.path.join(in_dir, "adc", speaker, f"{base_name}.adc.shn")
            raw_file = os.path.join(out_dir, speaker, f'{base_name}.raw')
            wav_file = raw_file.replace(".raw", ".wav")
            try:
                subprocess.check_call(f"shorten -x {utt_file} {raw_file} 2>/dev/null", shell=True)
                subprocess.check_call(f"sox -t raw -r 16000 -e signed-integer -b 16 {raw_file} -t wav {wav_file}.temp && rm -f {raw_file}", shell=True)
                subprocess.check_call(f"sox -G -v 0.9 {wav_file}.temp -r {sampling_rate} {wav_file} && rm {wav_file}.temp", shell=True)
                skipped = False
            except subprocess.CalledProcessError as e:
                print(e.__repr__())
                print(f"skipped {base_name}")
                skipped = True
            if not skipped:
                with open(os.path.join(out_dir, speaker, f"{base_name}.lab"), "w") as f1:
                    tokens = []
                    has_num = False
                    try:
                        for t in re.split("[\s]", trl_lines[i+1].lower()):
                            tokens.append(t)
                    except:
                        print(trl_lines[i+1])

                    f1.write(" ".join(tokens).lower())
                    

def prepare_align(config):
    in_dir = os.path.join(config["path"]["corpus_path"], "adc")
    pool = Pool()
    pool_args = []
    for speaker in tqdm(os.listdir(in_dir)):
        pool_args.append([config, speaker, os.path.join(config["path"]["corpus_path"], "trl", f"GE{speaker}.trl")])
    pool.starmap(process_speaker, tqdm(pool_args, total=len(pool_args)))
    pool.close()
    pool.join()