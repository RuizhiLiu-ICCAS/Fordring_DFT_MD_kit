# Fordring_DFT_MD_kit
Some programes for automation VASP calculation or data analysis.  
下载解压后放置在对应文件夹中即可使用  
使用前请阅读使用许可-程序包用户协议  

# AIMDkit.py
Created by Rui-Zhi Liu_ICCAS  
Version 1.0-2025.2.21  

此程序和 OSZICAR; XDATCAR; XDATCAR_toolkit.py 需要在同一文件夹  
目前此程序仅具有统计分子动力学模拟能量收敛及批处理不同帧数RDF的功能  

需要以下python库:  
import argparse  
import os  
import numpy as np  
import subprocess  
import MDAnalysis  
import MDAnalysis.analysis.rdf  
import shutil  
import matplotlib as mpl  
import math  

#XDATCAR_toolkit.py:  
#Convert XDATCAR to PDB and extract energy & temperature profile for AIMD simulations   
#by nxu tamas@zju.edu.cn  
#version 1.2  
#date 2019.4.9  
#此文件需从nxu tamas@zju.edu.cn处获取  

usage: AIMDkit.py [-h] [-Energycal] [-RDF] [-atom1 ATOM1] [-atom2 ATOM2] [-step STEP]
                  [-end_frame END_FRAME]  

This script provides different methods for molecular dynamics simulations analysis.  

options:  
  -h, --help            show this help message and exit  
  -Energycal            Run energy calculation. Extracts energy data from OSZICAR file and writes the results into totalE.txt.  
                        python AIMDkit.py -Energycal  
                        -----------------------  
  -RDF                  Run RDF calculation.  
                        For the RDF calculation you have to define additional parameters (see below):  
                        python AIMDkit.py -RDF -atom1 Al -atom2 S -step 100 -end_frame 5000  
                        -----------------------  
  -atom1 ATOM1          Type of atom 1 for RDF calculation. For example: -atom1 Al  
  -atom2 ATOM2          Type of atom 2 for RDF calculation. For example: -atom2 S  
  -step STEP            Step for RDF calculation. Defines the step size for frames in the simulation. For example: -step 100  
  -end_frame END_FRAME  End frame for RDF calculation. Defines the last frame for RDF calculation. For example: -end_frame 5000  

# RDFtxt2origin.py
RDF txt convert to Origin  
Created by LRZ  
version 1.0 2025.2.21  

此程序需放置于RDF文件夹下，通常用于AIMDkit.py生成多帧数RDF后  

需要以下python库：  
import os  
import pandas as pd  
import glob  

# catpotcar.sh
可以按照POSCAR中元素顺序自动抓取POTCAR数据至POTCAR文件中  

Created by Rui-Zhi Liu_ICCAS  
Version 1.0-2025.7.19  

此程序需放置于POSCAR同一文件夹下，并需要手动修改POTCAR数据库的路径  

# mergeXDAT.sh
可以将两个分子动力学生成的XDATCAR合并为一个  

此程序需将两个XDATCAR放置于同一文件夹  
