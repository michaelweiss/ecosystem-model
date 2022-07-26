import sys
import re
import networkx as nx

# read commits from the commit log
# each commit is a dict with the keys: "hash", "developer", "changes"
def read_commits(filename):
    commits = []
    # precompile regexes
    developer_pattern = re.compile(r"^Author: (.+?) <(.*?)>")   # first group is developer, second is email
    change_pattern = re.compile(r"^(\d+)\s+(\d+)\s+(.+)")       # third group is file name
    
    line_no = 0
    with open(filename, 'r', encoding='utf8') as f:
         for line in f:
            line_no += 1
            # line starts with 'commit' read the commit hash
            if line.startswith('commit'):
                commit_hash = line.split()[1]
                commits.append({})
                commits[-1]['hash'] = commit_hash
            elif line.startswith('Author:'):
                try:
                    developer = re.match(developer_pattern, line).group(2)
                    commits[-1]['developer'] = developer if developer != '' else 'NA'
                except:
                    perror(line_no, line, "Does not match developer pattern")
            elif re.match(r"^(\d+)", line):
                try:
                    change = re.match(change_pattern, line).group(3)
                    if 'changes' not in commits [-1]:
                        commits[-1]['changes'] = []
                    commits[-1]['changes'].append(change)
                except:
                    perror(line_no, line, "Does not match change pattern")

    return commits

def perror(line_no, line, error):
    print("Error in line {}: {}\n{}".format(line_no, error, line), file=sys.stderr)

# extract the list of files each developer has changed
def contributions(commits):
    contributions = {}
    for commit in commits:
        if 'changes' in commit:
            for file in commit['changes']:
                developer = commit['developer']
                if not developer in contributions:
                    contributions[developer] = {}
                if not file in contributions[developer]:   
                    contributions[developer][file] = 0
                contributions[developer][file] += 1
    return contributions

def create_network(commits, min_changes=1):
    # create a networkx graph
    G = nx.Graph()

    # add nodes for developers
    developers = sorted(contribs.keys())   
    G.add_nodes_from(developers)

    # add edges for each pair of developers who have contributed to the same file
    # expects developers to be in sorted order, so we just need to enumerate all i, j (i < j) pairs
    for a in developers:
        for b in developers:
            if a < b:
                shared_files = set(contribs[a].keys()) & set(contribs[b].keys())
                # compute weight as shared number of file contributions
                # an alternative would be to compute the cosine similarity of the two vectors
                weight = sum(min(contribs[a][f], contribs[b][f]) for f in shared_files)
                if weight >= min_changes:
                    G.add_edge(a, b, weight=weight)
    return G

# get name of commit log file from command line arguments
if len(sys.argv) != 2:
    print("Usage: python3 contribs.py <filename>")
    sys.exit(1)   # exit with error code 1

# read commits from commit log file
commits = read_commits(sys.argv[1])

# extract the list of files each developer has changed
contribs = contributions(commits) 
# for developer in contribs:
#     print(developer, len(contribs[developer].keys()))

# create network and save to csv format
G = create_network(commits, min_changes=1)
print("from,to,weight")
for u, v, d in G.edges(data=True):
    print("{},{},{}".format(u, v, d['weight']))