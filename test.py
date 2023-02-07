import subprocess

with open("Data/5.txt", "r") as input_file:
    input_data = input_file.read()

process = subprocess.Popen(["python", "cp.py"], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
output_data, _ = process.communicate(input=input_data.encode())

print(output_data.decode())