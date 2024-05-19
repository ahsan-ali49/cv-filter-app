import cv2
import numpy as np
import matplotlib.pyplot as plt

# originmal image
original_image = cv2.imread("./orig.png", 0)

#blur and sharpen convolution kernel
M = 3
blur_kernel = np.ones((M,M))*1/(M*M)

sharpen_kernel = np.array([[0, -1, 0],
                            [-1, 5, -1],
                            [0, -1, 0]],
                          dtype=np.float32)
# apply the convolution
blur_image = cv2.filter2D(src=original_image,
                          ddepth=-1,
                          kernel=blur_kernel)

sharpen_image = cv2.filter2D(src=original_image,
                             ddepth=-1,
                             kernel=sharpen_kernel)
# display the original_image result
plt.imshow(original_image, cmap="gray")
plt.axis("off")
plt.show()

# display the blur_image result
plt.imshow(blur_image, cmap="gray")
plt.axis("off")
plt.show()

# display the sharpen result
plt.imshow(sharpen_image, cmap="gray")
plt.axis("off")
plt.show()

# built in image blurring
builtin_blur = cv2.blur(src=original_image, ksize=(3,3)) 

# display builtin_blur image result
plt.imshow(builtin_blur, cmap="gray")
plt.axis("off")
plt.show()

# builtin_median_blur image
builtin_median_blur = cv2.medianBlur(src=original_image, ksize=3) 

# display builtin_blur image result
plt.imshow(builtin_median_blur, cmap="gray")
plt.axis("off")
plt.show()

# builtin_gaussian_blur image
builtin_gaussian_blur = cv2.GaussianBlur(src=original_image, ksize=(3,3), sigmaX=0, sigmaY=0) 

# display builtin_blur image result
plt.imshow(builtin_gaussian_blur, cmap="gray")
plt.axis("off")
plt.show()