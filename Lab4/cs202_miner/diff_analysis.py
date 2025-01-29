import sys
import csv
import os
from pydriller import Repository
from pydriller.metrics.process.code_churn import CodeChurn
from pydriller.metrics.process.commits_count import CommitsCount
from pydriller.metrics.process.hunks_count import HunksCount

columns = ['old_file_path', 'new_file_path', 'commit_sha', 'parent_sha', 'commit_message', 'diff_myers', 'diff_hist']

rows = []
count=0
last_n=10

commits = []
for x in Repository(sys.argv[1],only_no_merge=True,order='reverse').traverse_commits():
  if (x.in_main_branch==True):
    count=count+1
    commits.append(x)
    if count == last_n:
      break

in_order = []
for value in range(len(commits)):
  in_order.append(commits.pop())

commits=in_order
i=-1
for commit in commits:
  i+=1
  print('[{}/{}] Mining commit {}.{}'.format(i+1,len(commits),sys.argv[1],commit.hash))

  for m in commit.modified_files:
    old_file_path = m.old_path if m.old_path else '' 
    new_file_path = m.new_path if m.new_path else ''  
    commit_sha = commit.hash  
    parent_sha = commit.parents[0] if commit.parents else None  
    commit_message = commit.msg.strip() 

    diff_myers = m.diff_parsed['added'] if m.diff_parsed else None
    diff_hist = m.diff_parsed['deleted'] if m.diff_parsed else None

    rows.append([old_file_path, new_file_path, commit_sha, parent_sha, commit_message, diff_myers, diff_hist])

output_dir = os.path.join("results", sys.argv[1]) 
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Save the CSV in the results folder under the appropriate project subfolder
with open(os.path.join(output_dir, "diff_analysis.csv"), 'a', newline='', encoding='utf-8') as csvFile:
    writer = csv.writer(csvFile)
    writer.writerow(columns)
    writer.writerows(rows)