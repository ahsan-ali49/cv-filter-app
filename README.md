# Image Filter Application

This application allows users to upload images and apply various filters, such as Gaussian Lowpass, \
Butterworth Lowpass, Laplacian Highpass, and Histogram Matching. The processed image is \
displayed alongside the original for comparison.

## Prerequisites

Before you start, ensure you have the following installed:

* [Node.js](https://nodejs.org/en) (v14.x or later)
* [Python](https://www.python.org/downloads/) (v3.8 or later)
* [OpenCV-Python](https://pypi.org/project/opencv-python/): For image processing functionalities
* [Numpy](https://numpy.org/): Required for mathematical operations in Python\
\
You can install the required Python libraries using pip:\
\
`pip install opencv-python numpy`

## Installation
### 1. Clone the Repository
`git clone https://your-repository-url.com` \
`cd image-filter-app`
### 2. Install Node.js Dependencies
Navigate to the project directory and install the required Node.js packages.\
`npm install`
### 3. Running the Server
Start the Express server which handles the image processing requests.\
`node server.js`\
You should see the output indicating that the server is running on port 5000.
### 4. Start the React Application
In a new terminal window, start the frontend application.\
`npm start`\
This will open the web application in your default browser, typically at\
http://localhost:3000.

## Usage
### 1. Select an Image
Use the "Choose File" button to select an image file from your local computer.

### 2. Choose a Filter
Select the desired image filter from the dropdown menu:

* #### Lowpass Gaussian Filter (Spatial Domain)
* #### Lowpass Butterworth Filter (Frequency Domain)
* #### Highpass Laplacian Filter (Spatial Domain)
* #### Histogram Matching

### 3. Apply the Filter
Click the "Apply Filter" button to process the image. The processed image will be displayed next to the original image for comparison.

## Troubleshooting

* ### Server Not Starting: 
Ensure that all Python dependencies are correctly installed and that Python scripts are executable.

* ### Image Not Processing: 
Check the console for any errors related to file uploads or Python script execution.

## Contributing
Feel free to fork the repository and submit pull requests with enhancements or fixes.

## License
Specify your licensing information here.
