#!/usr/bin/env python3
"""
PDF Generator for Web Pages
Reads URLs from ss.txt and converts them to PDFs
"""

import os
import re
import requests
from urllib.parse import urlparse, urljoin
from pathlib import Path
import weasyprint
from bs4 import BeautifulSoup
import time

class WebPageToPDF:
    def __init__(self, input_file='ss.txt', output_dir='pdfs'):
        self.input_file = input_file
        self.output_dir = Path(output_dir)
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Linux; x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        
    def create_output_directory(self):
        """Create the output directory if it doesn't exist"""
        self.output_dir.mkdir(exist_ok=True)
        print(f"Output directory: {self.output_dir.absolute()}")
    
    def read_urls(self):
        """Read URLs from the input file"""
        if not os.path.exists(self.input_file):
            print(f"Error: {self.input_file} not found!")
            return []
        
        with open(self.input_file, 'r', encoding='utf-8') as f:
            urls = [line.strip() for line in f if line.strip()]
        
        print(f"Found {len(urls)} URLs to process")
        return urls
    
    def sanitize_filename(self, filename):
        """Remove invalid characters from filename"""
        # Remove or replace invalid characters
        filename = re.sub(r'[<>:"/\\|?*]', '_', filename)
        # Remove extra spaces and limit length
        filename = re.sub(r'\s+', ' ', filename).strip()
        return filename[:200]  # Limit filename length
    
    def extract_slug_from_url(self, url):
        """Extract a meaningful slug from the URL"""
        parsed = urlparse(url)
        
        # Get the path and remove leading/trailing slashes
        path = parsed.path.strip('/')
        
        # If no path, use the domain
        if not path or path == '':
            slug = 'homepage'
        else:
            # Take the last part of the path as slug
            slug = path.split('/')[-1]
            
            # If it's empty or has extension, use the full path
            if not slug or '.' in slug:
                slug = path.replace('/', '-')
        
        # Clean up the slug
        slug = re.sub(r'[^\w\-_]', '-', slug)
        slug = re.sub(r'-+', '-', slug).strip('-')
        
        return slug if slug else 'page'
    
    def get_domain_from_url(self, url):
        """Extract domain from URL"""
        parsed = urlparse(url)
        return parsed.netloc
    
    def fetch_webpage_content(self, url):
        """Fetch and clean webpage content"""
        try:
            print(f"Fetching: {url}")
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            
            # Parse HTML and clean it up
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Remove script and style elements
            for script in soup(["script", "style"]):
                script.decompose()
            
            # Convert relative URLs to absolute URLs
            for tag in soup.find_all(['img', 'link', 'a']):
                for attr in ['src', 'href']:
                    if tag.get(attr):
                        tag[attr] = urljoin(url, tag[attr])
            
            return str(soup)
            
        except requests.RequestException as e:
            print(f"Error fetching {url}: {e}")
            return None
    
    def generate_pdf(self, html_content, output_path):
        """Generate PDF from HTML content"""
        try:
            # Create CSS for better PDF formatting
            css_string = """
            @page {
                margin: 1in;
                size: A4;
            }
            body {
                font-family: Arial, sans-serif;
                line-height: 1.6;
                color: #333;
            }
            img {
                max-width: 100% !important;
                height: auto !important;
            }
            """
            
            # Generate PDF
            html_doc = weasyprint.HTML(string=html_content)
            css_doc = weasyprint.CSS(string=css_string)
            
            html_doc.write_pdf(output_path, stylesheets=[css_doc])
            print(f"✓ PDF saved: {output_path}")
            return True
            
        except Exception as e:
            print(f"Error generating PDF: {e}")
            return False
    
    def process_url(self, url):
        """Process a single URL"""
        # Ensure URL has protocol
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        
        # Get domain and slug
        domain = self.get_domain_from_url(url)
        slug = self.extract_slug_from_url(url)
        
        # Create filename: [domain] slug.pdf
        filename = f"[{domain}] {slug}.pdf"
        filename = self.sanitize_filename(filename)
        output_path = self.output_dir / filename
        
        # Skip if file already exists
        if output_path.exists():
            print(f"⚠ Skipping {url} - PDF already exists")
            return True
        
        # Fetch content
        html_content = self.fetch_webpage_content(url)
        if not html_content:
            return False
        
        # Generate PDF
        return self.generate_pdf(html_content, output_path)
    
    def run(self):
        """Main execution function"""
        print("🚀 Starting PDF generation process...")
        
        # Create output directory
        self.create_output_directory()
        
        # Read URLs
        urls = self.read_urls()
        if not urls:
            print("No URLs to process!")
            return
        
        # Process each URL
        successful = 0
        failed = 0
        
        for i, url in enumerate(urls, 1):
            print(f"\n[{i}/{len(urls)}] Processing: {url}")
            
            if self.process_url(url):
                successful += 1
            else:
                failed += 1
            
            # Small delay to be respectful to servers
            time.sleep(1)
        
        print(f"\n✅ Process completed!")
        print(f"   Successful: {successful}")
        print(f"   Failed: {failed}")
        print(f"   PDFs saved in: {self.output_dir.absolute()}")

if __name__ == "__main__":
    generator = WebPageToPDF()
    generator.run()