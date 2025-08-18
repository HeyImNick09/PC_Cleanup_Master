"""
Professional GUI Interface for PC Cleanup & Optimization Tool
Modern, customizable interface suitable for business deployment

Features:
- Real-time progress tracking
- Professional branding capabilities
- Customizable themes and colors
- Enterprise-ready reporting
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, filedialog
import threading
import queue
import os
import sys
from pathlib import Path
from datetime import datetime
import json
import webbrowser

# Import our main cleanup modules
from main import PCCleanupTool

class ModernPCCleanupGUI:
    """
    Professional GUI for PC Cleanup Tool with customizable branding
    """
    
    def __init__(self):
        self.root = tk.Tk()
        self.cleanup_tool = None
        self.cleanup_thread = None
        self.progress_queue = queue.Queue()
        
        # Customizable branding settings
        self.branding = {
            'title': "Nick's PC Optimization Suite",
            'subtitle': "Professional System Maintenance Tool",
            'company': "Nick P - IT Solutions",
            'website': "https://your-website.com",
            'support_email': "support@your-domain.com",
            'version': "1.0.0"
        }
        
        # Professional color scheme (easily customizable)
        self.colors = {
            'primary': '#2E86AB',      # Professional blue
            'secondary': '#A23B72',    # Accent purple
            'success': '#F18F01',      # Success orange
            'background': '#F5F5F5',   # Light gray background
            'card_bg': '#FFFFFF',      # White cards
            'text_primary': '#2C3E50', # Dark blue-gray text
            'text_secondary': '#7F8C8D' # Light gray text
        }
        
        self.setup_gui()
        self.setup_styles()
        
    def setup_gui(self):
        """Initialize the main GUI structure"""
        self.root.title(f"{self.branding['title']} v{self.branding['version']}")
        self.root.geometry("900x700")
        self.root.configure(bg=self.colors['background'])
        
        # Make window resizable but set minimum size
        self.root.minsize(800, 600)
        
        # Create main container with padding
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights for responsive design
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(2, weight=1)
        
        self.create_header(main_frame)
        self.create_control_panel(main_frame)
        self.create_progress_area(main_frame)
        self.create_status_bar(main_frame)
        
    def setup_styles(self):
        """Configure custom styles for professional appearance"""
        style = ttk.Style()
        
        # Configure custom button styles
        style.configure(
            'Primary.TButton',
            font=('Segoe UI', 10, 'bold'),
            padding=(20, 10)
        )
        
        style.configure(
            'Secondary.TButton',
            font=('Segoe UI', 9),
            padding=(15, 8)
        )
        
        # Configure label styles
        style.configure(
            'Title.TLabel',
            font=('Segoe UI', 16, 'bold'),
            foreground=self.colors['primary']
        )
        
        style.configure(
            'Subtitle.TLabel',
            font=('Segoe UI', 10),
            foreground=self.colors['text_secondary']
        )
        
        style.configure(
            'Header.TLabel',
            font=('Segoe UI', 12, 'bold'),
            foreground=self.colors['text_primary']
        )
        
    def create_header(self, parent):
        """Create professional header with branding"""
        header_frame = ttk.Frame(parent)
        header_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 20))
        header_frame.columnconfigure(0, weight=1)
        
        # Main title
        title_label = ttk.Label(
            header_frame, 
            text=self.branding['title'],
            style='Title.TLabel'
        )
        title_label.grid(row=0, column=0, sticky=tk.W)
        
        # Subtitle
        subtitle_label = ttk.Label(
            header_frame,
            text=self.branding['subtitle'],
            style='Subtitle.TLabel'
        )
        subtitle_label.grid(row=1, column=0, sticky=tk.W)
        
        # Company info
        company_label = ttk.Label(
            header_frame,
            text=f"© {datetime.now().year} {self.branding['company']}",
            style='Subtitle.TLabel'
        )
        company_label.grid(row=2, column=0, sticky=tk.W, pady=(5, 0))
        
    def create_control_panel(self, parent):
        """Create main control panel with action buttons"""
        control_frame = ttk.LabelFrame(parent, text="System Maintenance", padding="15")
        control_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N), padx=(0, 10))
        
        # Quick Actions
        ttk.Label(control_frame, text="Quick Actions", style='Header.TLabel').grid(
            row=0, column=0, columnspan=2, sticky=tk.W, pady=(0, 10)
        )
        
        # Main cleanup button
        self.cleanup_btn = ttk.Button(
            control_frame,
            text="🚀 Run Full Cleanup",
            command=self.start_cleanup,
            style='Primary.TButton'
        )
        self.cleanup_btn.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        # Individual action buttons
        ttk.Button(
            control_frame,
            text="🗂️ Clean Temp Files Only",
            command=self.clean_temp_only,
            style='Secondary.TButton'
        ).grid(row=2, column=0, sticky=(tk.W, tk.E), padx=(0, 5), pady=2)
        
        ttk.Button(
            control_frame,
            text="🌐 Clean Browser Cache",
            command=self.clean_browsers_only,
            style='Secondary.TButton'
        ).grid(row=2, column=1, sticky=(tk.W, tk.E), padx=(5, 0), pady=2)
        
        ttk.Button(
            control_frame,
            text="🔄 Check Windows Updates",
            command=self.check_updates_only,
            style='Secondary.TButton'
        ).grid(row=3, column=0, sticky=(tk.W, tk.E), padx=(0, 5), pady=2)
        
        ttk.Button(
            control_frame,
            text="📊 System Analysis",
            command=self.system_analysis,
            style='Secondary.TButton'
        ).grid(row=3, column=1, sticky=(tk.W, tk.E), padx=(5, 0), pady=2)
        
        # Configure column weights
        control_frame.columnconfigure(0, weight=1)
        control_frame.columnconfigure(1, weight=1)
        
    def create_progress_area(self, parent):
        """Create progress monitoring area"""
        progress_frame = ttk.LabelFrame(parent, text="Operation Progress", padding="15")
        progress_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(10, 0))
        progress_frame.columnconfigure(0, weight=1)
        progress_frame.rowconfigure(1, weight=1)
        
        # Progress bar
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(
            progress_frame,
            variable=self.progress_var,
            maximum=100,
            mode='determinate'
        )
        self.progress_bar.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Log output area
        self.log_text = scrolledtext.ScrolledText(
            progress_frame,
            height=15,
            font=('Consolas', 9),
            wrap=tk.WORD
        )
        self.log_text.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Action buttons for progress area
        button_frame = ttk.Frame(progress_frame)
        button_frame.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=(10, 0))
        
        ttk.Button(
            button_frame,
            text="📋 View Report",
            command=self.view_last_report
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Button(
            button_frame,
            text="📁 Open Log Folder",
            command=self.open_log_folder
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Button(
            button_frame,
            text="🗑️ Clear Log",
            command=self.clear_log
        ).pack(side=tk.LEFT)
        
    def create_status_bar(self, parent):
        """Create status bar with system info"""
        status_frame = ttk.Frame(parent)
        status_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(10, 0))
        status_frame.columnconfigure(1, weight=1)
        
        # Status label
        self.status_var = tk.StringVar(value="Ready")
        status_label = ttk.Label(status_frame, textvariable=self.status_var)
        status_label.grid(row=0, column=0, sticky=tk.W)
        
        # System info
        system_info = f"System: {os.environ.get('COMPUTERNAME', 'Unknown')} | User: {os.environ.get('USERNAME', 'Unknown')}"
        ttk.Label(status_frame, text=system_info, style='Subtitle.TLabel').grid(
            row=0, column=1, sticky=tk.E
        )
        
    def log_message(self, message, level="INFO"):
        """Add message to log area with timestamp"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        formatted_message = f"[{timestamp}] {level}: {message}\n"
        
        self.log_text.insert(tk.END, formatted_message)
        self.log_text.see(tk.END)
        
        # Color coding for different log levels
        if level == "ERROR":
            # Add red color for errors (would need text tags for full implementation)
            pass
        elif level == "SUCCESS":
            # Add green color for success messages
            pass
            
    def update_progress(self, value, message=""):
        """Update progress bar and status"""
        self.progress_var.set(value)
        if message:
            self.status_var.set(message)
            self.log_message(message)
            
    def start_cleanup(self):
        """Start full cleanup in background thread"""
        if self.cleanup_thread and self.cleanup_thread.is_alive():
            messagebox.showwarning("Operation in Progress", "A cleanup operation is already running.")
            return
            
        self.cleanup_btn.configure(state='disabled', text="🔄 Cleaning...")
        self.log_message("Starting full PC cleanup...", "INFO")
        self.update_progress(0, "Initializing cleanup...")
        
        # Start cleanup in background thread
        self.cleanup_thread = threading.Thread(target=self._run_cleanup, daemon=True)
        self.cleanup_thread.start()
        
        # Start progress monitoring
        self.monitor_progress()
        
    def _run_cleanup(self):
        """Run cleanup in background thread"""
        try:
            self.cleanup_tool = PCCleanupTool()
            
            # Simulate progress updates (in real implementation, modify PCCleanupTool to support progress callbacks)
            self.progress_queue.put((10, "Cleaning temporary files..."))
            
            # Run the actual cleanup
            results = self.cleanup_tool.run_full_cleanup()
            
            self.progress_queue.put((100, "Cleanup completed successfully!"))
            self.progress_queue.put(("COMPLETE", results))
            
        except Exception as e:
            self.progress_queue.put(("ERROR", str(e)))
            
    def monitor_progress(self):
        """Monitor progress queue and update UI"""
        try:
            while True:
                item = self.progress_queue.get_nowait()
                
                if isinstance(item[0], (int, float)):
                    # Progress update
                    self.update_progress(item[0], item[1])
                elif item[0] == "COMPLETE":
                    # Cleanup completed
                    results = item[1]
                    self.cleanup_completed(results)
                    return
                elif item[0] == "ERROR":
                    # Error occurred
                    self.cleanup_error(item[1])
                    return
                    
        except queue.Empty:
            # Continue monitoring
            self.root.after(100, self.monitor_progress)
            
    def cleanup_completed(self, results):
        """Handle cleanup completion"""
        self.cleanup_btn.configure(state='normal', text="🚀 Run Full Cleanup")
        
        summary = results.get('summary', {})
        files_deleted = summary.get('total_files_deleted', 0)
        space_freed = summary.get('total_size_freed_mb', 0)
        
        success_msg = f"Cleanup completed successfully!\n\nFiles deleted: {files_deleted}\nSpace freed: {space_freed:.2f} MB"
        
        self.log_message(success_msg, "SUCCESS")
        messagebox.showinfo("Cleanup Complete", success_msg)
        
    def cleanup_error(self, error_msg):
        """Handle cleanup error"""
        self.cleanup_btn.configure(state='normal', text="🚀 Run Full Cleanup")
        self.log_message(f"Cleanup failed: {error_msg}", "ERROR")
        messagebox.showerror("Cleanup Error", f"An error occurred during cleanup:\n\n{error_msg}")
        
    def clean_temp_only(self):
        """Clean temporary files only"""
        self.log_message("Starting temporary file cleanup...", "INFO")
        # Implement temp-only cleanup
        
    def clean_browsers_only(self):
        """Clean browser caches only"""
        self.log_message("Starting browser cache cleanup...", "INFO")
        # Implement browser-only cleanup
        
    def check_updates_only(self):
        """Check Windows updates only"""
        self.log_message("Checking Windows updates...", "INFO")
        # Implement update check only
        
    def system_analysis(self):
        """Run system analysis"""
        self.log_message("Running system analysis...", "INFO")
        # Implement system analysis
        
    def view_last_report(self):
        """Open the most recent cleanup report"""
        desktop_path = Path.home() / "Desktop"
        if desktop_path.exists():
            reports = list(desktop_path.glob("PC_Cleanup_Report_*.txt"))
            if reports:
                latest_report = max(reports, key=lambda p: p.stat().st_mtime)
                os.startfile(latest_report)
            else:
                messagebox.showinfo("No Reports", "No cleanup reports found.")
        
    def open_log_folder(self):
        """Open the log folder"""
        desktop_path = Path.home() / "Desktop"
        log_dir = desktop_path / "PC_Cleanup_Logs" if desktop_path.exists() else Path.home() / "PC_Cleanup_Logs"
        
        if log_dir.exists():
            os.startfile(log_dir)
        else:
            messagebox.showinfo("No Logs", "Log folder not found.")
            
    def clear_log(self):
        """Clear the log display"""
        self.log_text.delete(1.0, tk.END)
        self.log_message("Log cleared", "INFO")
        
    def run(self):
        """Start the GUI application"""
        # Add window icon if available
        try:
            # You can add a custom icon here
            # self.root.iconbitmap('icon.ico')
            pass
        except:
            pass
            
        # Center window on screen
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
        
        self.log_message("PC Cleanup Tool initialized", "INFO")
        self.log_message(f"Version: {self.branding['version']}", "INFO")
        self.log_message("Ready for operation", "INFO")
        
        # Start the GUI main loop
        self.root.mainloop()


def main():
    """Main entry point for GUI application"""
    try:
        app = ModernPCCleanupGUI()
        app.run()
    except Exception as e:
        messagebox.showerror("Application Error", f"Failed to start application:\n\n{str(e)}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
