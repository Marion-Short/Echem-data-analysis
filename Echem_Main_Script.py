#!/usr/bin/env python
# coding: utf-8

import matplotlib.pyplot as plt
from CV_Analysis import CV_Analysis
from CPE_Analysis import CPE_Analysis

# CVs
CVpre = 'Echem_data\CYM19-CVpre.ids'
CVpost = 'Echem_data\CYM19-CVpost.ids'

# Import for plotting CVs and return figure and charges
CVpre_fig, CVpre_charges = CV_Analysis(CVpre, 'CVpre')
CVpost_fig, CVpost_charges = CV_Analysis(CVpost, 'CVpost')

#CPE
CPE = 'Echem_data\CYM19-CPE1.idf'
CPE_fig, CPE_charge = CPE_Analysis(CPE, 'CPE')

# list to store charges
charges = []
charges.extend(CVpre_charges)
charges.extend(CVpost_charges)
charges.append(CPE_charge)

pos_charges = [abs(num) for num in charges]
total_charge = sum(pos_charges)

code = 'MS311-2'
plt.figure(CVpre_fig)  # Select the first figure
plt.savefig(f'{code} CVpre')
plt.close()

plt.figure(CVpost_fig)  # Select the first figure
plt.savefig(f'{code} CVpost')
plt.close()

plt.figure(CPE_fig)  # Select the first figure
plt.savefig(f'{code} CPE')
plt.close()

# GC data
H2_area = 125552
CH4_area = 1818912

CH4_percent = 0.02
H2_RF = 0.101
headspace = 8 # mL
molarvol_mL_per_mol = 24478 #mL/mol

integral_ratio = H2_area / CH4_area
H2_percent = (integral_ratio * CH4_percent) / H2_RF
H2_mL = H2_percent * headspace
H2_mol = H2_mL / molarvol_mL_per_mol
H2_umol = H2_mol * 1000000

# Faradaic Efficiency
Z = 2 # number of electrons
F = 96485 # faradays constant

FE = (H2_mol * Z * F * 100) / total_charge