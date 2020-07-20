from pathlib import Path

EXT = '.json'
INPUT_DIR = Path('data/corrupt_jsons')
OUTPUT_DIR = Path('data')
SKILLS_IN = INPUT_DIR / ('cleaned_related_skills' + EXT)
JOBS_IN = INPUT_DIR / ('cleaned_related_jobs' + EXT)
SKILLS_OUT = OUTPUT_DIR / ('cleaned_related_skills' + EXT)
JOBS_OUT = OUTPUT_DIR / ('cleaned_related_jobs' + EXT)


def insert_semicolons(file):
  cnt = 0
  line_arr = [line.strip() for line in file]
  for idx, line in enumerate(line_arr):
    if line == '}{':
      line_arr[idx] = '},{'
      cnt += 1
  print(f'Found & corrected {cnt} corrupt JSON entries.')
  return '\n'.join(line_arr)


if __name__ == "__main__":
  corrupt_skills = open(SKILLS_IN)
  skills = insert_semicolons(corrupt_skills)
  with open(SKILLS_OUT, 'w') as f:
    f.write(skills)
  corrupt_jobs = open(JOBS_IN)
  jobs = insert_semicolons(corrupt_jobs)
  with open(JOBS_OUT, 'w') as f:
    f.write(jobs)
  