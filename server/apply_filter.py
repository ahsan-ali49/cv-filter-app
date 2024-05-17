import cv2
import numpy as np
import sys
import os

def apply_gaussian_lowpass(img):
    return cv2.GaussianBlur(img, (5, 5), 0)

def butterworth_lowpass(img, d0=30, n=2):
    f = np.fft.fft2(img)
    fshift = np.fft.fftshift(f)
    rows, cols = img.shape
    crow, ccol = rows//2, cols//2

    mask = np.zeros((rows, cols), np.uint8)
    for u in range(rows):
        for v in range(cols):
            distance = np.sqrt((u-crow)**2 + (v-ccol)**2)
            mask[u, v] = 1 / (1 + (distance / d0)**(2*n))

    fshift = fshift * mask
    f_ishift = np.fft.ifftshift(fshift)
    img_back = np.fft.ifft2(f_ishift)
    img_back = np.abs(img_back)
    
    return np.uint8(img_back)

def apply_laplacian_highpass(img):
    return cv2.Laplacian(img, cv2.CV_64F)

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
