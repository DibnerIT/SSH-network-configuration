import paramiko
import threading
import os.path
import subprocess
import time
import sys
import re
#######checking validity of all ip addresses
def validity_ip_check():
    global iplist
    iplist = []
    
    while True:
        flag1 = []
        try:
            
            ip_file = raw_input("Enter the file with list of IP addresses with extention: \n")
            
            f = open (ip_file,'r')
            f.seek(0)
            iplist = f.readlines()
            f.close()
            #print iplist
            
        except IOError:
            
            print "\nFile %s does not exists, please try again :) \n" %ip_file
            continue
        
#checking validity of the IP addresses
        
        for ip in iplist:
            a = ip.split('.')
            if (len(a)==4) and (1 <= int(a[0]) <= 223) and (int(a[0]) != 127) and (int(a[0]) != 169 or int(a[1]) != 254) and (0 <= int(a[0]) <= 255 and 0 <= int(a[1]) <= 255 and 0 <= int(a[2]) <= 255 and 0 <= int(a[3]) <= 255):
                flag1.append(True)
                continue
            else:
                flag1.append(False)
                break
            
        #print flag1
    
        if False in flag1:
            print "\nFile contains atleat one invalid IP address\n"
            continue
        else:
            print "\nAll IP addresss are valid\n"
            break
    
    ###########checking the conectivity to all addresss
    
    print "\n* Checking IP reachability. Please wait...\n"
    
    check2 = False
    
    while True:
        #print iplist
        for ip in iplist:
            exit_code = subprocess.call(['ping', '-c', '2', '-w', '2', '-q', '-n', ip])
            #print exit_code
            if exit_code  == 0:
                check2 = True
                continue
            
            elif exit_code == 2:
                print "\n* No response from device %s." % ip
                check2 = False
                break
            
            else:
                print "\n Ping to the following %s device has FAILED" % ip
                check2 = False
                break
            
        if check2 == False:
            print "\nPlease check the IP address file \n"
            validity_ip_check()
            
        elif check2 == True:
            print "\nAll devices are rechable.\n"
            break
        break    
   
    
       #validating authentication and commmand files
       
       
       
def validate_authentication_file():
    global user_file
    
    while True:
        user_file = raw_input("# Enter user/pass file name and extension: ")
        
        #Changing output messages
        if os.path.isfile(user_file) == True:
            print "\n* Username/password file has been validated. Waiting for command file...\n"
            break
        
        else:
            print "\n* File %s does not exist! Please check and try again!\n" % user_file
            continue
    
def validate_cmd_file():
    global cmd_file
    
    while True:
        cmd_file = raw_input("# Enter command file name and extension: ")
        
        #Changing output messages
        if os.path.isfile(cmd_file) == True:
            print "\nCommand file is being validated\n"
            break
        
        else:
            print "\n* File %s does not exist! Please check and try again!\n" % cmd_file
            continue
        
        
# open ssh connections
def ssh_conn(ip):
    try:
        #getting username and password
        f1 = open(user_file,'r')
        f1.seek(0)
        username = (f1.readlines()[0]).split(',')[0]
        f1.seek(0)
        password = ((f1.readlines()[0]).split(',')[1]).rstrip("\n")
        f1.close()
        
        # starting ssh connection 
        session = paramiko.SSHClient()
        #getting host keys for ssh server
        a = session.get_host_keys()
        a.clear()
        session.set_missing_host_key_policy(paramiko.RejectPolicy())
        permission = raw_input("\nAuthenticity does no exist for host %sDo you want to continue connecting?\n" %ip)
        while (permission != "yes") and (permission != "no"):
            permission = raw_input("\nplease type yes or no: \n")
        if (permission == "yes"):
            print "\n Host key for is added automatically in known_hosts for ip %s Executing commands Please wait!\n" %ip
            transport = paramiko.Transport(ip+":22")
            transport.connect()
            key=transport.get_remote_server_key()
            transport.close()
            a.add(hostname = ip, key = key , keytype = key.get_name())
            session.connect(ip, username = username, password = password)
            
        
            connection = session.invoke_shell()	
                
            #Open user selected file for reading
            selected_cmd_file = open(cmd_file, 'r')
                    
            #Starting from the beginning of the file
            selected_cmd_file.seek(0)
            
            for each_line in selected_cmd_file.readlines():
                    connection.send(each_line + '\n')
                    time.sleep(2)
                
            #Closing the user file
            f1.close()
                
            #Closing the command file
            selected_cmd_file.close()
                
            #Checking command output for IOS syntax errors
            router_output = connection.recv(65535)
            print router_output    
            if re.search(r"% Invalid input detected at", router_output):
                print "****There was at least one IOS syntax error on device %s" % ip
                    
            else:
                print "\nDONE for device %s" % ip
                    
            
            session.close()
        elif (permission == 'no'):
            print "\nHOST KEY VERIFICATION FAILED\n"
            
            
        
        
    except paramiko.AuthenticationException:
        print "\n* Invalid username or password. \n* Please check the username/password file or the device configuration!"
        print "\n* Closing program...\n"
    except  paramiko.SSHException:
        print "\n Exception raised to due SSH protocol negotiation or SSH disabled at server!"
        

if __name__ == '__main__':
    try:
        validity_ip_check()
        for ip in iplist:
            print ("\nGive file names for authenticating and configuring device %s" %ip)
            validate_authentication_file()
            validate_cmd_file()
            ssh_conn(ip)
    except KeyboardInterrupt:
        print "\n program aborted by user. Exiting.....\n"
        sys.exit()