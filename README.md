# ecosystem-model
Code to model software ecosystems as networks

## Capture data
Suppose you want to map the Eclipse Che Server ecosystem:
```
https://github.com/eclipse-che/che-server
```
First, you need get the commit log for the project.

Clone the repo (this will take a while):
```
git clone https://github.com/eclipse-che/che-server.git
```

Before you can extract commits, you need to run this once:
```
git config diff.renameLimit 999999
```

Extract commits:
```
cd che-server/
git log --date=raw --numstat >changes.log
```

Now run ```contribs.py``` to extract developer collaborations:
```
python3 contribs.py che-server/changes.log >che-server.csv
```

## Understand networks

Computing network metrics can help you identify key players and their roles.

## Present networks

Configure the ecosystem visualization by changing the ```ecosystem.py``` file. Things that you may consider changing:

* File with the developer collaborations
* Color scheme to highlight specific nodes in the network
* Add code to compute summary statistics of the ecosystem
* Add code to compute network metrics
* Advanced: Add code for community detection to group the nodes
* Advanced: Use cosine similarity instead of commit sum similarity for inferring relationships

Run the ecosystem visualizer:
```
streamlit run ecosystem.py
```

## Dependencies

Required libraries:

* networkx
* pandas
* numpy
* pyvis
* streamlit

You can install each of these by using a version of this command:
```
python3 -m pip install networkx
```