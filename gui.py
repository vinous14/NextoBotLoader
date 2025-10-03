#!/usr/bin/env python3
"""
Nex        self.setup_logging()
        
        self.create_widgets()I
A modern graphical user interface for the Nexto bot loader.
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, filedialog
import threading
import queue
import sys
import os
import time
from pathlib import Path
import logging

from loader import NextoBotLoader

class LogHandler(logging.Handler):
    """Custom logging handler to redirect logs to GUI"""
    def __init__(self, log_queue):
        super().__init__()
        self.log_queue = log_queue
    
    def emit(self, record):
        self.log_queue.put(self.format(record))

class NextoBotGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🚀 Nexto Bot Loader")
        self.root.geometry("800x700")
        self.root.resizable(True, True)
        
        # Configure style
        self.setup_styles()
        
        self.loader = None
        self.loader_thread = None
        self.is_running = False
        self.log_queue = queue.Queue()
        
        # Setup logging
        self.setup_logging()
        
        self.create_widgets()
        
        # Start log checking
        self.check_log_queue()
        
        # Load initial configuration
        self.load_initial_config()
    
    def setup_styles(self):
        """Configure GUI styling"""
        style = ttk.Style()
        
        self.colors = {
            'primary': '#2E86C1',
            'secondary': '#28B463', 
            'warning': '#F39C12',
            'danger': '#E74C3C',
            'dark': '#2C3E50',
            'light': '#ECF0F1'
        }
        
        style.configure('Title.TLabel', font=('Arial', 16, 'bold'))
        style.configure('Heading.TLabel', font=('Arial', 12, 'bold'))
        style.configure('Success.TLabel', foreground=self.colors['secondary'])
        style.configure('Warning.TLabel', foreground=self.colors['warning'])
        style.configure('Danger.TLabel', foreground=self.colors['danger'])
    
    def setup_logging(self):
        """Setup logging to capture loader output"""
        self.log_handler = LogHandler(self.log_queue)
        self.log_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
        
        logging.getLogger().addHandler(self.log_handler)
        logging.getLogger().setLevel(logging.INFO)
    
    def create_widgets(self):
        """Create all GUI widgets"""
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        title_label = ttk.Label(main_frame, text="🚀 Nexto Bot Loader", style='Title.TLabel')
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        self.create_config_section(main_frame, row=1)
        self.create_status_section(main_frame, row=2)
        self.create_control_section(main_frame, row=3)
        self.create_log_section(main_frame, row=4)
        
        self.progress = ttk.Progressbar(main_frame, mode='indeterminate')
        self.progress.grid(row=5, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(10, 0))
    
    def create_config_section(self, parent, row):
        """Create configuration section"""
        # Configuration frame
        config_frame = ttk.LabelFrame(parent, text="⚙️ Configuration", padding="15")
        config_frame.grid(row=row, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 15))
        config_frame.columnconfigure(1, weight=1)
        
        # Bot path
        ttk.Label(config_frame, text="Bot Path:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.bot_path_var = tk.StringVar(value=str(Path.cwd()))
        bot_path_frame = ttk.Frame(config_frame)
        bot_path_frame.grid(row=0, column=1, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        bot_path_frame.columnconfigure(0, weight=1)
        
        self.bot_path_entry = ttk.Entry(bot_path_frame, textvariable=self.bot_path_var)
        self.bot_path_entry.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 10))
        
        browse_btn = ttk.Button(bot_path_frame, text="Browse", command=self.browse_bot_path)
        browse_btn.grid(row=0, column=1)
        
        # Team selection
        ttk.Label(config_frame, text="Team:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.team_var = tk.StringVar(value="Blue (0)")
        team_combo = ttk.Combobox(config_frame, textvariable=self.team_var, 
                                 values=["Blue (0)", "Orange (1)"], state="readonly", width=15)
        team_combo.grid(row=1, column=1, sticky=tk.W, pady=5)
        
        # Options
        options_frame = ttk.Frame(config_frame)
        options_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)
        
        self.wait_rl_var = tk.BooleanVar(value=True)
        wait_check = ttk.Checkbutton(options_frame, text="Wait for Rocket League", 
                                   variable=self.wait_rl_var)
        wait_check.grid(row=0, column=0, sticky=tk.W, padx=(0, 20))
        
        self.use_gui_var = tk.BooleanVar(value=False)
        gui_check = ttk.Checkbutton(options_frame, text="Use RLBot GUI", 
                                  variable=self.use_gui_var)
        gui_check.grid(row=0, column=1, sticky=tk.W, padx=(0, 20))
        
        self.auto_install_var = tk.BooleanVar(value=True)
        install_check = ttk.Checkbutton(options_frame, text="Auto-install dependencies", 
                                      variable=self.auto_install_var)
        install_check.grid(row=0, column=2, sticky=tk.W)
        
        # Second row of options
        options_frame2 = ttk.Frame(config_frame)
        options_frame2.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(5, 0))
        
        self.online_mode_var = tk.BooleanVar(value=False)
        online_check = ttk.Checkbutton(options_frame2, text="🌐 Online Mode (attach to existing matches)", 
                                     variable=self.online_mode_var, 
                                     command=self.on_online_mode_changed)
        online_check.grid(row=0, column=0, sticky=tk.W)
        
        # Online mode info label
        self.online_info = ttk.Label(options_frame2, 
                                   text="ℹ️ Only works with custom/private matches that allow bots",
                                   font=('Arial', 8), foreground='gray')
        self.online_info.grid(row=1, column=0, sticky=tk.W, pady=(2, 0))
    
    def create_status_section(self, parent, row):
        """Create status section"""
        status_frame = ttk.LabelFrame(parent, text="📊 Status", padding="15")
        status_frame.grid(row=row, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 15))
        status_frame.columnconfigure(1, weight=1)
        
        # Status indicators
        ttk.Label(status_frame, text="Dependencies:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.deps_status = ttk.Label(status_frame, text="⏳ Checking...", style='Warning.TLabel')
        self.deps_status.grid(row=0, column=1, sticky=tk.W, pady=2)
        
        ttk.Label(status_frame, text="Rocket League:").grid(row=1, column=0, sticky=tk.W, pady=2)
        self.rl_status = ttk.Label(status_frame, text="⏳ Checking...", style='Warning.TLabel')
        self.rl_status.grid(row=1, column=1, sticky=tk.W, pady=2)
        
        ttk.Label(status_frame, text="Bot Status:").grid(row=2, column=0, sticky=tk.W, pady=2)
        self.bot_status = ttk.Label(status_frame, text="⏹️ Stopped", style='Danger.TLabel')
        self.bot_status.grid(row=2, column=1, sticky=tk.W, pady=2)
        
        # Refresh button
        refresh_btn = ttk.Button(status_frame, text="🔄 Refresh", command=self.refresh_status)
        refresh_btn.grid(row=0, column=2, rowspan=3, padx=(20, 0))
    
    def on_online_mode_changed(self):
        """Handle online mode checkbox changes"""
        if self.online_mode_var.get():
            # Show warning for online mode
            response = messagebox.askokcancel(
                "Online Mode Warning",
                "🌐 Online Mode enables the bot to join online matches.\n\n"
                "⚠️ IMPORTANT NOTES:\n"
                "• Only works with CUSTOM/PRIVATE matches\n"
                "• Does NOT work with ranked/casual matchmaking\n"
                "• Host must allow bots in match settings\n"
                "• May not work in all online game modes\n\n"
                "Continue with online mode?"
            )
            if not response:
                self.online_mode_var.set(False)
    
    def create_control_section(self, parent, row):
        """Create control buttons section"""
        control_frame = ttk.Frame(parent)
        control_frame.grid(row=row, column=0, columnspan=3, pady=(0, 15))
        
        # Main control buttons
        self.start_btn = ttk.Button(control_frame, text="🚀 Start Bot", 
                                   command=self.start_bot, style='Success.TButton')
        self.start_btn.grid(row=0, column=0, padx=(0, 10))
        
        self.stop_btn = ttk.Button(control_frame, text="⏹️ Stop Bot", 
                                  command=self.stop_bot, state='disabled')
        self.stop_btn.grid(row=0, column=1, padx=(0, 10))
        
        # Utility buttons
        self.setup_btn = ttk.Button(control_frame, text="🔧 Setup & Verify", 
                                   command=self.run_setup)
        self.setup_btn.grid(row=0, column=2, padx=(0, 10))
        
        self.help_btn = ttk.Button(control_frame, text="❓ Help", 
                                  command=self.show_help)
        self.help_btn.grid(row=0, column=3)
    
    def create_log_section(self, parent, row):
        """Create log output section"""
        log_frame = ttk.LabelFrame(parent, text="📝 Log Output", padding="10")
        log_frame.grid(row=row, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 15))
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)
        
        # Configure main frame row weight for log expansion
        parent.rowconfigure(row, weight=1)
        
        # Log text area with scrollbar
        self.log_text = scrolledtext.ScrolledText(log_frame, height=15, width=80, 
                                                 wrap=tk.WORD, state='disabled')
        self.log_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Log control buttons
        log_controls = ttk.Frame(log_frame)
        log_controls.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(10, 0))
        
        clear_btn = ttk.Button(log_controls, text="🗑️ Clear Log", command=self.clear_log)
        clear_btn.grid(row=0, column=0)
        
        save_btn = ttk.Button(log_controls, text="💾 Save Log", command=self.save_log)
        save_btn.grid(row=0, column=1, padx=(10, 0))
    
    def browse_bot_path(self):
        """Browse for bot directory"""
        directory = filedialog.askdirectory(initialdir=self.bot_path_var.get())
        if directory:
            self.bot_path_var.set(directory)
            self.refresh_status()
    
    def load_initial_config(self):
        """Load initial configuration and status"""
        self.root.after(500, self.refresh_status)  # Delay to allow GUI to render
    
    def refresh_status(self):
        """Refresh all status indicators"""
        def check_status():
            try:
                # Initialize loader with current path
                bot_path = self.bot_path_var.get()
                temp_loader = NextoBotLoader(bot_path=bot_path)
                
                # Check dependencies
                deps_ok = temp_loader.check_dependencies(auto_install=False)
                self.root.after(0, self.update_deps_status, deps_ok)
                
                # Check Rocket League
                rl_running = temp_loader.is_rocket_league_running()
                self.root.after(0, self.update_rl_status, rl_running)
                
            except Exception as e:
                self.root.after(0, self.log_message, f"Status check error: {e}")
        
        # Run in background thread
        threading.Thread(target=check_status, daemon=True).start()
    
    def update_deps_status(self, deps_ok):
        """Update dependency status"""
        if deps_ok:
            self.deps_status.config(text="✅ Ready", style='Success.TLabel')
        else:
            self.deps_status.config(text="❌ Missing", style='Danger.TLabel')
    
    def update_rl_status(self, rl_running):
        """Update Rocket League status"""
        if rl_running:
            self.rl_status.config(text="✅ Running", style='Success.TLabel')
        else:
            self.rl_status.config(text="❌ Not Found", style='Danger.TLabel')
    
    def start_bot(self):
        """Start the bot in a background thread"""
        if self.is_running:
            return
        
        # Validate configuration
        bot_path = self.bot_path_var.get()
        if not Path(bot_path).exists():
            messagebox.showerror("Error", "Bot path does not exist!")
            return
        
        # Update UI state
        self.is_running = True
        self.start_btn.config(state='disabled')
        self.stop_btn.config(state='normal')
        self.bot_status.config(text="🚀 Starting...", style='Warning.TLabel')
        self.progress.start()
        
        # Clear log
        self.clear_log()
        
        # Start loader thread
        self.loader_thread = threading.Thread(target=self.run_loader, daemon=True)
        self.loader_thread.start()
    
    def run_loader(self):
        """Run the bot loader in background thread"""
        try:
            # Get configuration
            bot_path = self.bot_path_var.get()
            team = 0 if "Blue" in self.team_var.get() else 1
            wait_for_rl = self.wait_rl_var.get()
            use_gui = self.use_gui_var.get()
            auto_install = self.auto_install_var.get()
            online_mode = self.online_mode_var.get()
            
            # Create loader
            self.loader = NextoBotLoader(bot_path=bot_path)
            self.loader.bot_config['team'] = team
            
            # Update status
            mode_text = "🌐 Online" if online_mode else "🏠 Exhibition"
            self.root.after(0, self.bot_status.config, 
                          {"text": f"🔍 Checking ({mode_text})...", "style": "Warning.TLabel"})
            
            # Check dependencies
            if not self.loader.check_dependencies(auto_install=auto_install):
                self.root.after(0, self.loader_failed, "Dependency check failed")
                return
            
            # Wait for Rocket League if needed
            if wait_for_rl and not self.loader.is_rocket_league_running():
                self.root.after(0, self.bot_status.config, 
                              {"text": "⏳ Waiting for RL...", "style": "Warning.TLabel"})
                
                if not self.loader.wait_for_rocket_league():
                    self.root.after(0, self.loader_failed, "Rocket League not found")
                    return
            
            # Inject bot
            inject_text = f"💉 Injecting ({mode_text})..."
            self.root.after(0, self.bot_status.config, 
                          {"text": inject_text, "style": "Warning.TLabel"})
            
            success = False
            if use_gui:
                success = self.loader.inject_via_rlbot_gui(online_mode=online_mode)
            else:
                success = self.loader.inject_bot(online_mode=online_mode)
            
            if success:
                self.root.after(0, self.loader_success, online_mode)
                
                # Start monitoring
                while self.is_running:
                    time.sleep(5)
                    if not self.loader.is_rocket_league_running():
                        self.root.after(0, self.log_message, 
                                      "Warning: Rocket League process not found")
            else:
                error_msg = "Bot injection failed"
                if online_mode:
                    error_msg += " (make sure you're in a custom/private match that allows bots)"
                self.root.after(0, self.loader_failed, error_msg)
                
        except Exception as e:
            self.root.after(0, self.loader_failed, f"Error: {e}")
    
    def loader_success(self, online_mode=False):
        """Handle successful bot loading"""
        if online_mode:
            status_text = "✅ Running (Online)"
            success_msg = "🎉 Bot ready for online matches! Join a custom/private match to see the bot."
        else:
            status_text = "✅ Running (Exhibition)"
            success_msg = "🎉 Bot successfully injected! Start an exhibition match to see the bot."
            
        self.bot_status.config(text=status_text, style='Success.TLabel')
        self.progress.stop()
        self.log_message(success_msg)
    
    def loader_failed(self, error_msg):
        """Handle failed bot loading"""
        self.is_running = False
        self.start_btn.config(state='normal')
        self.stop_btn.config(state='disabled')
        self.bot_status.config(text="❌ Failed", style='Danger.TLabel')
        self.progress.stop()
        self.log_message(f"❌ {error_msg}")
        messagebox.showerror("Error", error_msg)
    
    def stop_bot(self):
        """Stop the bot"""
        if not self.is_running:
            return
        
        self.is_running = False
        
        if self.loader:
            self.loader.stop()
        
        # Update UI
        self.start_btn.config(state='normal')
        self.stop_btn.config(state='disabled')
        self.bot_status.config(text="⏹️ Stopped", style='Danger.TLabel')
        self.progress.stop()
        
        self.log_message("🛑 Bot loader stopped")
    
    def run_setup(self):
        """Run setup and verification"""
        def setup_task():
            try:
                import subprocess
                bot_path = self.bot_path_var.get()
                
                # Run setup script
                result = subprocess.run([
                    sys.executable, "setup.py"
                ], cwd=bot_path, capture_output=True, text=True)
                
                if result.returncode == 0:
                    self.root.after(0, messagebox.showinfo, "Setup Complete", 
                                  "Setup and verification completed successfully!")
                    self.root.after(0, self.refresh_status)
                else:
                    self.root.after(0, messagebox.showerror, "Setup Failed", 
                                  f"Setup failed:\n{result.stderr}")
            except Exception as e:
                self.root.after(0, messagebox.showerror, "Error", f"Setup error: {e}")
        
        threading.Thread(target=setup_task, daemon=True).start()
    
    def show_help(self):
        """Show help dialog"""
        help_text = """
🚀 Nexto Bot Loader Help

📋 Configuration:
• Bot Path: Directory containing the Nexto bot files
• Team: Blue (0) or Orange (1) 
• Wait for RL: Pause until Rocket League starts
• Use GUI: Launch RLBot GUI instead of direct injection
• Auto-install: Automatically install missing dependencies
• Online Mode: Enable bot for online matches (custom/private only)

🎮 Usage:
1. Configure settings above
2. Click "Start Bot" 
3. Bot will automatically inject into Rocket League

🌐 Online Mode:
• Allows bot to join CUSTOM/PRIVATE online matches
• Does NOT work with ranked/casual matchmaking
• Host must enable bots in match settings
• Only works with certain game modes

🏠 Exhibition Mode (Default):
• Works with offline/local matches
• Full control over match settings
• Recommended for testing and practice

⚙️ Troubleshooting:
• Use "Setup & Verify" to check installation
• Check log output for detailed information
• Try "Use RLBot GUI" if direct injection fails
• For online mode: ensure you're in a custom/private match
• Ensure Rocket League is running before starting

📝 Support:
Check the log output for detailed error messages.
"""
        
        help_window = tk.Toplevel(self.root)
        help_window.title("Help")
        help_window.geometry("500x400")
        
        text_widget = scrolledtext.ScrolledText(help_window, wrap=tk.WORD, padx=20, pady=20)
        text_widget.pack(fill=tk.BOTH, expand=True)
        text_widget.insert(tk.END, help_text)
        text_widget.config(state='disabled')
    
    def log_message(self, message):
        """Add message to log"""
        self.log_text.config(state='normal')
        timestamp = time.strftime("%H:%M:%S")
        self.log_text.insert(tk.END, f"[{timestamp}] {message}\n")
        self.log_text.see(tk.END)
        self.log_text.config(state='disabled')
    
    def check_log_queue(self):
        """Check for new log messages"""
        try:
            while True:
                message = self.log_queue.get_nowait()
                self.log_message(message)
        except queue.Empty:
            pass
        
        # Schedule next check
        self.root.after(100, self.check_log_queue)
    
    def clear_log(self):
        """Clear the log display"""
        self.log_text.config(state='normal')
        self.log_text.delete(1.0, tk.END)
        self.log_text.config(state='disabled')
    
    def save_log(self):
        """Save log to file"""
        try:
            filename = filedialog.asksaveasfilename(
                defaultextension=".txt",
                filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
            )
            if filename:
                with open(filename, 'w') as f:
                    log_content = self.log_text.get(1.0, tk.END)
                    f.write(log_content)
                messagebox.showinfo("Success", f"Log saved to {filename}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save log: {e}")
    
    def on_closing(self):
        """Handle window closing"""
        if self.is_running:
            if messagebox.askokcancel("Quit", "Bot is running. Stop and quit?"):
                self.stop_bot()
                self.root.after(1000, self.root.destroy)
        else:
            self.root.destroy()

def main():
    """Main entry point for GUI"""
    root = tk.Tk()
    
    # Set window icon if available
    try:
        if Path("nexto_logo.png").exists():
            # For Windows .ico support
            pass  # Could convert PNG to ICO here
    except:
        pass
    
    app = NextoBotGUI(root)
    
    # Handle window closing
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    
    # Center window on screen
    root.update_idletasks()
    x = (root.winfo_screenwidth() - root.winfo_width()) // 2
    y = (root.winfo_screenheight() - root.winfo_height()) // 2
    root.geometry(f"+{x}+{y}")
    
    # Start the GUI
    root.mainloop()

if __name__ == "__main__":
    main()