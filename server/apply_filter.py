import cv2
import numpy as np
import sys
import os

def apply_gaussian_lowpass(img):
    return cv2.GaussianBlur(src=img, ksize=(3,3), sigmaX=0, sigmaY=0)

# def butterworth_lowpass(img, d0=30, n=2):
#     f = np.fft.fft2(img)
#     fshift = np.fft.fftshift(f)
#     rows, cols = img.shape
#     crow, ccol = rows//2, cols//2

#     mask = np.zeros((rows, cols), np.uint8)
#     for u in range(rows):
#         for v in range(cols):
#             distance = np.sqrt((u-crow)**2 + (v-ccol)**2)
#             mask[u, v] = 1 / (1 + (distance / d0)**(2*n))

#     fshift = fshift * mask
#     f_ishift = np.fft.ifftshift(fshift)
#     img_back = np.fft.ifft2(f_ishift)
#     img_back = np.abs(img_back)
    
#     return np.uint8(img_back)

def butterworth_lowpass(img, D0=10, n=1):
    # Convert image to float32 for processing
    img_float32 = np.float32(img)

    # Compute the 2D FFT of the input image
    F = np.fft.fft2(img_float32)
    Fshift = np.fft.fftshift(F)

    # Butterworth Low Pass Filter
    M, N = img.shape
    H = np.zeros((M, N), dtype=np.float32)
    for u in range(M):
        for v in range(N):
            D = np.sqrt((u - M / 2) ** 2 + (v - N / 2) ** 2)
            H[u, v] = 1 / (1 + (D / D0) ** (2 * n))

    # Apply the filter and inverse FFT
    Gshift = Fshift * H
    G = np.fft.ifftshift(Gshift)
    g = np.abs(np.fft.ifft2(G))

    # Convert the output back to uint8
    g_uint8 = np.uint8(g)
    return g_uint8

def apply_laplacian_highpass(img):
    # Laplacian kernel
    kernel = np.array([[1, 1, 1],
                       [1, -8, 1],
                       [1, 1, 1]])

    # Apply the Laplacian kernel using filter2D
    LaplacianImage = cv2.filter2D(src=img, ddepth=-1, kernel=kernel)
    
    # Scale factor for enhancing the Laplacian effect
    c = -1

    # Enhanced image by subtracting the Laplacian from the original image
    g = img + c * LaplacianImage

    # Clipping the image to maintain pixel values between 0 and 255
    gClip = np.clip(g, 0, 255)
    
    return gClip.astype('uint8')

def histogram_matching(src, reference):
    src_hist, _ = np.histogram(src.flatten(), 256, [0, 256])
    src_cdf = src_hist.cumsum()
    ref_hist, _ = np.histogram(reference.flatten(), 256, [0, 256])
    ref_cdf = ref_hist.cumsum()
    
    src_cdf_norm = src_cdf / src_cdf[-1]
    ref_cdf_norm = ref_cdf / ref_cdf[-1]
    lut = np.interp(src_cdf_norm, ref_cdf_norm, np.arange(256))
    result = np.uint8(lut[src.flatten()]).reshape(src.shape)
    return result

# def extract_features_and_classify(img, reference_images, reference_labels):
#     # Placeholder for actual feature extraction and classification logic
#     # Assuming reference_descriptors and reference_labels are loaded and trained outside this function
#     return "Feature-based classification result"

if __name__ == "__main__":
    image_path = sys.argv[1]
    filter_type = sys.argv[2]
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

    if img is None:
        raise ValueError("Image not loaded correctly.")

    if filter_type == 'gaussian_lowpass':
        processed_img = apply_gaussian_lowpass(img)
    elif filter_type == 'butterworth_lowpass':
        processed_img = butterworth_lowpass(img)
    elif filter_type == 'laplacian_highpass':
        processed_img = apply_laplacian_highpass(img)
    elif filter_type == 'histogram_matching':
        # Example: Load a reference image for histogram matching
        ref_image = cv2.imread('reference.jpg', cv2.IMREAD_GRAYSCALE)
        processed_img = histogram_matching(img, ref_image)
    # elif filter_type == 'feature_extraction':
    #     # Example: Load reference images and labels
    #     processed_img = extract_features_and_classify(img, None, None)
    else:
        raise ValueError("Unsupported filter type specified.")

    output_path = 'output_' + os.path.basename(image_path)
    cv2.imwrite(output_path, processed_img)
    print(output_path)  # Output the file path to Node.js
