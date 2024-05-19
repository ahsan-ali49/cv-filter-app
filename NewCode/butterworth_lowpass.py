# -*- coding: utf-8 -*-
"""
Created on Sat May 11 13:05:57 2024

@author: AHSAN
"""
# Libraries
import cv2
import numpy as np
import matplotlib.pyplot as plt

# Open the image
f = cv2.imread("rubik.png", 0)

plt.imshow(f, cmap='gray')
plt.axis('off')
plt.show()

# Transform image into freq. domain shifted the low freq.
F = np.fft.fft2(f)
Fshift = np.fft.fftshift(F)

plt.imshow(np.log1p(np.abs(F)), cmap='gray')
plt.axis('off')
plt.show()

plt.imshow(np.log1p(np.abs(Fshift)), cmap='gray')
plt.axis("off")
plt.show()

# Butterworth Low Pass Filter
M, N = f.shape
H = np.zeros((M, N), dtype=np.float32)
D0 = 10 # cut of frequency
n = 1 # order
for u in range(M):
        for v in range(N):
            D = np.sqrt((u-M/2)**2 + (v-N/2)**2)
            H[u,v] = 1 / (1 + (D/D0)**(2*n))

plt.imshow(H, cmap='gray')
plt.axis('off')
plt.show()

# Frequency domain image filters
Gshift = Fshift * H
G = np.fft.ifftshift(Gshift)
g = np.abs(np.fft.ifft2(G))

plt.imshow(g, cmap='gray')
plt.axis('off')
plt.show()