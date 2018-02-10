# Working:

Providing IPs 
Program takes IPs as input text files.
Then it pings to each ip testing for the rechability.
Then program takes authentication file and command files.
Authentication files has SSH Username and password.
Commands file consist of commands to be run on cisco IOS.
Paramiko implementation of SSH is used to SSH each IP in IP list.
Program also implements paramiko implementation of StrickHostKeyChecking feature of linux by configuration of RejectPolicy policy which alearts user in following way:

Authenticity does no exist for host A Do you want to continue connecting?

yes

Host key for is added automatically in known_hosts for ip A Executing commands Please wait!

Authenticity does no exist for host B Do you want to continue connecting?

no

HOST KEY VERIFICATION FAILED

Each Router takes different authentication and command files.

# Sample configutation

![sample](https://user-images.githubusercontent.com/31825161/36058371-2529407e-0dec-11e8-8b96-851d9efe9880.jpg)

# Example: 

root@debian:~# python ssh1.py

Enter the file with list of IP addresses with extention: 

ipaddress

All IP addresss are valid


* Checking IP reachability. Please wait...

PING 10.1.1.1

 (10.1.1.1) 56(84) bytes of data.

--- 10.1.1.1

 ping statistics ---
 
2 packets transmitted, 2 received, 0% packet loss, time 1001ms

rtt min/avg/max/mdev = 9.807/11.968/14.130/2.164 ms

All devices are rechable.


Give file names for authenticating and configuring device 10.1.1.1

Enter user/pass file name and extension: authentication

* Username/password file has been validated. Waiting for command file...

Enter command file name and extension: command

Command file is being validated


Authenticity does no exist for host 10.1.1.1

Do you want to continue connecting?

yes

 Host key for is added automatically in known_hosts for ip 10.1.1.1
 
 Executing commands Please wait!
 
DONE for device 10.1.1.1


