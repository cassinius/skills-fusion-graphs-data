import re
import os
import json
import pandas
from pathlib import Path

REG_1 = re.compile(r"[\r\n\t\W0-9()-]")
REG_2 = re.compile(r"\s+.\s+")
REG_3 = re.compile(r"\s{2,}")

DATA_DIR = Path('data')
ESCO_DIR = DATA_DIR / 'esco'
ONET_DIR = DATA_DIR / 'onet'
REL_DIR = DATA_DIR / 'related'

CORPUS_DIR = Path('/ML/corpora')
ESCO_CORPUS = CORPUS_DIR / 'esco.txt'
ONET_CORPUS = CORPUS_DIR / 'onet.txt'
RELATED_CORPUS = CORPUS_DIR / 'related.txt'
INTEGRATED_CORPUS = CORPUS_DIR / 'integrated.txt'


def beautify(str):
  return REG_3.sub(' ', REG_2.sub(' ', REG_1.sub(' ', str)))


""" Returns an array of entries in this format:
  [entry, related_1, ..related_n]
"""
def collect_related_entries():
  related_arr = []
  for file in os.listdir(REL_DIR):
    with open(REL_DIR / file) as f:
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
  # item_arr.append(item['conceptType'])
  item_arr.append(item['preferredLabel'])
  item_arr.append(beautify(item['description']))
  item_arr.append(' '.join([l.strip() for l in item['altLabels'] if l is not None ]))
  item_arr.append(' '.join([l.strip() for l in item['hiddenLabels'] if l is not None]))
  item_arr.append(' '.join([l.strip() for l in item['broaderConceptPT'] if l is not None]))
  return ' '.join(item_arr)


""" Returns an array of entries in this format:
  [conceptType, preferredLabels, altLabels, hiddenlabels, description, broaderConceptPT]
"""
def collect_esco_entries():
  esco_arr = []
  for file in os.listdir(ESCO_DIR):
    with open(ESCO_DIR / file) as f:
      data = json.load(f)      
      print(f'Adding {len(data)} entries from {file} to corpus..')
      for item in data:
        esco_arr.append(extract_esco_item(item))
  return esco_arr


""" Returns the whole Onet corpus
  TODO This will be a diversified & heterogeneous function collection ;-)
  # print(df.keys())
"""
def collect_onet_entries():
  onet_arr = []
  
  df = pandas.read_csv(ONET_DIR / 'Abilities.txt', sep="\t", header=0)
  onet_arr.append(' '.join(df['Element Name'].unique()))
  
  df = pandas.read_csv(ONET_DIR / 'Content Model Reference.txt', sep="\t", header=0)
  for idx in df.index:
    onet_arr.append(df.iloc[idx]['Element Name'] + ' ' + df.iloc[idx]['Description'])
  
  df = pandas.read_csv(ONET_DIR / 'DWA Reference.txt', sep="\t", header=0)
  onet_arr.append('\n'.join(df['DWA Title'].unique()))

  df = pandas.read_csv(ONET_DIR / 'Emerging Tasks.txt', sep="\t", header=0)
  onet_arr.append('\n'.join(df['Task'].unique()))

  df = pandas.read_csv(ONET_DIR / 'IWA Reference.txt', sep="\t", header=0)
  onet_arr.append('\n'.join(df['IWA Title'].unique()))

  df = pandas.read_csv(ONET_DIR / 'Occupation Data.txt', sep="\t", header=0)
  for idx in df.index:
    onet_arr.append(df.iloc[idx]['Title'] + ' ' + df.iloc[idx]['Description'])
  
  df = pandas.read_csv(ONET_DIR / 'Sample of Reported Titles.txt', sep="\t", header=0)
  onet_arr.append(' '.join(df['Reported Job Title'].unique()))

  df = pandas.read_csv(ONET_DIR / 'Skills.txt', sep="\t", header=0)
  onet_arr.append(' '.join(df['Element Name'].unique()))

  df = pandas.read_csv(ONET_DIR / 'Task Statements.txt', sep="\t", header=0)
  onet_arr.append('\n'.join(df['Task'].unique()))

  df = pandas.read_csv(ONET_DIR / 'Technology Skills.txt', sep="\t", header=0)
  # This is e**ing slow for larger files...
  for idx in df.index:
    onet_arr.append(df.iloc[idx]['Example'] + ' ' + df.iloc[idx]['Commodity Title'])
  
  df = pandas.read_csv(ONET_DIR / 'Tools Used.txt', sep="\t", header=0)
  # This is e**ing slow for larger files...
  for idx in df.index:
    onet_arr.append(df.iloc[idx]['Example'] + ' ' + df.iloc[idx]['Commodity Title'])
  
  df = pandas.read_csv(ONET_DIR / 'UNSPSC Reference.txt', sep="\t", header=0)
  # This is e**ing slow for larger files...
  for idx in df.index:
    onet_arr.append(df.iloc[idx]['Commodity Title'] + ' ' + df.iloc[idx]['Class Title'] + ' ' + df.iloc[idx]['Family Title'])
  
  df = pandas.read_csv(ONET_DIR / 'Work Activities.txt', sep="\t", header=0)
  onet_arr.append(' '.join(df['Element Name'].unique()))

  return onet_arr
  

if __name__ == "__main__":
  print('Collecting ESCO entries..')
  esco_corpus = collect_esco_entries()
  print('Writing ESCO corpus..')
  with open(ESCO_CORPUS, 'w') as f:
    f.write(re.sub("[\.',]", '', '\n'.join(esco_corpus)))

  print('Collecting ONET entries..')
  onet_corpus = collect_onet_entries()
  print('Writing ONET corpus..')
  with open(ONET_CORPUS, 'w') as f:
    f.write(re.sub("[\.',]", '', '\n'.join(onet_corpus)))
  
  print('Collecting RELATED entries..')
  related_corpus = collect_related_entries()
  print('Writing RELATED corpus...')
  with open(RELATED_CORPUS, 'w') as f:
    f.write(re.sub("[\.',]", '', '\n'.join(related_corpus)))

  integrated_corpus = []
  integrated_corpus.extend(esco_corpus)
  integrated_corpus.extend(onet_corpus)
  integrated_corpus.extend(related_corpus)
  print('Writing INTEGRATED corpus..')
  with open(INTEGRATED_CORPUS, 'w') as f:
    f.write(re.sub("[\.',]", '', '\n'.join(integrated_corpus)))
