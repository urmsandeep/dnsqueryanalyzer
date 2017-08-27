#!/usr/bin/python

#import modules
import dns.resolver
import time
import datetime

#filename
filename = "dnsquery.result"

#domain names
domains = [
           "cisco.com",
           "google.com", 
           "azure.microsoft.com"
           "gmail.com",
           "cnn.com",
           "google.in", 
           "aws.amazon.com", 
           "amazon.com", 
           "amazon.in",
           "flipkart.com",
           "bing.com",
           "philips.com",
           "microsoft.com",
           "null"]

class IPAddressEntry():
    "Stores resolved IP addresses for a given domain and a count"
    def __init__(self, ipaddr):
        self.ipaddr = ipaddr
        self.count = 1

    def update(self, ipadd):
        self.count += 1

class DomainEntry():
    "Stores Domain name and list of corresponding resolved IP addresses"
    #resolved_iplist = []
    def __init__(self, name):
        self.domain_name = name
        print "Debug:Setting domain to", name
        self.resolved_iplist = []

    def updateip(self, ipaddr):
       ipentry = next((x for x in self.resolved_iplist if x.ipaddr == ipaddr), None)
       if (ipentry != None):
           ipentry.update(ipaddr)
           print "DomainEntry_debug:[", self.domain_name, "]", ipentry.ipaddr, "already exists. update ref_count to", ipentry.count
       else:
           print "DomainEntry_debug:[", self.domain_name, "]",  ipaddr, "not found. Add it to resolved_iplist"
           ipentry = IPAddressEntry(ipaddr)
           self.resolved_iplist.append(ipentry);

       def getKey(custom):
           return custom.domain_name

from time import gmtime, strftime
#showtime = strftime("%Y-%m-%d %H:%M:%S", datetime.datetime.now().time())
showtime = datetime.datetime.now().time()
starttime = datetime.datetime.now().strftime ("%Y-%m-%d %H:%M:%S")
print "======== START TIME : ",  showtime, "========"

#print datetime.date.today()
print datetime.datetime.now().time()

mylist = []

#create a new instance of resolver
myResolver = dns.resolver.Resolver()

resolved_iplist = []
domain_list = []

print "IP Addresses ( count =",len(resolved_iplist),"):"
for ip in resolved_iplist:
    print ip 

print "================================"
count = 0
while True:
   x = 0
   while (domains[x] != "null"):
       #Lookup the 'A' records for a domain
       myAnswers = myResolver.query(domains[x], "A");
       print("qname=", myAnswers.qname)
       dentry = next((x for x in domain_list if x.domain_name == myAnswers.qname), None)
       if (dentry != None):
           print dentry.domain_name ," :already exists in domain_list"
       else:
           print myAnswers.qname, ":not found. Adding it into domain_list"
           dentry = DomainEntry(myAnswers.qname)
           domain_list.append(dentry)
   
       for rdata in myAnswers:
          print rdata 
          dentry.updateip(rdata)

       time.sleep(1)
       x = x+1

   #write to file
   fd = open(filename,"w")
   num_domains = len(domain_list)
   num_ipaddrs = 0;
   nowtime = datetime.datetime.now().strftime ("%Y-%m-%d %H:%M:%S")
   fd.write("==========    Start Time: %s ==========\n" % starttime)
   fd.write("==========  Current Time: %s ==========\n" % nowtime)
   fd.write("Domain names (count = %d)\n" % num_domains)
   for dn in domain_list:
     num_ipaddrs += len(dn.resolved_iplist)
     fd.write("\n==============================================\n");
     fd.write("%-20s (IP addresses=%d)\n" % (dn.domain_name, len(dn.resolved_iplist)))
     fd.write("==============================================\n");
     for ipentry in dn.resolved_iplist:
         #print "%15s"% ipentry.ipaddr, "      Recurrences:",  "%4d"% ipentry.count
         fd.write("%-15s       Recurrences:%4d\n" % (ipentry.ipaddr, ipentry.count))
   fd.write("\n==============================================\n");
   fd.write("Domains: %d        IP Addresses: %d\n" % (num_domains, num_ipaddrs))
   fd.write("==============================================\n");
   fd.close()
   count += 1

num_domains = len(domain_list)
num_ipaddrs = 0;
print "Domain names ( count =", num_domains,"):"
for dn in domain_list:
    num_ipaddrs += len(dn.resolved_iplist)
    print dn.domain_name, "(IP addresses = ", len(dn.resolved_iplist), "):"
    for ipentry in dn.resolved_iplist:
        print "%15s"% ipentry.ipaddr, "       Recurrences:",  "%4d"% ipentry.count
print "Number of Domains:", num_domains, "Number of IP Addresses:", num_ipaddrs

#write to file
fd = open(filename,"w")
num_domains = len(domain_list)
num_ipaddrs = 0;
nowtime = datetime.datetime.now().strftime ("%Y-%m-%d %H:%M:%S")
fd.write("==========    Start Time: %s ==========\n" % starttime)
fd.write("==========  Current Time: %s ==========\n" % nowtime)
fd.write("Domain names (count = %d)\n" % num_domains)
for dn in domain_list:
    num_ipaddrs += len(dn.resolved_iplist)
    fd.write("\n==============================================\n");
    fd.write("%-20s (IP addresses=%d)\n" % (dn.domain_name, len(dn.resolved_iplist)))
    fd.write("==============================================\n");
    for ipentry in dn.resolved_iplist:
        #print "%15s"% ipentry.ipaddr, "      Recurrences:",  "%4d"% ipentry.count
        fd.write("%-15s       Recurrences:%4d\n" % (ipentry.ipaddr, ipentry.count))
fd.write("\n==============================================\n");
fd.write("Domains: %d        IP Addresses: %d\n" % (num_domains, num_ipaddrs))
fd.write("==============================================\n");
fd.close()

