import time
import sys
import re
import paramiko
import threading
import os.path
import subprocess


#Checking IP address file and content validity
def ip_is_valid():
    check = False
    global ip_list
    
    while True:
        #Prompting user for input
        print "\n# # # # # # # # # # # # # # # # # # # # # # # # # # # #\n"
        ip_file = raw_input("# Enter IP file name and extension: ")
        print "\n# # # # # # # # # # # # # # # # # # # # # # # # # # # #"
        
        #Changing exception message
        try:
            #Open user selected file for reading (IP addresses file)
            selected_ip_file = open(ip_file, 'r')
            
            #Starting from the beginning of the file
            selected_ip_file.seek(0)
            
            #Reading each line (IP address) in the file
            ip_list = selected_ip_file.readlines()
            print ip_list
            #Closing the file
            selected_ip_file.close()
            
        except IOError:
            print "\n* File %s does not exist! Please check and try again!\n" % ip_file
            
        #Checking octets            
        for ip in ip_list:
            a = ip.split('.')
            print a
            
            if (len(a) == 4) and (1 <= int(a[0]) <= 223) and (int(a[0]) != 127) and (int(a[0]) != 169 or int(a[1]) != 254) and (0 <= int(a[1]) <= 255 and 0 <= int(a[2]) <= 255 and 0 <= int(a[3]) <= 255):
                check = True
                break
                 
            else:
                print '\n* There was an INVALID IP address! Please check and try again!\n'
                check = False
                continue
            
        #Evaluating the 'check' flag    
        if check == False:
            continue
        
        elif check == True:
            break

    ############# Application #2 - Part #2 #############
    
    #Checking IP reachability
    print "\n* Checking IP reachability. Please wait...\n"
    
    check2 = False
    
    while True:
        for ip in ip_list:
            ping_reply = subprocess.call(['ping', '-c', '2', '-w', '2', '-q', '-n', ip])
            
            if ping_reply == 0:
                check2 = True
                continue
            
            elif ping_reply == 2:
                print "\n* No response from device %s." % ip
                check2 = False
                break
            
            else:
                print "\n* Ping to the following device has FAILED:", ip
                check2 = False
                break
            
        #Evaluating the 'check' flag 
        if check2 == False:
            print "* Please re-check IP address list or device.\n"
            ip_is_valid()
        
        elif check2 == True:
            print '\n* All devices are reachable. Waiting for username/password file...\n'
            break
ip_is_valid()