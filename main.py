#!/usr/bin/env python
# -*- coding: utf-8 -*-
# coding: utf8

import pingHost
import select
from paramiko import SSHClient
from paramiko import AutoAddPolicy

print('Version 0.0.7')

StatusDevice = 'Status host'
ConnectDevice = 'Connect to host'
Update = 'Update'
Updatefirmware = 'Update Firmware'
UpdateLoader = 'Update Loader'

ssh = SSHClient()
ssh.set_missing_host_key_policy(AutoAddPolicy())

for menu in range(999):
    print('1 ', StatusDevice, '\n' '2 ', ConnectDevice)
    Variant = str(input())
    if Variant == '1':
        print('Check availability of equipment')
        host = input("Enter ip address host:")
        print(pingHost.host(host))
        continue
    elif Variant == '2':
        try:
            # hosts array IP
            host = input("Введите адрес обррудования: ")
            # User
            user = input("Enter login: ")
            # Password
            password = input("Enter password: ")
            print('Connection')
            print("connecting.." + str(host) + "@" + str(user) + ":" + str(password))
            ssh.connect(str(host), username=str(user), password=str(password))
            print("connected..")
        except:
            print("Error connecting to host", host)
            continue

        for ConnectionMenu in range(999):
            print('1 ', 'Creat backup', '\n' '2 ', Update)
            VariantCM = str(input())
            if VariantCM == '1':
                print('Creat backup y/n')
                Variant = str(input())
                if Variant == 'y':
                    BackupName = input("Enter name file: ")
                    print('Format file backup', '\n' '1 ', '.backup', '\n' '2 ', '.rsc')
                    Variant = str(input())
                    if Variant == "1":
                        Backup = "system backup save name=/flash/" + BackupName + '.backup'
                        ssh.exec_command(Backup)
                        print("local backup created..")
                        break
                    elif Variant == '2':
                        BackupRsc = "export file=/flash/" + BackupName + '.rsc'
                        ssh.exec_command(BackupRsc)
                        ssh.close()
                        print("local backup created..")
                        break
                elif Variant == 'n':
                    print('Backup NO')
                    ssh.close()
                    continue
            if VariantCM == '2':
                print('1 ', Updatefirmware, '\n' '2 ', UpdateLoader )
                VariantUpdate = str(input())
                if VariantUpdate == '1':
                    command = 'sys package update check-for-updates'
                    stdin, stdout, stderr = ssh.exec_command(command)
                    while not stdout.channel.exit_status_ready():
                        if stdout.channel.recv_ready():
                            rl, wl, xl = select.select([stdout.channel], [], [], 0.0)
                            if len(rl) > 0:
                                tmp = stdout.channel.recv(1024)
                                output = tmp.decode()
                                print(output)

                    print('Update? y/n')
                    VariantUpdate = str(input())
                    if VariantUpdate == 'y':
                        command = 'sys package update download'
                        stdin, stdout, stderr = ssh.exec_command(command)
                        while not stdout.channel.exit_status_ready():
                            if stdout.channel.recv_ready():
                                rl, wl, xl = select.select([stdout.channel], [], [], 0.0)
                                if len(rl) > 0:
                                    tmp = stdout.channel.recv(1024)
                                    output = tmp.decode()
                                    print(output)

                    print('Downloaded, please reboot router to upgrade it. Reboot? y/n')
                    VariantReboot = str(input())
                    if VariantReboot == 'y':
                        command = 'sys reboot'
                        ssh.exec_command(command)
                        break
                    elif VariantReboot == 'n':
                        print('Reboot later')
                        break
                elif VariantUpdate == '2':
                    print(UpdateLoader)
                    break