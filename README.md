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
python3 contribs.py che-server/changes.log
```

## Understand networks

## Present networks