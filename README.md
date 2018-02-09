Providing IPs 
Program takes IPs as input text files.
Then it pngs to each ip testing for the rechability.
Then program takes authentication file and command files.
Authentication files has SSH Username and password.
Commands file consist of commands to be run on cisco IOS.
Paramiko implementation of SSH is used to SSH each IP in IP list.
RejectPolicy policy in configured which alearts user in following way:

Authenticity does no exist for host A Do you want to continue connecting?
yes
Host key for is added automatically in known_hosts for ip A Executing commands Please wait!
Authenticity does no exist for host B Do you want to continue connecting?
no
HOST KEY VERIFICATION FAILED

Each Router takes different authentication and command files.
