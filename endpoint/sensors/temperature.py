import subprocess
# run temp and adjust for farenhiet
temp = subprocess.call(["temperv14", "-c"])
far = (9.00 / 5.00) * temp + 32 - 6
print str(far)