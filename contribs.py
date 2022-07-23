import sys
import re
import networkx as nx

def read_commits(filename):
    commits = []
    commit_hash = ""
    author = ""
    authors = []
    with open(filename, 'r') as f:
        for line in f:
            # line starts with 'commit' read the commit hash
            if line.startswith('commit'):
                commit_hash = line.split()[1]
                commits.append(commit_hash)
            elif line.startswith('Author:'):
                pattern = r"Author: (.+?) <(.+)>"   # first group is author, second is email
                author = re.search(pattern, line).group(2)
                authors.append(author)

    return commits, authors

# get name of commit log file from command line arguments
if len(sys.argv) != 2:
    print("Usage: python3 contribs.py <filename>")
    sys.exit(1)   # exit with error code 1

# read commits from commit log file
commits, authors = read_commits(sys.argv[1])
print(authors[:5])

