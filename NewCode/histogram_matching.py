# Importing Libraries
from skimage.io import imread
from skimage.exposure import cumulative_distribution
import numpy as np
import matplotlib.pyplot as plt

# Read/Load the Input and Template Image
image = (imread("lana.png", as_gray=True)*255).astype(np.uint8)
imageTemplate = (imread('sunset.jpg', as_gray=True)*255).astype(np.uint8)

plt.figure(figsize=(8,6))
plt.subplot(1,2,1)
plt.title("Input Image")
plt.imshow(image, cmap='gray')
plt.axis('off')
plt.subplot(1,2,2)
plt.title("Template Image")
plt.imshow(imageTemplate, cmap='gray')
plt.axis("off")
plt.show()

#Compute the Cumulative Distribution of input image
cdfImageInput, binsImageInput = cumulative_distribution(image)

plt.plot(binsImageInput, cdfImageInput, linewidth=5)
plt.xlim(0, 255)
plt.ylim(0,1)
plt.xlabel("Pixel Values")
plt.ylabel("Cumulative Probablity")
plt.show()

# Check the first and last bins and probability
print(f"First bins: {binsImageInput[0]}, Cumulative Probablity: {cdfImageInput[0]:.5f}")
print(f"Last bins: {binsImageInput[-1]}, Cumulative Probability: {cdfImageInput[0]:.5f}")

# pad beginning and ending pixel values:
cdfImageInput = np.insert(cdfImageInput, 0, [0]*binsImageInput[0]) # fill 0 in index 0 - 17
cdfImageInput = np.append(cdfImageInput, [1]*(255-binsImageInput[-1])) # fill 1 in index 247 - 255

plt.plot(cdfImageInput, linewidth=5)
plt.xlim(0, 255)
plt.ylim(0,1)
plt.xlabel("Pixel Values: ")
plt.ylabel("Cumulative Probability")
plt.show()

# compute the comulative distribution of image template
cdfImageTemplate, binsImageTemplate = cumulative_distribution(imageTemplate)

cdfImageTemplate = np.insert(cdfImageTemplate, 0, [0]*binsImageTemplate[0])
cdfImageTemplate = np.append(cdfImageTemplate, [1]*(255-binsImageTemplate[-1]))

plt.plot(cdfImageTemplate, linewidth=5)
plt.xlim(0,255)
plt.ylim(0,1)
plt.xlabel("Pixel Values")
plt.ylabel("Cumulative Probability")
plt.show()

plt.plot(cdfImageInput, linewidth=5, label="Input Image")
plt.plot(cdfImageTemplate, linewidth=5, label="Template")
plt.xlim(0,255)
plt.ylim(0,1)
plt.xlabel("Pixel Values")
plt.ylabel("Cumulative Probability")
plt.legend()
plt.show()

# Create and array of pixel values
pixels = np.arange(256)

new_pixels = np.interp(cdfImageInput, cdfImageTemplate, pixels)
plt.plot(new_pixels, linewidth=5)
plt.xlim(0,255)
plt.ylim(0,255)
plt.show()

# Map and Reshape in 2D array
imageOut = (np.reshape(new_pixels[image.ravel()], image.shape)).astype(np.uint8)

# Preview the result
plt.figure(figsize=(10,7))
plt.subplot(1,3,1)
plt.title("Image Input")
plt.imshow(image, cmap="gray")
plt.axis("off")
plt.subplot(1,3,2)
plt.title("Template Image")
plt.imshow(imageTemplate, cmap="gray")
plt.axis("off")
plt.subplot(1,3,3)
plt.title("Result")
plt.imshow(imageOut, cmap='gray')
plt.axis("off")
plt.show()