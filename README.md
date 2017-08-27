# dnsqueryanalyzer
The objective is to trigger DNS queries to certain domains and analyze responses. 
At the moment the code runs on a loop sending DNS A-record queries to specified domians and parses rdata in responses. 
It eventually writes the results into dnsqueires.results created in the default run directory.
The frequency of queries is set to 1-min
