import json
from pathlib import Path

EXT = '.json'
DATA_DIR = Path('data')
ONET_DIR = Path('data/onet')

REL_SKILLS = DATA_DIR / ('cleaned_related_skills' + EXT)
REL_JOBS = DATA_DIR / ('cleaned_related_jobs' + EXT)

CORPUS_FILE = Path('/ML/corpora/skillsjobs.txt')


'''
  Returns a string consisting of lines in this format:
  entry related_1 .. related_n
'''
def add_related_entries():
  related_arr = []
  for file in [REL_JOBS, REL_SKILLS]:
    with open(file) as f:
      data = json.load(f)
      entries = data["entries"]
      print(f'Adding {len(entries)} {data["filename"]} to corpus..')
      for entry in entries:
        related_arr.append(' '.join([val for key, val in entry.items() if val is not None]))
  return related_arr


if __name__ == "__main__":
  corpus = []
  corpus.extend(add_related_entries())
  with open(CORPUS_FILE, 'w') as f:
    f.write('\n'.join(corpus))
