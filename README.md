# PDF Generator for Web Pages

A Python application that reads URLs from a text file and converts the web pages to PDF files.

## Features

- Reads URLs from `ss.txt` (one URL per line)
- Converts web pages to PDF format
- Automatically creates a `pdfs` folder for output
- Names PDFs with format: `[domain] slug.pdf`
- Handles relative URLs by converting them to absolute
- Cleans HTML content for better PDF generation
- Includes proper error handling and progress tracking

## Installation

1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

Note: WeasyPrint requires some system dependencies. On Ubuntu/Debian:
```bash
sudo apt-get install python3-dev python3-pip python3-cffi python3-brotli libpango-1.0-0 libharfbuzz0b libpangoft2-1.0-0
```

## Usage

1. Create or edit `ss.txt` with your URLs (one per line):
```
https://www.google.com
https://www.github.com
https://stackoverflow.com/questions/tagged/python
```

2. Run the application:
```bash
python pdf_generator.py
```

3. PDFs will be saved in the `pdfs` folder with names like:
- `[www.google.com] homepage.pdf`
- `[www.github.com] homepage.pdf`
- `[stackoverflow.com] questions-tagged-python.pdf`

## File Structure

```
├── pdf_generator.py    # Main application
├── requirements.txt    # Python dependencies
├── ss.txt             # Input file with URLs
└── pdfs/              # Output folder (created automatically)
    ├── [domain1] slug1.pdf
    ├── [domain2] slug2.pdf
    └── ...
```

## Features Details

- **Smart Slug Generation**: Extracts meaningful names from URLs
- **Domain Prefixing**: Each PDF is prefixed with `[domain]` as requested
- **Duplicate Prevention**: Skips URLs if PDF already exists
- **Error Handling**: Continues processing even if some URLs fail
- **Progress Tracking**: Shows current progress and final statistics
- **Respectful Crawling**: Includes delays between requests

## Example Output

For URL `https://docs.python.org/3/tutorial/introduction.html`, the output would be:
`[docs.python.org] introduction.pdf`