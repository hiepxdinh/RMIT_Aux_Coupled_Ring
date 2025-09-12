# -*- coding: utf-8 -*-
"""
Created on Wed Sep  6 23:08:47 2023

@author: S3923133
"""

##########################################################
import numpy as np
import matplotlib.pyplot as plt
# import matplotlib.colors as colors
# from pyplot.get_cmap('afmhot_u')
############ li2023direct - 03 ###########################

# Number of sample points
N = 5000000
# sample spacing
T = 1.0 / 800.0

delta_Omega_03 = np.linspace(-6, 6, 201)
kOmega_03 = np.linspace(0, N*T, N, endpoint=False)

# kOmega_03 = np.linspace(0, 4*np.pi, 201)

g1_03 = 1
g2_03 = 2


phi1_03 = 0*np.pi/180
phi2_03 = 0*np.pi/180


#
G = (g1_03*np.exp(-1j*phi1_03)) + (g2_03*np.exp(1j*(kOmega_03) + 1j*(phi2_03)))

phase = np.angle(G)

#%% Dispersion curve

epsilon_m_plus_03 = np.sqrt(g1_03**2 + g2_03**2 + 2*g1_03*g2_03*np.cos(kOmega_03 + phi1_03 + phi2_03))
epsilon_m_minus_03 = - np.sqrt(g1_03**2 + g2_03**2 + 2*g1_03*g2_03*np.cos(kOmega_03 + phi1_03 + phi2_03))

plt.plot(kOmega_03, epsilon_m_plus_03)
plt.plot(kOmega_03, epsilon_m_minus_03)
plt.ylim(-6, 6)
plt.show()

### Band structure

kappa_03 = (4/20)/2
print('kappa: {}'.format(kappa_03))

delta_Omega_03_plus = delta_Omega_03 - kappa_03
delta_Omega_03_minus = delta_Omega_03 + kappa_03

gamma_loss_03 = 0.25
gammaA = 0.2

PhiD_plus_03 = 1 / np.sqrt(2)
PhiC_plus_03 = np.exp(-1j*phase) / np.sqrt(2)

PhiD_minus_03 = 1 / np.sqrt(2)
PhiC_minus_03 = -1*np.exp(-1j*phase) / np.sqrt(2)

PhiD_plus_03_conj = 1 / np.sqrt(2)
PhiC_plus_03_conj = np.conjugate(PhiD_plus_03)      #np.exp(1j*phase) / np.sqrt(2)

PhiD_minus_03_conj = 1 / np.sqrt(2)
PhiC_minus_03_conj = np.conjugate(PhiD_minus_03)    #- np.exp(1j*phase) / np.sqrt(2)

### Initialize band structure arrays

OutR_TB_03_kappa_plus_m_plus = np.zeros((len(delta_Omega_03_plus), len(kOmega_03)), complex)
OutR_TB_03_kappa_plus_m_minus = np.zeros((len(delta_Omega_03_plus), len(kOmega_03)), complex)
OutR_TB_03_kappa_plus = np.zeros((len(delta_Omega_03_plus), len(kOmega_03)), complex)

OutR_TB_03_kappa_minus_m_plus = np.zeros((len(delta_Omega_03_minus), len(kOmega_03)), complex)
OutR_TB_03_kappa_minus_m_minus = np.zeros((len(delta_Omega_03_minus), len(kOmega_03)), complex)
OutR_TB_03_kappa_minus = np.zeros((len(delta_Omega_03_minus), len(kOmega_03)), complex)

for i in range(len(delta_Omega_03)):
    OutR_TB_03_kappa_plus_m_plus[i]  = (-1j*gammaA / 2) * (PhiC_plus_03_conj * (PhiC_plus_03 + PhiD_plus_03 * np.exp(2j * kOmega_03 / 8)) / (delta_Omega_03_plus[i] - epsilon_m_plus_03 + 1j*gamma_loss_03))
    OutR_TB_03_kappa_plus_m_minus[i]  = (-1j*gammaA / 2) * (PhiC_minus_03_conj * (PhiC_minus_03 + PhiD_minus_03 * np.exp(2j * kOmega_03 / 8))/ (delta_Omega_03_plus[i] - epsilon_m_minus_03  + 1j*gamma_loss_03))

    OutR_TB_03_kappa_plus = (OutR_TB_03_kappa_plus_m_plus + OutR_TB_03_kappa_plus_m_minus)*np.conjugate(OutR_TB_03_kappa_plus_m_plus + OutR_TB_03_kappa_plus_m_minus)

    OutR_TB_03_kappa_minus_m_plus[i] = (-1j*gammaA / 2) * (PhiD_plus_03_conj * (PhiC_plus_03 * np.exp(-2j * kOmega_03 / 8) + PhiD_plus_03) / (delta_Omega_03_minus[i] - epsilon_m_plus_03 + 1j*gamma_loss_03) )
    OutR_TB_03_kappa_minus_m_minus[i] = (-1j * gammaA / 2) * (PhiD_minus_03_conj * (PhiC_minus_03 * np.exp(-2j * kOmega_03 / 8) + PhiD_minus_03) / (delta_Omega_03_minus[i] - epsilon_m_minus_03 + 1j * gamma_loss_03))

    OutR_TB_03_kappa_minus = (OutR_TB_03_kappa_minus_m_minus + OutR_TB_03_kappa_minus_m_plus)*np.conjugate(OutR_TB_03_kappa_minus_m_minus + OutR_TB_03_kappa_minus_m_plus)

    OutR_TB_03_kappa = (OutR_TB_03_kappa_minus + OutR_TB_03_kappa_plus )

plt.imshow(np.abs(OutR_TB_03_kappa), interpolation='nearest', origin='lower', aspect='auto')
# plt.colorbar()
# plt.pcolor(kOmega_03, delta_Omega_03, np.abs(TB_03_kappa), vmin = 0.15, vmax=0.65)
# plt.imshow(np.abs(TB_03_kappa), interpolation='nearest', origin='lower', aspect='auto', cmap='afmhot_r', vmin = 0, vmax=50)
# plt.ylim(90, 130)

plt.tick_params(
axis='both',          # changes apply to the x-axis
which='both',      # both major and minor ticks are affected
bottom=False,      # ticks along the bottom edge are off
top=False,         # ticks along the top edge are off
left=False,
right = False,
labelleft=False,
labelbottom=False) # labels along the bottom edge are off

# plt.savefig("5GHz.png", dpi=1000, bbox_inches='tight')
# v = np.linspace(0, 1.0, 2, endpoint=True)
# plt.colorbar()
plt.title("|Out_R|")
plt.show()

### Initialize band structure arrays

OutL_TB_03_kappa_plus_m_plus = np.zeros((len(delta_Omega_03_plus), len(kOmega_03)), complex)
OutL_TB_03_kappa_plus_m_minus = np.zeros((len(delta_Omega_03_plus), len(kOmega_03)), complex)
OutL_TB_03_kappa_plus = np.zeros((len(delta_Omega_03_plus), len(kOmega_03)), complex)

OutL_TB_03_kappa_minus_m_plus = np.zeros((len(delta_Omega_03_minus), len(kOmega_03)), complex)
OutL_TB_03_kappa_minus_m_minus = np.zeros((len(delta_Omega_03_minus), len(kOmega_03)), complex)
OutL_TB_03_kappa_minus = np.zeros((len(delta_Omega_03_minus), len(kOmega_03)), complex)

for i in range(len(delta_Omega_03)):
    OutL_TB_03_kappa_plus_m_plus[i]  = (-1j*gammaA / 2) * (PhiC_plus_03_conj * (PhiC_plus_03 - PhiD_plus_03 * np.exp(2j * kOmega_03 / 10)) / (delta_Omega_03_plus[i] - epsilon_m_plus_03 + 1j*gamma_loss_03))
    OutL_TB_03_kappa_plus_m_minus[i]  = (-1j*gammaA / 2) * (PhiC_minus_03_conj * (PhiC_minus_03 - PhiD_minus_03 * np.exp(2j * kOmega_03 / 10))/ (delta_Omega_03_plus[i] - epsilon_m_minus_03  + 1j*gamma_loss_03))

    OutL_TB_03_kappa_plus = (OutL_TB_03_kappa_plus_m_plus + OutL_TB_03_kappa_plus_m_minus)*np.conjugate(OutL_TB_03_kappa_plus_m_plus + OutL_TB_03_kappa_plus_m_minus)

    OutL_TB_03_kappa_minus_m_plus[i] = (-1j*gammaA / 2) * (PhiD_plus_03_conj * (PhiC_plus_03 * np.exp(-2j * kOmega_03 / 10) - PhiD_plus_03) / (delta_Omega_03_minus[i] - epsilon_m_plus_03 + 1j*gamma_loss_03) )
    OutL_TB_03_kappa_minus_m_minus[i] = (-1j * gammaA / 2) * (PhiD_minus_03_conj * (PhiC_minus_03 * np.exp(-2j * kOmega_03 / 10) - PhiD_minus_03) / (delta_Omega_03_minus[i] - epsilon_m_minus_03 + 1j * gamma_loss_03))

    OutL_TB_03_kappa_minus = (OutL_TB_03_kappa_minus_m_minus + OutL_TB_03_kappa_minus_m_plus)*np.conjugate(OutL_TB_03_kappa_minus_m_minus + OutL_TB_03_kappa_minus_m_plus)

    OutL_TB_03_kappa = (OutL_TB_03_kappa_minus + OutL_TB_03_kappa_plus )

plt.imshow(np.abs(OutL_TB_03_kappa), interpolation='nearest', origin='lower', aspect='auto')
# plt.colorbar()
# plt.pcolor(kOmega_03, delta_Omega_03, np.abs(TB_03_kappa), vmin = 0.15, vmax=0.65)
# plt.imshow(np.abs(TB_03_kappa), interpolation='nearest', origin='lower', aspect='auto', cmap='afmhot_r', vmin = 0, vmax=50)


# plt.ylim(90, 130)

plt.tick_params(
axis='both',          # changes apply to the x-axis
which='both',      # both major and minor ticks are affected
bottom=False,      # ticks along the bottom edge are off
top=False,         # ticks along the top edge are off
left=False,
right = False,
labelleft=False,
labelbottom=False) # labels along the bottom edge are off

# plt.savefig("5GHz.png", dpi=1000, bbox_inches='tight')
# v = np.linspace(0, 1.0, 2, endpoint=True)
# plt.colorbar()
plt.title("|Out_L|")
plt.show()

#############################

plt.imshow(np.abs(OutR_TB_03_kappa) + np.abs(OutL_TB_03_kappa), interpolation='nearest', origin='lower', aspect='auto')
plt.tick_params(
axis='both',          # changes apply to the x-axis
which='both',      # both major and minor ticks are affected
bottom=False,      # ticks along the bottom edge are off
top=False,         # ticks along the top edge are off
left=False,
right = False,
labelleft=False,
labelbottom=False) # labels along the bottom edge are off
plt.title("|Out_L| + |Out_L|")
plt.show()

##############################

plt.imshow(np.abs(OutR_TB_03_kappa) - np.abs(OutL_TB_03_kappa), interpolation='nearest', origin='lower', aspect='auto')
plt.tick_params(
axis='both',          # changes apply to the x-axis
which='both',      # both major and minor ticks are affected
bottom=False,      # ticks along the bottom edge are off
top=False,         # ticks along the top edge are off
left=False,
right = False,
labelleft=False,
labelbottom=False) # labels along the bottom edge are off
plt.title("|Out_L| - |Out_L|")
plt.show()

##############################

from scipy.fft import fft, fftfreq, fftshift

delta_Omega_03_plus = 3

TB_03_kappa_plus_m_plus_2 = np.zeros((1, len(kOmega_03)), complex)
TB_03_kappa_plus_m_minus_2 = np.zeros((1, len(kOmega_03)), complex)
TB_03_kappa_plus_2 = np.zeros((1, len(kOmega_03)), complex)

# TB_03_kappa_minus_m_plus_2 = np.zeros((len(delta_Omega_03_minus), len(kOmega_03)), complex)
# TB_03_kappa_minus_m_minus_2 = np.zeros((len(delta_Omega_03_minus), len(kOmega_03)), complex)
# TB_03_kappa_minus_2 = np.zeros((len(delta_Omega_03_minus), len(kOmega_03)), complex)


TB_03_kappa_plus_m_plus_2  = (-1j*gammaA / 2) * (PhiC_plus_03_conj * (PhiC_plus_03 + PhiD_plus_03 * np.exp(2j * kOmega_03 / 8.67)) / (delta_Omega_03_plus - epsilon_m_plus_03 + 1j*gamma_loss_03))
TB_03_kappa_plus_m_minus_2  = (-1j*gammaA / 2) * (PhiC_minus_03_conj * (PhiC_minus_03 + PhiD_minus_03 * np.exp(2j * kOmega_03 / 8.67))/ (delta_Omega_03_plus - epsilon_m_minus_03  + 1j*gamma_loss_03))

TB_03_kappa_plus_2 = (TB_03_kappa_plus_m_plus_2 + TB_03_kappa_plus_m_minus_2)*np.conjugate(TB_03_kappa_plus_m_plus_2 + TB_03_kappa_plus_m_minus_2)

# TB_03_kappa_minus_m_plus_2[i] = (-1j*gammaA / 2) * (PhiD_plus_03_conj * (PhiC_plus_03 * np.exp(-2j * kOmega_03 / 8.67) + PhiD_plus_03) / (delta_Omega_03_minus[i] - epsilon_m_plus_03 + 1j*gamma_loss_03) )
# TB_03_kappa_minus_m_minus_2[i] = (-1j * gammaA / 2) * (PhiD_minus_03_conj * (PhiC_minus_03 * np.exp(-2j * kOmega_03 / 8.67) + PhiD_minus_03) / (delta_Omega_03_minus[i] - epsilon_m_minus_03 + 1j * gamma_loss_03))

# TB_03_kappa_minus_2 = (TB_03_kappa_minus_m_minus + TB_03_kappa_minus_m_plus)*np.conjugate(TB_03_kappa_minus_m_minus + TB_03_kappa_minus_m_plus)

TB_03_kappa_2 = (TB_03_kappa_plus_m_plus_2)

# TB_03_kappa = (TB_03_kappa_minus + TB_03_kappa_plus)

plt.plot(kOmega_03, np.abs(TB_03_kappa_2))

# N = 85e3
# T = 10e-9

yf = fft(OutL_TB_03_kappa_plus_m_plus + OutL_TB_03_kappa_plus_m_minus)
xf = fftfreq(N, T)[:N//2]

print(len(xf))
print(len(yf))

yf_2 = 2.0/N * np.abs(yf[0:N//2])
print(len(yf_2))

plt.plot(xf, 2.0/N * np.abs(yf[0:N//2]))
# plt.xlim(-0.000000001, 0.0000000005)
plt.show()


# xf = fftshift(xf)
# yplot = fftshift(yf)
# import matplotlib.pyplot as plt
# plt.plot(xf, 1.0/N * np.abs(yplot))
# plt.grid()
# plt.show()


#%%
# OutL_TB_03_kappa_plus_m_plus = np.zeros((len(delta_Omega_03_plus), len(kOmega_03)), complex)
# OutL_TB_03_kappa_plus_m_minus = np.zeros((len(delta_Omega_03_plus), len(kOmega_03)), complex)
# OutL_TB_03_kappa_plus = np.zeros((len(delta_Omega_03_plus), len(kOmega_03)), complex)

# OutL_TB_03_kappa_minus_m_plus = np.zeros((len(delta_Omega_03_minus), len(kOmega_03)), complex)
# OutL_TB_03_kappa_minus_m_minus = np.zeros((len(delta_Omega_03_minus), len(kOmega_03)), complex)
# OutL_TB_03_kappa_minus = np.zeros((len(delta_Omega_03_minus), len(kOmega_03)), complex)

# for i in range(len(delta_Omega_03)):
#     OutL_TB_03_kappa_plus_m_plus[i]  = (-1j*gammaA / 2) * (PhiC_plus_03_conj * (PhiC_plus_03 - PhiD_plus_03 * np.exp(2j * kOmega_03 / 8.67)) / (delta_Omega_03_plus[i] - epsilon_m_plus_03 + 1j*gamma_loss_03))
#     OutL_TB_03_kappa_plus_m_minus[i]  = (-1j*gammaA / 2) * (PhiC_minus_03_conj * (PhiC_minus_03 - PhiD_minus_03 * np.exp(2j * kOmega_03 / 8.67))/ (delta_Omega_03_plus[i] - epsilon_m_minus_03  + 1j*gamma_loss_03))

#     OutL_TB_03_kappa_plus = (OutL_TB_03_kappa_plus_m_plus + OutL_TB_03_kappa_plus_m_minus)*np.conjugate(OutL_TB_03_kappa_plus_m_plus + OutL_TB_03_kappa_plus_m_minus)

#     OutL_TB_03_kappa_minus_m_plus[i] = (-1j*gammaA / 2) * (PhiD_plus_03_conj * (PhiC_plus_03 * np.exp(-2j * kOmega_03 / 8.67) - PhiD_plus_03) / (delta_Omega_03_minus[i] - epsilon_m_plus_03 + 1j*gamma_loss_03) )
#     OutL_TB_03_kappa_minus_m_minus[i] = (-1j * gammaA / 2) * (PhiD_minus_03_conj * (PhiC_minus_03 * np.exp(-2j * kOmega_03 / 8.67) - PhiD_minus_03) / (delta_Omega_03_minus[i] - epsilon_m_minus_03 + 1j * gamma_loss_03))

#     OutL_TB_03_kappa_minus = (OutL_TB_03_kappa_minus_m_minus + OutL_TB_03_kappa_minus_m_plus)*np.conjugate(OutL_TB_03_kappa_minus_m_minus + OutL_TB_03_kappa_minus_m_plus)

#     OutL_TB_03_kappa = (OutL_TB_03_kappa_minus + OutL_TB_03_kappa_plus )

# plt.imshow(np.abs(OutL_TB_03_kappa), interpolation='nearest', origin='lower', aspect='auto')

# # plt.pcolor(kOmega_03, delta_Omega_03, np.abs(TB_03_kappa), norm = colors.LogNorm(vmin=TB_03_kappa.min(), vmax=TB_03_kappa.max()))
# # plt.colorbar()

# plt.tick_params(
# axis='both',          # changes apply to the x-axis
# which='both',      # both major and minor ticks are affected
# bottom=False,      # ticks along the bottom edge are off
# top=False,         # ticks along the top edge are off
# left=False,
# right = False,
# labelleft=False,
# labelbottom=False) # labels along the bottom edge are off

# plt.show()




# # A1 = np.abs(TB_03_kappa)

# # print(np.shape(A1))

# # B1 = np.zeros(len(delta_Omega_03))

# # B1 = np.sum(A1**2, axis=1)

# # # np.savetxt('DOS.csv', (delta_Omega_03, B1), delimiter=',')

# # y1 = np.loadtxt('DOS.csv', delimiter = ',')

# # # plt.plot(delta_Omega_03*19, y1[1])
# # plt.plot(delta_Omega_03*19, B1)


# # plt.xlabel("Optical detuning [GHz]")

# # plt.savefig("DOS.pdf", dpi=3000)



# # plt.show()

# #%%
# #Extract the phase - Equations 9 - 10

# S_out_S_in_kappa_plus_m_plus = np.zeros((len(delta_Omega_03_minus), len(kOmega_03)), complex)
# S_out_S_in_kappa_plus_m_minus = np.zeros((len(delta_Omega_03_minus), len(kOmega_03)), complex)
# # 
# S_out_S_in_kappa_minus_m_plus = np.zeros((len(delta_Omega_03_minus), len(kOmega_03)), complex)
# S_out_S_in_kappa_minus_m_minus = np.zeros((len(delta_Omega_03_minus), len(kOmega_03)), complex)

# S_out_S_in_kappa_plus = np.zeros((len(delta_Omega_03_minus), len(kOmega_03)), complex)
# S_out_S_in_kappa_minus = np.zeros((len(delta_Omega_03_minus), len(kOmega_03)), complex)

# S_out_S_in = np.zeros((len(delta_Omega_03_minus), len(kOmega_03)), complex)

# for i in range(len(delta_Omega_03)):
#     S_out_S_in_kappa_plus_m_plus[i] = (-1j*gammaA / 4) * ((1 + 1*np.exp((2j * kOmega_03/8.67) - 1j*phase))/ (delta_Omega_03_plus[i] - epsilon_m_plus_03 + 1j*gamma_loss_03)) 
#     S_out_S_in_kappa_plus_m_minus[i] = (-1j*gammaA / 4) * ((1 - 1*np.exp((2j * kOmega_03/8.67) - 1j*phase))/ (delta_Omega_03_plus[i] - epsilon_m_plus_03 + 1j*gamma_loss_03))
    
#     S_out_S_in_kappa_plus = S_out_S_in_kappa_plus_m_plus + S_out_S_in_kappa_plus_m_minus
#     # 
#     S_out_S_in_kappa_minus_m_plus[i] = (-1j*gammaA / 4) * ((1 + 1*np.exp((-2j * kOmega_03/8.67) + 1j*phase))/ (delta_Omega_03_minus[i] - epsilon_m_minus_03 + 1j * gamma_loss_03))
#     S_out_S_in_kappa_minus_m_minus[i] = (-1j*gammaA / 4) * ((1 - 1*np.exp((-2j * kOmega_03/8.67) + 1j*phase))/ (delta_Omega_03_minus[i] - epsilon_m_minus_03 + 1j * gamma_loss_03))

#     S_out_S_in_kappa_minus = S_out_S_in_kappa_minus_m_plus + S_out_S_in_kappa_minus_m_minus

#     S_out_S_in = (S_out_S_in_kappa_plus + S_out_S_in_kappa_minus)*np.conjugate(S_out_S_in_kappa_plus + S_out_S_in_kappa_minus)

# plt.imshow(np.abs(S_out_S_in), interpolation='nearest', origin='lower', aspect='auto')

# # plt.show()

# #%%

# # Taking the maximum output intensity value of each vertical slice (fixed kf) from the chosen band
# # For example, choose lower band from upper region, meaning m = 1
# # This corresponding to TB_03_Test

# TB_03_Test_MAX = np.zeros(len(kOmega_03), complex)

# for i in range(len(kOmega_03)):
    
#     TB_03_Test_MAX[i] =  np.max(TB_03_kappa[105:126, i])
#     # TB_03_Test_MAX[i] =  np.max(TB_03_kappa[129:150, i])
    
#     # TB_03_Test_MAX[i] =  np.max(TB_03_kappa[50:72, i])
#     # TB_03_Test_MAX[i] =  np.max(TB_03_kappa[73:90, i])
#     # TB_03_Test_MAX[i] =  np.max(TB_03_Test[:, i])


# plt.plot(kOmega_03, TB_03_Test_MAX)
# plt.show()

# ###

# S2 = TB_03_Test_MAX

# S2_max = np.max(TB_03_Test_MAX)

# Coff_m = (2*S2**2/S2_max**2) - 1


# # plt.plot(kOmega_03, Coff_m)
# # plt.plot(kOmega_03, Coff_plus_exp)
# plt.xlim(0, 10*np.pi)

# # plt.tick_params(
# # axis='both',          # changes apply to the x-axis
# # which='both',      # both major and minor ticks are affected
# # bottom=False,      # ticks along the bottom edge are off
# # top=False,         # ticks along the top edge are off
# # left=False,
# # right = False,
# # labelleft=False,
# # labelbottom=False) # labels along the bottom edge are off

# # plt.show()

# #%%

# arg_phase_plus_m_plus = (2*kOmega_03/8.67) + np.arccos((Coff_m))
# arg_phase_minus_m_plus = (2*kOmega_03/8.67) - np.arccos((Coff_m))



# for i in range(len(arg_phase_plus_m_plus)):
#     if arg_phase_plus_m_plus[i] > np.pi:
#         arg_phase_plus_m_plus[i] = (2*kOmega_03[i]/8.67) + np.arccos((Coff_m[i])) - 2*np.pi

    
# for i in range(len(arg_phase_minus_m_plus)):
#     if arg_phase_minus_m_plus[i] > np.pi:
#         arg_phase_minus_m_plus[i] = (2*kOmega_03[i]/8.67) - np.arccos((Coff_m[i])) - 2*np.pi


# plt.plot(kOmega_03, arg_phase_plus_m_plus, color='cyan', marker='.')
# plt.plot(kOmega_03, arg_phase_minus_m_plus, color='magenta', marker='.')

# plt.plot(kOmega_03, phase, 'blue')
# plt.ylim(-np.pi, np.pi)


# plt.xlim(0*np.pi, 10*np.pi)


# # print(kOmega_03[83])

# # print(kOmega_03[95])

# # print(kOmega_03[110])

# # print(kOmega_03[122])

# # print(kOmega_03[135])

# # print(kOmega_03[145])


# # # slop_1 = (arg_phase_minus_m_plus[9] - arg_phase_minus_m_plus[5]) / (kOmega_03[9] - kOmega_03[5])
# # # slop_2 = (arg_phase_minus_m_plus[22] - arg_phase_minus_m_plus[18]) / (kOmega_03[22] - kOmega_03[18])
# # # slop_3 = (arg_phase_minus_m_plus[34] - arg_phase_minus_m_plus[30]) / (kOmega_03[34] - kOmega_03[30])
# # # slop_4 = (arg_phase_minus_m_plus[47] - arg_phase_minus_m_plus[43]) / (kOmega_03[47] - kOmega_03[43])
# # # slop_5 = (arg_phase_minus_m_plus[60] - arg_phase_minus_m_plus[56]) / (kOmega_03[60] - kOmega_03[56])
# # # slop_6 = (arg_phase_minus_m_plus[72] - arg_phase_minus_m_plus[68]) / (kOmega_03[72] - kOmega_03[68])

# # # total_slope_1 = slop_1 + slop_2 + slop_3 + slop_4 + slop_5 + slop_6

# # # print(total_slope_1)

# # slop_1 = (arg_phase_plus_m_plus[85] - arg_phase_plus_m_plus[81]) / (kOmega_03[85] - kOmega_03[81])
# # slop_2 = (arg_phase_plus_m_plus[97] - arg_phase_plus_m_plus[93]) / (kOmega_03[97] - kOmega_03[93])
# # slop_3 = (arg_phase_plus_m_plus[112] - arg_phase_plus_m_plus[108]) / (kOmega_03[112] - kOmega_03[108])
# # slop_4 = (arg_phase_plus_m_plus[124] - arg_phase_plus_m_plus[120]) / (kOmega_03[124] - kOmega_03[120])
# # slop_5 = (arg_phase_plus_m_plus[137] - arg_phase_plus_m_plus[133]) / (kOmega_03[137] - kOmega_03[133])
# # slop_6 = (arg_phase_plus_m_plus[147] - arg_phase_plus_m_plus[143]) / (kOmega_03[147] - kOmega_03[143])

# # total_slope_2 = slop_1 + slop_2 + slop_3 + slop_4 + slop_5 + slop_6

# # print(total_slope_2)

# # # plt.title("m plus")
# # # plt.text(0, -3.5, r"$0$")
# # # plt.text(18, -3.5, r"$6\pi$")
# # # plt.text(9, -3.5, r"$3\pi$")

# # # plt.tick_params(
# # # axis='both',          # changes apply to the x-axis
# # # which='both',      # both major and minor ticks are affected
# # # bottom=False,      # ticks along the bottom edge are off
# # # top=False,         # ticks along the top edge are off
# # # left=False,
# # # right = False,
# # # labelleft=False,
# # # labelbottom=False) # labels along the bottom edge are off

# plt.show()

# #%%

# arg_phase_plus_m_minus = (2*kOmega_03/8.67) + np.arccos(-(Coff_m))
# arg_phase_minus_m_minus = (2*kOmega_03/8.67) - np.arccos(-(Coff_m))


# for i in range(len(arg_phase_plus_m_minus)):
#     if arg_phase_plus_m_minus[i] > np.pi:
#         arg_phase_plus_m_minus[i] = (2*kOmega_03[i]/8.67) + np.arccos(-(Coff_m[i])) - 2*np.pi

    
# for i in range(len(arg_phase_minus_m_minus)):
#     if arg_phase_minus_m_minus[i] > np.pi:
#         arg_phase_minus_m_minus[i] = (2*kOmega_03[i]/8.67) - np.arccos(-(Coff_m[i])) - 2*np.pi


# plt.plot(kOmega_03, arg_phase_plus_m_minus, color='cyan', marker='.')
# plt.plot(kOmega_03, arg_phase_minus_m_minus, color='magenta', marker='.')

# plt.plot(kOmega_03, phase, 'blue')
# plt.ylim(-np.pi, np.pi)
# # plt.xlabel("x")
# # plt.ylabel("phi")
# plt.xlim(0*np.pi, 10*np.pi)

# print(kOmega_03[10])


# # print(kOmega_03[95])

# # print(kOmega_03[110])

# # print(kOmega_03[122])

# # print(kOmega_03[135])

# # print(kOmega_03[145])


# slope_plus_1 = (arg_phase_minus_m_minus[145] - arg_phase_minus_m_minus[141]) / (kOmega_03[145] - kOmega_03[141])
# print("slope_plus: {}". format(slope_plus_1))

# slope_plus_2 = (arg_phase_plus_m_minus[133] - arg_phase_plus_m_minus[129]) / (kOmega_03[133] - kOmega_03[129])
# print("slope_plus: {}". format(slope_plus_2))

# slope_plus_3 = (arg_phase_plus_m_minus[18] - arg_phase_plus_m_minus[14]) / (kOmega_03[18] - kOmega_03[14])
# print("slope_plus: {}". format(slope_plus_3))


# total_slope_1 = slope_plus_1 + slope_plus_2 + slope_plus_3

# print(total_slope_1)

# theo_slope = (phase[6] - phase[2]) / (kOmega_03[6] - kOmega_03[2])
# print("theo slope: {}".format(theo_slope))

# # plt.title("m minus")
# # plt.text(0, -3.5, r"$0$")
# # plt.text(18, -3.5, r"$6\pi$")
# # plt.text(4.5, -3.5, r"$3\pi$")

# print(kOmega_03[75])
# print(arg_phase_plus_m_minus[28])

# total = 0

# for i in range(0, 41):
#     total = total + arg_phase_minus_m_minus[i]
    
# print(total)





# plt.tick_params(
# axis='both',          # changes apply to the x-axis
# which='both',      # both major and minor ticks are affected
# bottom=False,      # ticks along the bottom edge are off
# top=False,         # ticks along the top edge are off
# left=False,
# right = False,
# labelleft=False,
# labelbottom=False) # labels along the bottom edge are off

# # plt.show()

# #%%

# # Exact_Zak_array = np.zeros(len(kOmega_03), complex)


# # for i in range(len(kOmega_03)):
    
# #     if kOmega_03[i] < 4:
    
# #         Exact_Zak_array[i] = arg_phase_plus_m_minus[i]
    
# #     elif 4 < kOmega_03[i] < 5:
        
# #         Exact_Zak_array[i] = arg_phase_plus_m_minus[i]
        
# #     elif 5 < kOmega_03[i] < 10:
            
# #         Exact_Zak_array[i] = arg_phase_minus_m_minus[i]
        
# #     elif 10 < kOmega_03[i] < 12:
                
# #         Exact_Zak_array[i] = arg_phase_minus_m_minus[i]
        

# # plt.plot(kOmega_03, Exact_Zak_array, color='orange', marker='.')

# # plt.plot(kOmega_03, phase, 'blue')

# # plt.ylim(-np.pi, np.pi)
# # plt.xlim(0, 10*np.pi)

# # plt.show()

# # #%%

# # print("Red line: {}".format(arg_phase_minus_m_plus))

# # print("Green line: {}".format(arg_phase_plus_m_plus))


# #%%





# #%%

# # print("start point 1: {}".format(kOmega_03[60]))

# # print("end point 1: {}".format(kOmega_03[120]))

# # print("start phase 1: {}".format(phase[60]))

# # print("end phase 1: {}".format(phase[120]))

# # slope_theoretical_1 = (phase[120] - phase[60]) / (kOmega_03[120] - kOmega_03[60])
# # slope_simulation_1 = (arg_phase_minus_m_minus[120] - arg_phase_minus_m_minus[60]) / (kOmega_03[120] - kOmega_03[60])

# # print("theoretical slope 1: {}".format(slope_theoretical_1))
# # print("simulation slope 1: {}".format(slope_simulation_1))



# # print("start point 2: {}".format(kOmega_03[0]))

# # print("end point 2: {}".format(kOmega_03[40]))

# # print("start phase 2: {}".format(phase[0]))

# # print("end phase 2: {}".format(phase[40]))

# # slope_theoretical_2 = (phase[40] - phase[0]) / (kOmega_03[40] - kOmega_03[0])
# # slope_simulation_2 = (arg_phase_minus_m_minus[40] - arg_phase_minus_m_minus[0]) / (kOmega_03[40] - kOmega_03[0])

# # print("theoretical slope 2: {}".format(slope_theoretical_2))
# # print("simulation slope 2: {}".format(slope_simulation_2))


# # total_phase = -0.5*slope_simulation_1 + 0.5 * slope_simulation_2
# # print("total phase: {}".format(total_phase))

    
# # #%%
# # a = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

# # for i in range(len(a)):
    
# #     if a[i] < 5:
        
# #         print(a[i])
        

# # 
