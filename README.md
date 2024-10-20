# Top AI Conference collections

This repository collects the list of accepted paper from top AI conferences. All lists are crawled by python scripts for later maintenance and analysis. Welcome to contribute.

## Conference collections

Including IJCAI, ECCV, ACCV, NIPS, ACMMM, WACV, ICML, CVPR, AAAI, ICCV, ACL, BMVC. All conferences have been updated by **October 20, 2024**.


## Download pdf files

You can run the following script to download papers from all supported conferences:

```
pip install -r requirements.txt
cd scripts/crawl
bash scripts/bash.sh
```

or execute each python file to crawl and download papers for each conference:

```
cd scripts/crawl
python nips.py
```

## Build wordclouds

You can run the following script to build wordclouds:
> Please remember to specify the confernce path variable.
```
bash

# transform markdown to csv
python md2csv.py
python cloud.py
```


## Find related work

A simple script are provided under `focus/` folder, which can use multiple regular experssions to filter papers you may be interested:

```
cd focus
# edit match_lis
python filter.py
# a xlsx file will be generated.
```

## Reference

This repository is heavily borrowed from:
- https://github.com/sailist/Awesome-Paper-List-py/tree/master

## Other Tools

- [Conference-Acceptance-Rates](https://github.com/lixin4ever/Conference-Acceptance-Rate)
- [ccfddl - Conference-Deadlines](https://ccfddl.github.io/)
