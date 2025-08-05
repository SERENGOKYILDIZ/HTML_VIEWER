import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import os
from pathlib import Path
import tempfile
import threading
import webbrowser
import time
import subprocess
import platform
import sys

# WebView import'unu try-except ile yapalım
try:
    import webview
    WEBVIEW_AVAILABLE = True
except ImportError:
    WEBVIEW_AVAILABLE = False
    print("Uyarı: pywebview kütüphanesi bulunamadı. Tarayıcıda açma modu kullanılacak.")

class WebViewer:
    def __init__(self, root):
        self.root = root
        self.root.title("🚀 Web Görüntüleyici - Modern HTML/CSS/JS Editörü")
        
        # Tam ekran yap ve boyutlandırmayı sabit tut
        try:
            self.root.state('zoomed')
            # Pencere boyutlandırmasını sabit tut
            self.root.resizable(True, True)
            # Minimum boyut ayarla
            self.root.minsize(1200, 800)
        except:
            self.root.geometry("1400x900")
            self.root.resizable(True, True)
            self.root.minsize(1200, 800)
        
        # Modern dark theme
        self.root.configure(bg='#0a0a0a')
        
        # Modern stil ayarları
        self.setup_modern_styles()
        
    def setup_modern_styles(self):
        """Modern stil ayarları - Siyah, Gri, Mavi Tema"""
        try:
            style = ttk.Style()
            style.theme_use('clam')
            
            # Siyah, Gri, Mavi renk paleti
            primary_color = '#1e40af'      # Koyu mavi
            secondary_color = '#3b82f6'     # Mavi
            accent_color = '#60a5fa'        # Açık mavi
            hover_color = '#4f46e5'         # Hover mavi
            
            # Dark theme renkler - Siyah ve Gri tonları
            bg_dark = '#0a0a0a'            # Siyah arka plan
            bg_medium = '#1a1a1a'          # Koyu gri
            bg_light = '#2a2a2a'           # Orta gri
            bg_card = '#333333'            # Kart gri
            text_primary = '#ffffff'       # Beyaz metin
            text_secondary = '#a0a0a0'     # Gri metin
            text_muted = '#666666'         # Soluk gri
            
            # Modern buton stilleri
            style.configure('Modern.TButton',
                          background=primary_color,
                          foreground=text_primary,
                          borderwidth=0,
                          focuscolor='none',
                          font=('Segoe UI', 11, 'bold'),
                          padding=[18, 10])
            
            style.map('Modern.TButton',
                     background=[('active', hover_color),
                               ('pressed', accent_color)])
            
            # Büyük buton stili
            style.configure('Large.TButton',
                          background=secondary_color,
                          foreground=text_primary,
                          borderwidth=0,
                          focuscolor='none',
                          font=('Segoe UI', 13, 'bold'),
                          padding=[22, 12])
            
            style.map('Large.TButton',
                     background=[('active', hover_color),
                               ('pressed', accent_color)])
            
            # Notebook stili
            style.configure('Modern.TNotebook',
                          background=bg_dark,
                          borderwidth=0,
                          tabmargins=[3, 6, 3, 0])
            
            style.configure('Modern.TNotebook.Tab',
                          background=bg_medium,
                          foreground=text_secondary,
                          borderwidth=0,
                          focuscolor='none',
                          font=('Segoe UI', 11, 'bold'),
                          padding=[18, 10])
            
            style.map('Modern.TNotebook.Tab',
                     background=[('selected', primary_color),
                               ('active', hover_color)],
                     foreground=[('selected', text_primary),
                               ('active', text_primary)])
            
            # Frame stili
            style.configure('Modern.TFrame',
                          background=bg_dark)
            
            # Label stili
            style.configure('Modern.TLabel',
                          background=bg_dark,
                          foreground=text_primary,
                          font=('Segoe UI', 11))
            
            # Başlık stili
            style.configure('Title.TLabel',
                          background=bg_dark,
                          foreground=text_primary,
                          font=('Segoe UI', 18, 'bold'))
            
        except Exception as e:
            print(f"Stil ayarlama hatası: {e}")
            pass
        
        self.current_file = None
        self.temp_file = None
        self.browser_process = None
        self.open_files = {}  # Açık dosyaları takip et
        self.setup_ui()
        
    def setup_ui(self):
        # Main toolbar (always visible)
        self.setup_main_toolbar()
        
        # Main notebook (tab container) - modern design
        notebook_frame = tk.Frame(self.root, bg='#0a0a0a')
        notebook_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=(10, 15))
        
        self.notebook = ttk.Notebook(notebook_frame, style='Modern.TNotebook')
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Modern durum çubuğu
        status_frame = tk.Frame(self.root, bg='#1a1a1a', height=30)
        status_frame.pack(side=tk.BOTTOM, fill=tk.X)
        status_frame.pack_propagate(False)
        
        self.status_bar = tk.Label(status_frame, 
                                  text="🚀 Web Viewer Ready", 
                                  font=('Segoe UI', 10),
                                  bg='#1a1a1a',
                                  fg='#a0a0a0')
        self.status_bar.pack(side=tk.LEFT, padx=15, pady=5)
        
        # Varsayılan dosya var mı kontrol et
        self.check_default_file()
        
    def setup_main_toolbar(self):
        """Modern main toolbar"""
        # Main toolbar frame (gradient background)
        main_toolbar = tk.Frame(self.root, bg='#1a1a1a', height=80)
        main_toolbar.pack(fill=tk.X, padx=0, pady=0)
        main_toolbar.pack_propagate(False)
        
        # Inner frame
        inner_frame = tk.Frame(main_toolbar, bg='#1a1a1a')
        inner_frame.pack(fill=tk.BOTH, padx=20, pady=15)
        
        # Title (modern gradient text effect)
        title_frame = tk.Frame(inner_frame, bg='#1a1a1a')
        title_frame.pack(side=tk.LEFT, padx=(0, 40))
        
        title_label = tk.Label(title_frame, 
                              text="🚀 Web Viewer", 
                              font=('Segoe UI', 20, 'bold'),
                              bg='#1a1a1a',
                              fg='#ffffff')
        title_label.pack(side=tk.LEFT)
        
        subtitle_label = tk.Label(title_frame,
                                 text="Modern HTML/CSS/JS Editor",
                                 font=('Segoe UI', 10),
                                 bg='#1a1a1a',
                                 fg='#a0a0a0')
        subtitle_label.pack(side=tk.LEFT, padx=(10, 0))
        
        # Buttons frame (right side)
        buttons_frame = tk.Frame(inner_frame, bg='#1a1a1a')
        buttons_frame.pack(side=tk.RIGHT)
        
        # Modern buttons
        self.create_modern_button(buttons_frame, "📄 New File", 
                                self.create_new_file, '#1e40af')
        self.create_modern_button(buttons_frame, "📁 Open File", 
                                self.open_file, '#3b82f6')
        self.create_modern_button(buttons_frame, "🔄 Preview", 
                                self.show_preview, '#60a5fa')
        self.create_modern_button(buttons_frame, "💾 Save", 
                                self.save_file, '#4f46e5')
        
    def create_modern_button(self, parent, text, command, color):
        """Create modern button"""
        button_frame = tk.Frame(parent, bg='#1a1a1a')
        button_frame.pack(side=tk.LEFT, padx=5)
        
        button = tk.Button(button_frame,
                          text=text,
                          command=command,
                          font=('Segoe UI', 11, 'bold'),
                          bg=color,
                          fg='#ffffff',
                          activebackground='#4f46e5',
                          activeforeground='#ffffff',
                          relief='flat',
                          borderwidth=0,
                          padx=20,
                          pady=8,
                          cursor='hand2')
        button.pack()
        
        # Hover effect
        def on_enter(e):
            button['bg'] = '#4f46e5'
        def on_leave(e):
            button['bg'] = color
        button.bind('<Enter>', on_enter)
        button.bind('<Leave>', on_leave)
        
    def check_default_file(self):
        """Create empty file on first startup"""
        # Always start with an empty file
        self.create_empty_editor_tab()
        
    def create_empty_editor_tab(self):
        """Create empty editor tab"""
        # Empty HTML content
        empty_html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🚀 Web Viewer</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        h1 { color: #333; }
        .container { max-width: 800px; margin: 0 auto; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🚀 Web Viewer</h1>
        <p>Write your HTML code here and click the "Preview" button.</p>
        <p>JavaScript, CSS and HTML5 are fully supported.</p>
    </div>
</body>
</html>"""
        
        # Create empty editor tab
        self.add_file_tab(None, empty_html, "📝 New File")
        
    def create_welcome_screen(self):
        """Welcome screen - buttons only"""
        # Main frame
        welcome_frame = ttk.Frame(self.notebook)
        self.notebook.add(welcome_frame, text="🚀 Welcome")
        
        # Title
        title_label = ttk.Label(welcome_frame, text="🚀 Web Viewer", 
                               font=('Arial', 24, 'bold'))
        title_label.pack(pady=(50, 20))
        
        # Description
        desc_label = ttk.Label(welcome_frame, 
                              text="Create a new file or open an existing one to test your HTML, CSS and JavaScript code.",
                              font=('Arial', 11), wraplength=600)
        desc_label.pack(pady=(0, 50))
        
        # Buttons frame
        buttons_frame = ttk.Frame(welcome_frame)
        buttons_frame.pack(pady=20)
        
        # New file button
        new_file_btn = ttk.Button(buttons_frame, text="📄 Create New File", 
                                 command=self.create_new_file_from_welcome,
                                 style='Large.TButton')
        new_file_btn.pack(pady=10, padx=20, fill=tk.X)
        
        # Open file button
        open_file_btn = ttk.Button(buttons_frame, text="📁 Open File", 
                                  command=self.open_file_from_welcome,
                                  style='Large.TButton')
        open_file_btn.pack(pady=10, padx=20, fill=tk.X)
        
        # Örnek dosya oluştur butonu
        create_example_btn = ttk.Button(buttons_frame, text="🎨 Create Example HTML", 
                                       command=self.create_example_file,
                                       style='Large.TButton')
        create_example_btn.pack(pady=10, padx=20, fill=tk.X)
        
        # Store welcome frame
        self.welcome_frame = welcome_frame
        
    def add_existing_file_to_tab(self, frame):
        """Mevcut dosyayı seçip aktif sekmeye yükle"""
        file_path = filedialog.askopenfilename(
            title="HTML Dosyası Seç",
            filetypes=[("HTML dosyaları", "*.html *.htm"), ("Tüm dosyalar", "*.*")]
        )
        
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    content = file.read()
                    
                # Dosya bilgilerini güncelle
                file_info = self.open_files.get(frame)
                if file_info and 'editor' in file_info:
                    # Editör içeriğini güncelle
                    file_info['editor'].delete(1.0, tk.END)
                    file_info['editor'].insert(1.0, content)
                    
                    # Dosya bilgilerini güncelle
                    file_info['path'] = file_path
                    file_info['title'] = os.path.basename(file_path)
                    
                    # Sekme başlığını güncelle
                    tab_index = self.notebook.index(frame)
                    self.notebook.tab(tab_index, text=file_info['title'])
                    
                    self.status_bar.config(text=f"✅ File loaded: {file_path}")
                    
            except Exception as e:
                messagebox.showerror("❌ Error", f"Error loading file: {str(e)}")
        
    def create_new_file_from_welcome(self):
        """Create new file from welcome screen"""
        # Create new file tab
        self.add_file_tab(None, "", f"New File {len(self.open_files) + 1}")
        self.status_bar.config(text="📄 New file created")
        
        # Close welcome tab
        if hasattr(self, 'welcome_frame'):
            self.notebook.forget(self.welcome_frame)
        
    def open_file_from_welcome(self):
        """Open file from welcome screen"""
        self.open_file()
        
        # Close welcome tab if file opened
        if len(self.open_files) > 0 and hasattr(self, 'welcome_frame'):
            self.notebook.forget(self.welcome_frame)
        
    def create_example_file(self):
        """Create example HTML file"""
        example_html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🚀 Example Web Page</title>
    <style>
        body { 
            font-family: Arial, sans-serif; 
            margin: 0; 
            padding: 20px; 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }
        .container { 
            max-width: 800px; 
            margin: 0 auto; 
            background: rgba(255,255,255,0.1);
            padding: 30px;
            border-radius: 15px;
            backdrop-filter: blur(10px);
        }
        h1 { 
            color: #fff; 
            text-align: center;
            margin-bottom: 30px;
        }
        .feature {
            background: rgba(255,255,255,0.2);
            padding: 15px;
            margin: 10px 0;
            border-radius: 8px;
            border-left: 4px solid #4CAF50;
        }
        button {
            background: #4CAF50;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 5px;
            cursor: pointer;
            margin: 5px;
        }
        button:hover {
            background: #45a049;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🚀 Web Viewer Example</h1>
        <p>This is an example HTML page. HTML, CSS and JavaScript are fully supported.</p>
        
        <div class="feature">
            <h3>✅ Supported Features:</h3>
            <ul>
                <li>Full HTML5 support</li>
                <li>CSS3 animations and transitions</li>
                <li>Complete JavaScript execution</li>
                <li>Modern web standards</li>
                <li>Responsive design</li>
            </ul>
        </div>
        
        <div class="feature">
            <h3>🎮 Interactive Example:</h3>
            <button onclick="showMessage()">Show Message</button>
            <button onclick="changeColor()">Change Color</button>
            <button onclick="addElement()">Add Element</button>
            <div id="output"></div>
        </div>
    </div>
    
    <script>
        function showMessage() {
            alert('🎉 JavaScript is working!');
        }
        
        function changeColor() {
            const colors = ['#667eea', '#764ba2', '#f093fb', '#f5576c', '#4facfe'];
            const randomColor = colors[Math.floor(Math.random() * colors.length)];
            document.body.style.background = `linear-gradient(135deg, ${randomColor} 0%, ${randomColor}dd 100%)`;
        }
        
        function addElement() {
            const output = document.getElementById('output');
            const newElement = document.createElement('div');
            newElement.style.background = 'rgba(255,255,255,0.2)';
            newElement.style.padding = '10px';
            newElement.style.margin = '5px 0';
            newElement.style.borderRadius = '5px';
            newElement.innerHTML = '🆕 New element added! - ' + new Date().toLocaleTimeString();
            output.appendChild(newElement);
        }
    </script>
</body>
</html>"""
        
        # Create example file tab
        self.add_file_tab(None, example_html, "🎨 Example HTML")
        self.status_bar.config(text="🎨 Example HTML file created")
        
        # Close welcome tab
        if hasattr(self, 'welcome_frame'):
            self.notebook.forget(self.welcome_frame)
        
    def create_default_editor_tab(self):
        """Create default editor tab"""
        # Get default HTML content
        try:
            with open('default_page.html', 'r', encoding='utf-8') as file:
                default_html = file.read()
        except FileNotFoundError:
            # Create simple HTML if file not found
            default_html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🚀 Web Viewer</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        h1 { color: #333; }
        .container { max-width: 800px; margin: 0 auto; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🚀 Web Viewer</h1>
        <p>Write your HTML code here and click the "Preview" button.</p>
        <p>JavaScript, CSS and HTML5 are fully supported.</p>
    </div>
</body>
</html>"""
        
        # Create main editor tab
        self.add_file_tab(None, default_html, "📝 Main Editor")
        
    def add_file_tab(self, file_path, content, custom_title=None):
        """Add new file tab"""
        # Tab title
        if custom_title:
            tab_title = custom_title
        else:
            tab_title = os.path.basename(file_path) if file_path else f"New File {len(self.open_files) + 1}"
        
        # Create new frame
        file_frame = ttk.Frame(self.notebook)
        self.notebook.add(file_frame, text=tab_title)
        
        # Store file info
        self.open_files[file_frame] = {
            'path': file_path,
            'title': tab_title,
            'content': content
        }
        
        # Create tab content
        self.setup_file_tab(file_frame, content)
        
        # Make tab active
        self.notebook.select(file_frame)
        
        return file_frame
        
    def setup_file_tab(self, frame, content):
        """Create modern file tab content"""
        # Modern top toolbar
        toolbar_frame = tk.Frame(frame, bg='#1a1a1a', height=50)
        toolbar_frame.pack(fill=tk.X, pady=(0, 5))
        toolbar_frame.pack_propagate(False)
        
        # Inner toolbar frame
        inner_toolbar = tk.Frame(toolbar_frame, bg='#1a1a1a')
        inner_toolbar.pack(fill=tk.BOTH, padx=15, pady=10)
        
        # Modern tab buttons
        self.create_modern_button(inner_toolbar, "❌ Close", 
                                lambda: self.close_file_tab(frame), '#ef4444')
        
        # File path label
        file_info = self.open_files[frame]
        file_label = tk.Label(inner_toolbar, 
                             text=f"📄 {file_info['title']}", 
                             font=('Segoe UI', 10, 'bold'),
                             bg='#1a1a1a',
                             fg='#ffffff')
        file_label.pack(side=tk.RIGHT, padx=(0, 10))
        
        # Modern code editor
        editor_frame = tk.Frame(frame, bg='#2a2a2a')
        editor_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        code_editor = scrolledtext.ScrolledText(
            editor_frame,
            wrap=tk.WORD,
            font=('Cascadia Code', 12),
            bg='#2a2a2a',
            fg='#ffffff',
            insertbackground='#60a5fa',
            selectbackground='#1e40af',
            relief='flat',
            borderwidth=0,
            padx=15,
            pady=15
        )
        code_editor.pack(fill=tk.BOTH, expand=True)
        
        # Load content
        code_editor.delete(1.0, tk.END)
        code_editor.insert(1.0, content)
        
        # Store editor reference
        self.open_files[frame]['editor'] = code_editor
        
    def show_preview(self):
        """Aktif sekmeden embedded görüntüleme"""
        # Aktif sekmeyi bul
        current_tab = self.notebook.select()
        if current_tab:
            # Aktif sekmenin frame'ini bul
            for frame in self.open_files:
                if str(frame) == current_tab:
                    file_info = self.open_files[frame]
                    if 'editor' in file_info:
                        content = file_info['editor'].get(1.0, tk.END)
                        if content.strip():
                            self.create_embedded_preview(content, file_info['title'])
                        else:
                            messagebox.showwarning("⚠️ Warning", "No HTML content found to preview!")
                    return
        else:
            messagebox.showwarning("⚠️ Warning", "No active tab found!")
            
    def show_file_preview(self, frame):
        """Dosya sekmesinden embedded görüntüleme"""
        file_info = self.open_files.get(frame)
        if file_info and 'editor' in file_info:
            content = file_info['editor'].get(1.0, tk.END)
            if content.strip():
                self.create_embedded_preview(content, file_info['title'])
            else:
                messagebox.showwarning("⚠️ Warning", "No HTML content found to preview!")
                
    def create_embedded_preview(self, content, title):
        """Program içinde ayrı pencerede görüntüleme"""
        try:
            # Geçici dosya oluştur
            with tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False, encoding='utf-8') as temp_file:
                temp_file.write(content)
                temp_file_path = temp_file.name
            
            if WEBVIEW_AVAILABLE:
                try:
                    # Get screen dimensions
                    screen_width = self.root.winfo_screenwidth()
                    screen_height = self.root.winfo_screenheight()
                    
                    # Calculate window position (center)
                    x_position = 0  # Left edge
                    y_position = 0  # Top edge
                    
                    # Create WebView window - full screen but top bar preserved
                    webview.create_window(
                        title=f"🌐 {title} - Web Viewer",
                        url=f'file://{temp_file_path}',
                        width=screen_width,     # Screen width
                        height=screen_height,   # Screen height
                        x=0,                    # Left edge
                        y=0,                    # Top edge
                        resizable=True,
                        text_select=True,
                        confirm_close=False,
                        frameless=False,        # Top bar visible
                        easy_drag=False,        # Disable dragging
                        fullscreen=False,       # Not fullscreen, top bar preserved
                        on_top=True,            # Keep on top and lock
                        background_color='#ffffff'
                    )
                    
                    # Start WebView
                    def start_webview():
                        try:
                            # Start WebView
                            webview.start(debug=False)
                        except Exception as e:
                            print(f"WebView error: {e}")
                            # Open in browser if error occurs
                            webbrowser.open(f'file://{temp_file_path}')
                        finally:
                            # Return main window to full screen when WebView closes
                            try:
                                # Make main window full screen again
                                self.root.state('zoomed')
                                # Reset sizing
                                self.root.resizable(True, True)
                                self.root.minsize(1200, 800)
                            except:
                                pass
                            # Clean up temporary file
                            try:
                                os.unlink(temp_file_path)
                            except:
                                pass
                    
                    # Keep main window fixed
                    try:
                        self.root.resizable(True, True)
                        self.root.minsize(1200, 800)
                    except:
                        pass
                    
                    # Run in main thread
                    self.root.after(100, start_webview)
                    self.status_bar.config(text=f"🌐 {title} opened in screen size (top bar preserved)")
                    
                except Exception as e:
                    # Open in browser if WebView fails
                    webbrowser.open(f'file://{temp_file_path}')
                    messagebox.showinfo("ℹ️ Info", f"WebView not available, opened in browser.\nError: {str(e)}")
                    # Clean up temporary file
                    try:
                        os.unlink(temp_file_path)
                    except:
                        pass
            else:
                # Open in browser if WebView not available
                webbrowser.open(f'file://{temp_file_path}')
                self.status_bar.config(text=f"🌐 {title} opened in browser")
                messagebox.showinfo("ℹ️ Info", "pywebview library not found. Opened in browser.")
                # Clean up temporary file
                try:
                    os.unlink(temp_file_path)
                except:
                    pass
            
        except Exception as e:
            messagebox.showerror("❌ Error", f"Error opening preview window: {str(e)}")
        
    def open_file(self):
        """Open file and create new tab"""
        file_path = filedialog.askopenfilename(
            title="Select HTML File",
            filetypes=[("HTML files", "*.html *.htm"), ("All files", "*.*")]
        )
        
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    content = file.read()
                    
                # Yeni sekme oluştur
                self.add_file_tab(file_path, content)
                self.status_bar.config(text=f"✅ Dosya açıldı: {file_path}")
                
            except Exception as e:
                messagebox.showerror("❌ Hata", f"Dosya açılırken hata oluştu: {str(e)}")
        else:
            # Dosya seçilmezse yeni boş sekme oluştur
            self.add_file_tab(None, "", f"Yeni Dosya {len(self.open_files) + 1}")
            self.status_bar.config(text="📝 Yeni boş sekme oluşturuldu")
                
    def save_file_tab(self, frame):
        """Save file tab"""
        file_info = self.open_files.get(frame)
        if file_info and 'editor' in file_info:
            content = file_info['editor'].get(1.0, tk.END)
            
            if file_info['path']:
                try:
                    with open(file_info['path'], 'w', encoding='utf-8') as file:
                        file.write(content)
                    self.status_bar.config(text=f"💾 File saved: {file_info['path']}")
                    messagebox.showinfo("✅ Success", "File saved successfully!")
                except Exception as e:
                    messagebox.showerror("❌ Error", f"Error saving file: {str(e)}")
            else:
                self.save_as_file_tab(frame)
                
    def save_as_file_tab(self, frame):
        """Save file tab as"""
        file_info = self.open_files.get(frame)
        if file_info and 'editor' in file_info:
            content = file_info['editor'].get(1.0, tk.END)
            
            file_path = filedialog.asksaveasfilename(
                title="Save HTML File",
                defaultextension=".html",
                filetypes=[("HTML files", "*.html"), ("All files", "*.*")]
            )
            
            if file_path:
                try:
                    with open(file_path, 'w', encoding='utf-8') as file:
                        file.write(content)
                    
                    # Dosya bilgilerini güncelle
                    file_info['path'] = file_path
                    file_info['title'] = os.path.basename(file_path)
                    
                    # Sekme başlığını güncelle
                    tab_index = self.notebook.index(frame)
                    self.notebook.tab(tab_index, text=file_info['title'])
                    
                    self.status_bar.config(text=f"💾 File saved: {file_path}")
                    messagebox.showinfo("✅ Success", "File saved successfully!")
                except Exception as e:
                    messagebox.showerror("❌ Error", f"Error saving file: {str(e)}")
    
    def close_file_tab(self, frame):
        """Close file tab"""
        if frame in self.open_files:
            # Remove tab
            self.notebook.forget(frame)
            # Clean file info
            del self.open_files[frame]
            self.status_bar.config(text="🗑️ Tab closed")
        
    def save_file(self):
        """Save active tab"""
        # Find active tab
        current_tab = self.notebook.select()
        if current_tab:
            # Find active tab frame
            for frame in self.open_files:
                if str(frame) == current_tab:
                    file_info = self.open_files[frame]
                    if 'editor' in file_info:
                        content = file_info['editor'].get(1.0, tk.END)
                        if file_info['path']:
                            try:
                                with open(file_info['path'], 'w', encoding='utf-8') as file:
                                    file.write(content)
                                self.status_bar.config(text=f"💾 File saved: {file_info['path']}")
                                messagebox.showinfo("✅ Success", "File saved successfully!")
                            except Exception as e:
                                messagebox.showerror("❌ Error", f"Error saving file: {str(e)}")
                        else:
                            self.save_as_file()
                    return
        messagebox.showwarning("⚠️ Warning", "No active tab found!")
            
    def save_as_file(self):
        """Save active tab as"""
        # Find active tab
        current_tab = self.notebook.select()
        if current_tab:
            # Find active tab frame
            for frame in self.open_files:
                if str(frame) == current_tab:
                    file_info = self.open_files[frame]
                    if 'editor' in file_info:
                        content = file_info['editor'].get(1.0, tk.END)
                        
                        file_path = filedialog.asksaveasfilename(
                            title="Save HTML File",
                            defaultextension=".html",
                            filetypes=[("HTML files", "*.html"), ("All files", "*.*")]
                        )
                        
                        if file_path:
                            try:
                                with open(file_path, 'w', encoding='utf-8') as file:
                                    file.write(content)
                                
                                # Update file info
                                file_info['path'] = file_path
                                file_info['title'] = os.path.basename(file_path)
                                
                                # Update tab title
                                tab_index = self.notebook.index(frame)
                                self.notebook.tab(tab_index, text=file_info['title'])
                                
                                self.status_bar.config(text=f"💾 File saved: {file_path}")
                                messagebox.showinfo("✅ Success", "File saved successfully!")
                            except Exception as e:
                                messagebox.showerror("❌ Error", f"Error saving file: {str(e)}")
                    return
        messagebox.showwarning("⚠️ Warning", "No active tab found!")
        
    def clear_content(self):
        """Clear active tab"""
        # Find active tab
        current_tab = self.notebook.select()
        if current_tab:
            # Find active tab frame
            for frame in self.open_files:
                if str(frame) == current_tab:
                    file_info = self.open_files[frame]
                    if 'editor' in file_info:
                        if messagebox.askyesno("❓ Confirm", "Are you sure you want to clear the active tab content?"):
                            file_info['editor'].delete(1.0, tk.END)
                            # Clear file info
                            file_info['path'] = None
                            file_info['title'] = f"New File {len(self.open_files)}"
                            # Update tab title
                            tab_index = self.notebook.index(frame)
                            self.notebook.tab(tab_index, text=file_info['title'])
                            self.status_bar.config(text="🗑️ Content cleared")
                    return
        messagebox.showwarning("⚠️ Warning", "No active tab found!")
            
    def create_new_file(self):
        """Create new empty file tab"""
        new_file_count = len(self.open_files) + 1
        self.add_file_tab(None, "", f"New File {new_file_count}")
        self.status_bar.config(text=f"📄 New file tab created")
            
    def run(self):
        try:
            print("Web Viewer starting...")
            self.root.mainloop()
            print("Web Viewer closed.")
        except Exception as e:
            print(f"Error: {e}")
            messagebox.showerror("❌ Error", f"Error running program: {str(e)}")

def main():
    try:
        print("Program starting...")
        root = tk.Tk()
        app = WebViewer(root)
        app.run()
    except Exception as e:
        print(f"Critical error: {e}")
        input("Press Enter to continue...")

if __name__ == "__main__":
    main() 