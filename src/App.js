import React, { useState } from 'react';
import { Button, Input, MenuItem, FormControl, Select, Box, Typography, Paper } from '@mui/material';
import axios from 'axios';

function App() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [selectedFilter, setSelectedFilter] = useState('');
  const [imageSrc, setImageSrc] = useState('');
  const [originalImageSrc, setOriginalImageSrc] = useState('');
  const [processedImageSrc, setProcessedImageSrc] = useState('');


  const handleFileChange = event => {
    const file = event.target.files[0];
    setSelectedFile(file);

    // Read the file and set it as the original image source
    const reader = new FileReader();
    reader.onloadend = () => {
        setOriginalImageSrc(reader.result);
    };
    reader.readAsDataURL(file);
};


  const handleFilterChange = event => {
    setSelectedFilter(event.target.value);
  };

  const handleSubmit = async () => {
    const formData = new FormData();
    formData.append('image', selectedFile);
    formData.append('filter', selectedFilter);

    try {
        const response = await axios.post('http://localhost:5000/upload', formData, {
            headers: {
                'Content-Type': 'multipart/form-data',
            },
        });
        setProcessedImageSrc(`data:image/jpeg;base64,${response.data}`);
    } catch (error) {
        console.error('Error uploading image:', error);
    }
  };


  return (
    <Box sx={{
      minHeight: '100vh',
      backgroundImage: 'url("/background.png")',
      backgroundSize: 'cover',
      backgroundPosition: 'center',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
    }}>
      <Paper elevation={3} sx={{ p: 2, pt:0, pb:0, maxWidth: 1200, width: '100%', display: 'flex', flexDirection: 'column', alignItems: 'center', margin: 2 }}>
        <Typography variant="h4" gutterBottom textAlign="center">
          Image Filter Application
        </Typography>
        <Input
          type="file"
          onChange={handleFileChange}
          disableUnderline
          fullWidth
          inputProps={{ accept: 'image/*' }}
          sx={{ mb: 1 }}
        />
        <FormControl fullWidth sx={{ mb: 1 }}>
          <Select
            value={selectedFilter}
            onChange={handleFilterChange}
            displayEmpty
            inputProps={{ 'aria-label': 'Without label' }}
          >
            <MenuItem value="">
              <em>None</em>
            </MenuItem>
            <MenuItem value="gaussian_lowpass">Lowpass Gaussain filter (spatial domian)</MenuItem>
            <MenuItem value="butterworth_lowpass">Lowpass butterworth filter (Frequency domian)</MenuItem>
            <MenuItem value="laplacian_highpass">HighPass Lalacian filter (spaical Domain)</MenuItem>
            <MenuItem value="histogram_matching">Histogram Matching</MenuItem>
          </Select>
        </FormControl>
        <Button variant="contained" onClick={handleSubmit} fullWidth sx={{ mb: 1 }}>
          Apply Filter
        </Button>
        <Box sx={{ display: 'flex', width: '100%', justifyContent: 'space-around', flexWrap: 'wrap' }}>
            {originalImageSrc && (
                <Box sx={{ maxWidth: '50%', p: 1, pb:0, pt:0 }}>
                    <Typography variant="subtitle1" gutterBottom>Original Image</Typography>
                    <img src={originalImageSrc} alt="Original" style={{ width: '100%' }} />
                </Box>
            )}
            {processedImageSrc && (
                <Box sx={{ maxWidth: '50%', p: 1, pt:0 }}>
                    <Typography variant="subtitle1" gutterBottom>Processed Image</Typography>
                    <img src={processedImageSrc} alt="Processed" style={{ width: '100%' }} />
                </Box>
            )}
        </Box>
      </Paper>
    </Box>
  );
}

export default App;

// import React, { useState } from 'react';
// import { Button, Input, MenuItem, FormControl, Select, Box, Typography, Paper } from '@mui/material';
// import axios from 'axios';

// function App() {
//   const [selectedFile, setSelectedFile] = useState(null);
//   const [selectedFilter, setSelectedFilter] = useState('');
//   const [imageSrc, setImageSrc] = useState('');

//   const handleFileChange = event => {
//     setSelectedFile(event.target.files[0]);
//   };

//   const handleFilterChange = event => {
//     setSelectedFilter(event.target.value);
//   };

//   const handleSubmit = async () => {
//     const formData = new FormData();
//     formData.append('image', selectedFile);
//     formData.append('filter', selectedFilter);

//     try {
//       const response = await axios.post('http://localhost:5000/upload', formData, {
//         headers: {
//           'Content-Type': 'multipart/form-data',
//         },
//       });

//       setImageSrc(`data:image/jpeg;base64,${response.data}`);
//     } catch (error) {
//       console.error('Error uploading image:', error);
//     }
//   };

//   return (
//     <Box sx={{
//       minHeight: '100vh',
//       backgroundImage: 'url("/background.png")',
//       backgroundSize: 'cover',
//       backgroundPosition: 'center',
//       display: 'flex',
//       alignItems: 'center',
//       justifyContent: 'center',
//     }}>
//       <Paper elevation={3} sx={{ p: 3, maxWidth: 600, width: '100%', margin: 2 }}>
//         <Typography variant="h4" gutterBottom textAlign="center">
//           Image Filter Application
//         </Typography>
//         <Input
//           type="file"
//           onChange={handleFileChange}
//           disableUnderline
//           fullWidth
//           inputProps={{ accept: 'image/*' }}
//           sx={{ mb: 2 }}
//         />
//         <FormControl fullWidth sx={{ mb: 2 }}>
//           <Select
//             value={selectedFilter}
//             onChange={handleFilterChange}
//             displayEmpty
//             inputProps={{ 'aria-label': 'Without label' }}
//           >
//             <MenuItem value="">
//               <em>None</em>
//             </MenuItem>
//             <MenuItem value="grayscale">Grayscale</MenuItem>
//             <MenuItem value="blur">Blur</MenuItem>
//             <MenuItem value="threshold">Threshold</MenuItem>
//             <MenuItem value="edge_detection">Edge Detection</MenuItem>
//             <MenuItem value="color_filter">Color Filter</MenuItem>
//           </Select>
//         </FormControl>
//         <Button variant="contained" onClick={handleSubmit} fullWidth sx={{ mb: 2 }}>
//           Apply Filter
//         </Button>
//         {imageSrc && (
//           <Box sx={{ mt: 2, textAlign: 'center' }}>
//             <img src={imageSrc} alt="Processed" style={{ maxWidth: '100%' }} />
//           </Box>
//         )}
//       </Paper>
//     </Box>
//   );
// }

// export default App;