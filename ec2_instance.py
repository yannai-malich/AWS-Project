#!/bin/python3
from contextlib import nullcontext
import sys, os, boto3, time
from botocore.exceptions import ClientError
clear = lambda: os.system('clear')
global ec2_client, ec3_resource, id_list 
id_list = []
ec2_client = boto3.client('ec2')
ec2_resource = boto3.resource('ec2')
#exit fun
def fin():
    clear()
    temp = input('1. Exit y/n.\n')
    if temp == "n":
        main()
    elif temp == 'y':
        clear()
        print("Good bey!")
        time.sleep(2)
        clear()
        exit
    else:
        print('y or n only!')
        time.sleep(2)
        fin()
#install awscki & boto3
def installing():
    clear()
    if boto3.__version__ == "":
        print('boto3 need is not installed')
    else:
        print(boto3.__version__)
    os.system('bash i_aws.sh')
    main()
#Funcion that swohing all EC2 instances by state.
def ec2_display(status):
    if status == "":
        temp = input('1. Running.\n2. Stopping.\n9. Main menu.\n0. Exit.\n')
        clear()
        if temp == "1":
            status = 'running'
        elif temp == "2":
            status = 'stopped'
        elif temp == "9":
            main()
        elif temp == "0":
            fin()
        else:
            print("1-2 or 0 only!")
            time.sleep(2)
            ec2_display
    instances = ec2_resource.instances.filter(Filters=[{'Name': 'instance-state-name', 'Values': [status]}])
    id_list.clear()
    i = 1
    for instance in instances:
        print('Instance number ' + str(i) + ': Id: {0}. Type: {1}.\n'.format(instance.id, instance.instance_type))
        id_list.append(instance.id)
        i += 1
#Funcion that swohing all EC2 instances.
def ec2_display_all(): 
    clear()
    id_list.clear()
    i = 1
    for instance in ec2_resource.instances.all():
        print('Instance number ' +str(i) + ': Id: {0}. Type: {1}. AMI: {2}. State: {3}.\n'.format(instance.id, instance.instance_type, instance.image.id, instance.state))
        id_list.append(instance.id)
        i += 1
#running ec2 instacne
def start():
    ec2_display("stopped")
    t1 = int(input('Select instane to start:\n')) - 1
    clear()
    instance_id = id_list[t1]
    print("start  " + instance_id + '\n')
    time.sleep(2)
    ec2_resource.instances.filter(InstanceIds=[instance_id]).start()
    manage()
#stoping ec2 instacne
def stop():
    ec2_display("running")
    t2 = int(input('Select instane to stop:\n')) - 1
    clear()
    instance_id = id_list[t2]
    print("stoping " + instance_id + '\n')
    time.sleep(2)
    ec2_resource.instances.filter(InstanceIds=[instance_id]).stop()
    manage()
# creating ec2 instances
def create():
    instances = ec2_resource.create_instances(
        ImageId='ami-03a0c45ebc70f98ea',
        MinCount=1,
        MaxCount=int(input('How many instances you want to create?\n')),
        InstanceType='t2.micro',
        KeyName='yannai_1',
        SecurityGroupIds=['sg-0e8c6e694c1046b4e']
    )
    manage()
#terminate fun
def terminate_fun():
    clear()
    ec2_display_all()
    t3 = int(input('Selecte instance to terminate.\n')) - 1
    instance_id = id_list[t3]
    ec2_resource.instances.filter(InstanceIds=[instance_id]).terminate()
    manage()
#managing menu
def manage():
    clear()
    temp = input('Manage menu:\n1. Create EC2 instance.\n2. Terminate EC2 instance.\n3. Start EC2 instance.\n4. Stop EC2 instance.\n9. Main menu.\n0. Exit.\n')
    clear()
    if temp == "1":
        create()
    elif temp == "2":
        terminate_fun()
    elif temp == "3":
        start()
    elif temp == "4":
        stop()
    elif temp == "9":
        main()
    elif temp == "0":
        fin()
    else:
        print("1-5 or 0 only!")
        time.sleep(2)
        manage()
#monitor menu
def monitor():
    clear()
    temp = input('Monitor menu:\n1. Display all EC2 instances.\n2. Display EC2 instances by state.\n3. Describe EC2 instance.\n9. Main menu.\n0. Exit.\n')
    clear()
    if temp == "1":
        ec2_display_all()
        temp = input('Prass any key to continue\n')
        monitor()
    elif temp == "2":
        ec2_display("")
        temp = input('Prass any key to continue\n')
        monitor()
    elif temp == "9":
        main()
    elif temp == "0":
        fin()
    else:
        print("1-2 or 0 only!")
        time.sleep(2)
        monitor()
#main menu
def main():
    clear()
    temp = input('Main menu:\n1. Manageing.\n2. Monitoring.\n3. Installing.\n0. Exit.\n')  
    clear()
    if temp == "1":
        manage()
    elif temp == "2":
        monitor()
    elif temp == "3":
        installing()
    elif temp == "0":
        print("Good bey!")
        time.sleep(2)
        clear()
        exit
    else:
        print("1-5 or 0 only!")
        time.sleep(2)
        main() 
main()