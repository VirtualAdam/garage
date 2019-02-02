import subprocess

outlet1_on = 1332531
outlet1_off = 1332540
outlet2_on = 1332675
outlet2_off = 1332684
outlet3_on = 1332995
outlet3_off = 1333004
outlet4_on = 1334531
outlet4_off = 1334540
outlet5_on = 1340675
outlet5_off = 1340684

data = subprocess.Popen(["/var/www/rfoutlet/codesend", "1332531", "-p", "3"], stdout=subprocess.PIPE).communicate()[0]
#data = subprocess.Popen(["/var/www/rfoutlet/codesend", "1332540", "-p", "3"], stdout=subprocess.PIPE).communicate()[0]
print "done"
