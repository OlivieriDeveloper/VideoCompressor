# VideoCompressor

VideoCompressor is a desktop application for video file compression, developed in Python with PyQt5 graphical interface.

## Features

- **Intuitive Graphical Interface**: Easy to use with simple and clear controls
- **Video Compression**: Reduces video file sizes while maintaining good quality
- **Multi-Format Support**: Compatible with MP4, MOV, and MKV files
- **Folder Management**: Automatically saves compressed files in a "compressed" subfolder
- **Size Control**: Allows specifying the desired size for the compressed file
- **Real-time Feedback**: Shows compression status and notifies upon completion
- **Quick Access**: Button to directly open the compressed files folder

## System Requirements

- Windows 10 or later
- Python 3.7 or later
- FFmpeg (included in the package)
- PyQt5
- pymediainfo
- ffmpeg installed (or you can download the ffmpeg.exe and move into ``./ffmpeg/bin/ffmpeg.exe``)

## Installation

1. Clone the repository:

```bash
git clone https://github.com/tuonome/VideoCompressor.git
cd VideoCompressor
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

## Usage

1. Start the application:

```bash
python main.py
```

2. Select a video file using the "Select File" button
3. Adjust the desired size using the slider
4. Click "Compress" to start compression
5. Upon completion, you can open the compressed files folder directly from the application

## Project Structure

```
VideoCompressor/
├── main.py              # Main graphical interface
├── compressor.py        # Video compression logic
├── ffmpeg/             # Directory containing FFmpeg
│   └── bin/
│       └── ffmpeg.exe
└── requirements.txt     # Project dependencies
```

## License

This project is distributed under the terms of the [GNU GPLv3](LICENSE).

## Contributing

Contributions are welcome! To contribute:

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## Author

[Il Tuo Nome] - [Il Tuo Email]

## Acknowledgments

- FFmpeg for the video compression tool
- PyQt5 for the graphical interface
- pymediainfo for video file analysis
