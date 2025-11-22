import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
import os
import subprocess
import sys
import time
import re
import yt_dlp  # for PyInstaller hidden import

class M3U8ToMP4Converter:
    def __init__(self, root):
        self.root = root
        self.root.title("M3U8 to MP4 Converter")
        self.root.geometry("700x500")
        
        self.setup_ui()
        self.check_dependencies()
        
    def setup_ui(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Title
        title_label = ttk.Label(main_frame, text="M3U8 to MP4 Converter", 
                               font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # Input file selection
        ttk.Label(main_frame, text="Select TXT file with M3U8 links:").grid(row=1, column=0, sticky=tk.W, pady=5)
        
        self.file_path = tk.StringVar()
        file_entry = ttk.Entry(main_frame, textvariable=self.file_path, width=50)
        file_entry.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=5)
        
        browse_btn = ttk.Button(main_frame, text="Browse", command=self.browse_file)
        browse_btn.grid(row=2, column=1, padx=5, pady=5)
        
        # Output directory selection
        ttk.Label(main_frame, text="Output directory:").grid(row=3, column=0, sticky=tk.W, pady=5)
        
        self.output_dir = tk.StringVar()
        self.output_dir.set(os.path.expanduser("~/Downloads"))
        output_entry = ttk.Entry(main_frame, textvariable=self.output_dir, width=50)
        output_entry.grid(row=4, column=0, sticky=(tk.W, tk.E), pady=5)
        
        output_browse_btn = ttk.Button(main_frame, text="Browse", command=self.browse_output_dir)
        output_browse_btn.grid(row=4, column=1, padx=5, pady=5)
        
        # Settings frame
        settings_frame = ttk.LabelFrame(main_frame, text="Settings", padding="5")
        settings_frame.grid(row=5, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10)
        
        # Quality selection
        ttk.Label(settings_frame, text="Video Quality:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.quality = tk.StringVar(value="best")
        quality_combo = ttk.Combobox(settings_frame, textvariable=self.quality, 
                                   values=["best", "1080p", "720p", "480p", "360p", "worst"])
        quality_combo.grid(row=0, column=1, sticky=tk.W, pady=2, padx=(10, 20))
        
        # Timeout setting
        ttk.Label(settings_frame, text="Timeout (minutes):").grid(row=0, column=2, sticky=tk.W, pady=2)
        self.timeout = tk.StringVar(value="30")
        try:
            timeout_spin = ttk.Spinbox(settings_frame, from_=1, to=240, textvariable=self.timeout, width=8)
        except AttributeError:
            timeout_spin = tk.Spinbox(settings_frame, from_=1, to=240, textvariable=self.timeout, width=8)
        timeout_spin.grid(row=0, column=3, sticky=tk.W, pady=2, padx=(10, 0))

        # Retry attempts
        ttk.Label(settings_frame, text="Retry attempts:").grid(row=1, column=0, sticky=tk.W, pady=2)
        self.retries = tk.StringVar(value="3")
        try:
            retry_spin = ttk.Spinbox(settings_frame, from_=0, to=10, textvariable=self.retries, width=8)
        except AttributeError:
            retry_spin = tk.Spinbox(settings_frame, from_=0, to=10, textvariable=self.retries, width=8)
        retry_spin.grid(row=1, column=1, sticky=tk.W, pady=2, padx=(10, 20))
        
        # Convert button
        self.convert_btn = ttk.Button(main_frame, text="Convert M3U8 to MP4", 
                                     command=self.start_conversion)
        self.convert_btn.grid(row=6, column=0, columnspan=2, pady=20)
        
        # Progress bar
        self.progress = ttk.Progressbar(main_frame, mode='determinate')
        self.progress.grid(row=7, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        # Status label
        self.status_label = ttk.Label(main_frame, text="Ready")
        self.status_label.grid(row=8, column=0, columnspan=2, pady=5)
        
        # Log text area
        log_frame = ttk.LabelFrame(main_frame, text="Conversion Log", padding="5")
        log_frame.grid(row=9, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10)
        
        self.log_text = tk.Text(log_frame, height=12, width=80)
        scrollbar = ttk.Scrollbar(log_frame, orient="vertical", command=self.log_text.yview)
        self.log_text.configure(yscrollcommand=scrollbar.set)
        
        self.log_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(9, weight=1)
        
    def check_dependencies(self):
        """Check if yt-dlp is available"""
        try:
            subprocess.run([sys.executable, "-m", "yt_dlp", "--version"], 
                         capture_output=True, check=True)
            self.log("✓ yt-dlp is available")
            return True
        except:
            self.log("✗ yt-dlp not found. Please install with: pip install yt-dlp")
            self.convert_btn.config(state='disabled')
            return False
            
    def browse_file(self):
        filename = filedialog.askopenfilename(
            title="Select TXT file with M3U8 links",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if filename:
            self.file_path.set(filename)
            
    def browse_output_dir(self):
        directory = filedialog.askdirectory(title="Select output directory")
        if directory:
            self.output_dir.set(directory)
            
    def log(self, message):
        self.log_text.insert(tk.END, f"{message}\n")
        self.log_text.see(tk.END)
        self.root.update_idletasks()
        
    def update_status(self, message):
        self.status_label.config(text=message)
        self.root.update_idletasks()
        
    def start_conversion(self):
        if not self.file_path.get():
            messagebox.showerror("Error", "Please select a TXT file with M3U8 links")
            return
            
        if not os.path.exists(self.file_path.get()):
            messagebox.showerror("Error", "Selected file does not exist")
            return
            
        # Disable convert button during conversion
        self.convert_btn.config(state='disabled')
        
        # Start conversion in separate thread
        thread = threading.Thread(target=self.convert_files)
        thread.daemon = True
        thread.start()
        
    def parse_txt_file(self, file_path):
        """Parse the TXT file and extract name-url pairs"""
        entries = []
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                
            current_name = None
            for line in lines:
                line = line.strip()
                if not line:
                    continue
                    
                # Check if line contains a name (not a URL)
                if not line.startswith('http') and not line.startswith('#'):
                    current_name = line
                # Check if line contains a URL
                elif line.startswith('http'):
                    if current_name:
                        entries.append((current_name, line))
                        current_name = None
                    else:
                        # If no name provided, generate one from URL
                        name = self.generate_name_from_url(line, len(entries) + 1)
                        entries.append((name, line))
                        
        except Exception as e:
            self.log(f"Error parsing TXT file: {str(e)}")
            
        return entries
        
    def generate_name_from_url(self, url, index):
        """Generate a name from URL if no custom name is provided"""
        try:
            # Extract filename from URL
            match = re.search(r'/([^/]+)\.(m3u8|mpd)', url)
            if match:
                return match.group(1)
        except:
            pass
        return f"video_{index}"
        
    def sanitize_filename(self, filename):
        """Remove invalid characters from filename"""
        # Remove or replace invalid characters for Windows/Linux
        invalid_chars = '<>:"/\\|?*'
        for char in invalid_chars:
            filename = filename.replace(char, '_')
        return filename.strip()
        
    def convert_files(self):
        try:
            # Parse TXT file to get name-url pairs
            entries = self.parse_txt_file(self.file_path.get())
                
            if not entries:
                self.log("No valid M3U8 links found in the file")
                return
                
            total_links = len(entries)
            self.progress['maximum'] = total_links
            
            self.log(f"Found {total_links} M3U8 links to convert")
            self.log("Starting conversion using yt-dlp...")
            
            successful = 0
            failed = 0
            
            for i, (name, m3u8_url) in enumerate(entries, 1):
                self.update_status(f"Converting {i}/{total_links}")
                self.log(f"\n[{i}/{total_links}] Converting: {name}")
                self.log(f"  URL: {m3u8_url}")
                
                try:
                    max_retries = int(self.retries.get())
                    converted = False
                    
                    for attempt in range(max_retries + 1):
                        if attempt > 0:
                            self.log(f"  Retry attempt {attempt}/{max_retries}...")
                            time.sleep(2)  # Wait before retry
                            
                        if self.convert_with_ytdlp(name, m3u8_url, i):
                            successful += 1
                            converted = True
                            self.log(f"✓ Successfully converted: {name}")
                            break
                        else:
                            if attempt < max_retries:
                                self.log(f"  Waiting before next retry...")
                                time.sleep(5)
                    
                    if not converted:
                        failed += 1
                        self.log(f"✗ Failed to convert: {name} after {max_retries + 1} attempts")
                        
                except Exception as e:
                    failed += 1
                    self.log(f"✗ Error converting {name}: {str(e)}")
                    
                self.progress['value'] = i
                
            # Final status
            self.update_status(f"Completed: {successful} successful, {failed} failed")
            self.log(f"\n🎉 Conversion completed! Successful: {successful}, Failed: {failed}")
            
        except Exception as e:
            self.log(f"Error: {str(e)}")
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
        finally:
            # Re-enable convert button
            self.convert_btn.config(state='normal')
            self.progress['value'] = 0
            
    def convert_with_ytdlp(self, name, m3u8_url, index):
        """Convert M3U8 to MP4 using yt-dlp with custom filename"""
        try:
            # Create output directory if it doesn't exist
            os.makedirs(self.output_dir.get(), exist_ok=True)
            
            # Sanitize the filename
            safe_name = self.sanitize_filename(name)
            output_template = os.path.join(self.output_dir.get(), f"{safe_name}.%(ext)s")
            
            # Build yt-dlp command with optimized settings
            cmd = [
                sys.executable, "-m", "yt_dlp",
                "-o", output_template,
                "--format", f"best[height<={self.get_quality_height()}]/best",
                "--no-part",
                "--console-title",
                "--no-warnings",
                m3u8_url
            ]
            
            self.log(f"  Output: {safe_name}.mp4")
            
            # Calculate timeout in seconds
            timeout_seconds = int(self.timeout.get()) * 60
            
            # Run conversion
            process = subprocess.Popen(
                cmd, 
                stdout=subprocess.PIPE, 
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1,
                universal_newlines=True
            )
            
            # Read output in real-time
            start_time = time.time()
            while True:
                output = process.stdout.readline()
                if output == '' and process.poll() is not None:
                    break
                if output:
                    # Filter and show relevant output
                    clean_output = output.strip()
                    if clean_output and not clean_output.startswith('[debug]'):
                        self.log(f"    {clean_output}")
                
                # Check timeout
                if time.time() - start_time > timeout_seconds:
                    process.terminate()
                    self.log("  ⏰ Process terminated due to timeout")
                    return False
                    
                time.sleep(0.1)
            
            # Check return code
            return_code = process.poll()
            if return_code == 0:
                return True
            else:
                stderr_output = process.stderr.read()
                if stderr_output:
                    error_lines = stderr_output.strip().split('\n')
                    for line in error_lines:
                        if line and not line.startswith('[debug]'):
                            self.log(f"    {line}")
                return False
                
        except subprocess.TimeoutExpired:
            self.log("  ⏰ Conversion timeout")
            return False
        except Exception as e:
            self.log(f"  ✗ Unexpected error: {str(e)}")
            return False
            
    def get_quality_height(self):
        """Get maximum height for selected quality"""
        quality_map = {
            "best": "9999",
            "1080p": "1080",
            "720p": "720", 
            "480p": "480",
            "360p": "360",
            "worst": "144"
        }
        return quality_map.get(self.quality.get(), "9999")

def main():
    root = tk.Tk()
    app = M3U8ToMP4Converter(root)
    root.mainloop()

if __name__ == "__main__":
    main()
