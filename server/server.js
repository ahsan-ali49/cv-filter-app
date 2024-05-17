const express = require('express');
const multer = require('multer');
const { spawn } = require('child_process');
// const cors = require('cors');
const path = require('path');
const fs = require('fs');

const app = express();
const port = 5000;

const cors = require('cors');
app.use(cors());

app.use(express.static('public'));

const storage = multer.diskStorage({
  destination: function (req, file, cb) {
    cb(null, 'uploads/');
  },
  filename: function (req, file, cb) {
    cb(null, Date.now() + path.extname(file.originalname)); //Appending extension
  }
});

const upload = multer({ storage: storage });

app.post('/upload', upload.single('image'), (req, res) => {
    console.log("Received file:", req.file);
    console.log("Selected filter:", req.body.filter);
  const filter = req.body.filter;
  const pythonProcess = spawn('python', ["apply_filter.py", req.file.path, filter]);

  pythonProcess.stdout.on('data', (data) => {
    // Assuming the Python script returns the path to the processed image
    const imagePath = data.toString().trim();

    // Send the image as a base64 encoded string
    fs.readFile(imagePath, (err, imageData) => {
      if (err) {
        res.status(500).send("Failed to read processed image.");
        return;
      }

      res.send(Buffer.from(imageData).toString('base64'));
      fs.unlink(req.file.path, (err) => { if (err) console.log(err); }); // Delete the original file
      fs.unlink(imagePath, (err) => { if (err) console.log(err); }); // Delete the processed file
    });
  });

  pythonProcess.stderr.on('data', (data) => {
    console.error(`stderr: ${data}`);
  });

  pythonProcess.on('close', (code) => {
    console.log(`child process exited with code ${code}`);
  });
});

app.listen(port, () => {
  console.log(`Server running on port ${port}`);
});
