import subprocess
cmd = "fdisk -l|grep Disk|grep sd|awk -F ':' '{print$1}'|awk '{print $2}'"
disk = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
disk = disk.stdout.read().decode().split()
print disk
for i in disk:
   cmd = "smartctl -i %s |grep Vendor|awk '{print $2}'"  %i
   model = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
   model = model.stdout.read().decode().replace('\n','')
   print model
   cmd = "smartctl -i %s|grep Serial|awk '{print $3}'" %i
   sn = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True) 
   sn = sn.stdout.read().decode().replace('\n','')
   print sn
   
   cmd = "sudo fdisk -l %s | grep Disk|head -1" %i
   size_data = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
   size_data = size_data.stdout.read().decode()
   size = size_data.split(":")[1].strip().split(" ")[0]  
   print size
