#!/bin/bash -e
# 运行这个脚本给出图片显示MD的温度、能量、压强、体积的收敛情况，数据保存于MDConv.txt

filename1="OUTCAR"
filename2="OSZICAR"
tempfile1="temp1.txt"
tempfile2="temp2.txt"
output_file="MDConv.txt"

grep "F=" $filename2 | awk '{print $1, "\t", $3, "\t", $9}' > $output_file
grep "total pressure" $filename1 | awk '{print $4}' > $tempfile1
grep "volume of cell" $filename1 | awk '{print $5}' > $tempfile2
paste $output_file $tempfile1 $tempfile2 > temp_final.txt
mv temp_final.txt $output_file
rm $tempfile1 $tempfile2

# Insert header to the first line
echo -e "No.MD\tTemperature\tE0\tPressure\tVolume\n$(cat $output_file)" > $output_file

# call python code within bash
python3 << EOF
import matplotlib.pyplot as plt
import pandas as pd

# Read the data from the file
data = pd.read_csv("$output_file", delimiter="\t")

fig, axs = plt.subplots(2, 2)

# Create four scatter plots
axs[0, 0].scatter(data["No.MD"], data["Temperature"])
axs[0, 0].set_title('Temperature')
axs[0, 1].scatter(data["No.MD"], data["E0"])
axs[0, 1].set_title('E0')
axs[1, 0].scatter(data["No.MD"], data["Pressure"])
axs[1, 0].set_title('Pressure')
axs[1, 1].scatter(data["No.MD"], data["Volume"])
axs[1, 1].set_title('Volume')

# A common title for all subplots
fig.suptitle('MD Convergence Situation')

plt.tight_layout()

# Save the combined plot 
plt.savefig("MDConv.png")
EOF

