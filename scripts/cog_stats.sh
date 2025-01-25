cat kine.csv | awk -F, '{print $6}' | grep -v '^$'| datamash mean 1 median 1 min 1 max 1
