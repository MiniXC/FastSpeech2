import urllib

from rpy2.robjects.packages import importr
from ipapy import ipastring
from rpy2.robjects.vectors import StrVector

utils = importr("utils")
utils.install_packages(StrVector(["ipa"]))
ipa = importr("ipa")

file = urllib.request.urlopen("https://raw.githubusercontent.com/kaldi-asr/kaldi/master/egs/gp/s5/conf/xsampa_map/German")
gp2x = {}
for line in file:
    if "\t" in line.decode():
        gp_phon, x_phon = line.decode().split("\t")
        gp_phon = gp_phon.strip()
        x_phon = x_phon.strip()
        gp2x[gp_phon] = x_phon

print(gp2x)

conversion_cache = {}

def convert_phones(phones, from_set, to_set="ipa"):
    results = []
    for p in phones:
        key = (p, from_set, to_set)
        if key in conversion_cache:
            results.append(conversion_cache[key])
        else:
            if from_set == "gp":
                if p not in ["sil", "sp", "spn"]:
                    n_p = convert_phones([gp2x[p]], "xsampa", to_set)[0]
                else:
                    n_p = "spn"
            else:
                if p not in ["sil", "sp", "spn"]:
                    n_p = ipa.convert_phonetics(p, from_set, to_set)[-1]
                else:
                    n_p = "spn"
            conversion_cache[key] = n_p
            results.append(n_p)
    return results
