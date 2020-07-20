import json
from pathlib import Path

EXT = '.json'
INPUT_DIR = Path('data/corrupt_jsons')
OUTPUT_DIR = Path('data')
SKILLS_CORRUPT = INPUT_DIR / ('related_skills' + EXT)
JOBS_CORRUPT = INPUT_DIR / ('related_jobs' + EXT)
SKILLS_JSON = OUTPUT_DIR / ('cleaned_related_skills' + EXT)
JOBS_JSON = OUTPUT_DIR / ('cleaned_related_jobs' + EXT)


def insert_semicolons(file):
  cnt = 0
  line_arr = [line.strip() for line in file]
  for idx, line in enumerate(line_arr):
    if line == '}{':
      line_arr[idx] = '},{'
      cnt += 1
  print(f'Found & corrected {cnt} corrupt JSON entries.')
  return '\n'.join(line_arr)


def correct_jsons():
  corrupt_skills = open(SKILLS_CORRUPT)
  skills = insert_semicolons(corrupt_skills)
  with open(SKILLS_JSON, 'w') as f:
    f.write(skills)
  corrupt_jobs = open(JOBS_CORRUPT)
  jobs = insert_semicolons(corrupt_jobs)
  with open(JOBS_JSON, 'w') as f:
    f.write(jobs)


def print_stats(file):
  with open(file) as f:
    min_len = float('inf')
    max_len = float('-inf')
    avg_len = 0
    data = json.load(f)
    entries = data["entries"]
    for idx, entry in enumerate(entries):
      min_len = len(entry) if len(entry) < min_len else min_len
      max_len = len(entry) if len(entry) > max_len else max_len
      avg_len = ( len(entry) + avg_len * (idx) ) / (idx + 1)
    print(f'Scanned {len(entries)} `{data["filename"]}` entries.')
    print(f'Minimum related entries length was {min_len}')
    print(f'Maximum related entries length was {max_len}')
    print(f'Average related entries length was {avg_len}')


if __name__ == "__main__":
  correct_jsons()
  for file in [SKILLS_JSON, JOBS_JSON]:
    print_stats(file)