import re
import os
import json
from pathlib import Path

REG_1 = re.compile(r"[\r\n\t\W0-9()-]")
REG_2 = re.compile(r"\s+.\s+")
REG_3 = re.compile(r"\s{2,}")


EXT = '.json'
DATA_DIR = Path('data')
ESCO_DIR = DATA_DIR / 'esco'
ONET_DIR = DATA_DIR / 'onet'

REL_SKILLS = DATA_DIR / ('cleaned_related_skills' + EXT)
REL_JOBS = DATA_DIR / ('cleaned_related_jobs' + EXT)

CORPUS_FILE = Path('/ML/corpora/skillsjobs.txt')


def strip_ws(str):
  return REG_3.sub(' ', REG_2.sub(' ', REG_1.sub(' ', str)))


""" Returns an array of entries in this format:
  [entry, related_1, ..related_n]
"""
def add_related_entries():
  related_arr = []
  for file in [REL_JOBS, REL_SKILLS]:
    with open(file) as f:
      data = json.load(f)
      entries = data["entries"]
      print(f'Adding {len(entries)} `{data["filename"]}` to corpus..')
      for entry in entries:
        related_arr.append(' '.join([val for key, val in entry.items() if val is not None]))
  return related_arr


""" Returns one array of format:
  [conceptType, preferredLabels, altLabels, hiddenlabels, description, broaderConceptPT]
"""
def extract_esco_item(item):
  item_arr = []
  item_arr.append(item['conceptType'])
  item_arr.append(item['preferredLabel'])
  item_arr.append(strip_ws(item['description']))
  item_arr.append(' '.join([l.strip() for l in item['altLabels'] if l is not None ]))
  item_arr.append(' '.join([l.strip() for l in item['hiddenLabels'] if l is not None]))
  item_arr.append(' '.join([l.strip() for l in item['broaderConceptPT'] if l is not None]))
  return ' '.join(item_arr)
  # return item_arr


""" Returns an array of entries in this format:
  [conceptType, preferredLabels, altLabels, hiddenlabels, description, broaderConceptPT]
"""
def add_esco_entries():
  esco_arr = []
  for file in os.listdir(ESCO_DIR):
    with open(ESCO_DIR / file) as f:
      data = json.load(f)      
      print(f'Adding {len(data)} entries from {file} to corpus..')
      for item in data:
        esco_arr.append(extract_esco_item(item))
  return esco_arr


if __name__ == "__main__":
  corpus = []
  # corpus.extend(add_related_entries())
  # corpus.extend(add_esco_entries())
  with open(CORPUS_FILE, 'w') as f:
    f.write('\n'.join(corpus))
