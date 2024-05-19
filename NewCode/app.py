import os
import cv2
import numpy as np

def load_image(image_path):
    if not os.path.isfile(image_path):
        print(f"Error: The file {image_path} does not exist.")
        return None
    image = cv2.imread(image_path)  # Load as color image
    if image is None:
        print(f"Error: Unable to load the image at {image_path}.")
        return None
    return image

def apply_gaussian_lowpass(image, sigma=1.0):
    kernel_size = int(6 * sigma + 1)
    kernel_size = kernel_size + (kernel_size % 2 == 0)  # Ensure kernel size is odd
    blurred = cv2.GaussianBlur(image, (kernel_size, kernel_size), sigma)
    return blurred

def apply_butterworth_lowpass(image, d0=30, n=2):
    if len(image.shape) > 2 and image.shape[2] == 3:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    rows, cols = image.shape[:2]
    crow, ccol = rows // 2, cols // 2

    dft = cv2.dft(np.float32(image), flags=cv2.DFT_COMPLEX_OUTPUT)
    dft_shift = np.fft.fftshift(dft)

    mask = np.zeros((rows, cols, 2), np.float32)
    for i in range(rows):
        for j in range(cols):
            distance = np.sqrt((i - crow)**2 + (j - ccol)**2)
            mask[i, j] = 1 / (1 + (distance / d0)**(2 * n))

    fshift = dft_shift * mask
    f_ishift = np.fft.ifftshift(fshift)
    img_back = cv2.idft(f_ishift)
    img_back = cv2.magnitude(img_back[:, :, 0], img_back[:, :, 1])
    cv2.normalize(img_back, img_back, 0, 255, cv2.NORM_MINMAX)
    return np.uint8(img_back)

def main():
    image_path = 'first.jpg'  # Replace with the actual path to your image

    # Load the original image
    original_image = load_image(image_path)
    if original_image is None:
        return
    
    # Apply Gaussian Lowpass Filter to the original image
    gaussian_blur_sigma = 1.5  # Change this value to adjust the blurriness
    gaussian_filtered_image = apply_gaussian_lowpass(original_image, sigma=gaussian_blur_sigma)

    # Apply Butterworth Lowpass Filter to the grayscale version of the original image
    d0 = 30  # Cutoff frequency
    n = 2  # Order of the filter
    butterworth_filtered_image = apply_butterworth_lowpass(original_image, d0, n)
    
    # Display the results
    cv2.imshow('Original Image', original_image)
    cv2.imshow(f'Gaussian Lowpass Filtered (sigma={gaussian_blur_sigma})', gaussian_filtered_image)
    cv2.imshow(f'Butterworth Lowpass Filtered (D0={d0}, n={n})', butterworth_filtered_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
