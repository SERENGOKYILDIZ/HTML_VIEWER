# 🚀 Web Viewer - Modern HTML/CSS/JS Editor

A modern, feature-rich web development environment built with Python and Tkinter. This application provides a sleek interface for writing, editing, and previewing HTML, CSS, and JavaScript code with real-time web preview capabilities.

## ✨ Features

### 🎨 Modern Interface
- **Dark Theme**: Elegant black, gray, and blue color scheme
- **Tabbed Interface**: Multiple file tabs for efficient workflow
- **Modern UI**: Clean, professional design with hover effects
- **Responsive Layout**: Adaptive interface that works on different screen sizes

### 📝 Code Editor
- **Syntax Highlighting**: Support for HTML, CSS, and JavaScript
- **Multi-tab Editing**: Work on multiple files simultaneously
- **Auto-save**: Automatic content preservation
- **Large Font Support**: Easy-to-read Cascadia Code font

### 🌐 Web Preview
- **Embedded WebView**: Preview HTML content within the application
- **Full Screen Mode**: Immersive preview experience
- **Real-time Updates**: Instant preview of your code changes
- **Cross-platform**: Works on Windows, macOS, and Linux

### 💾 File Management
- **New File Creation**: Start with empty HTML templates
- **File Opening**: Load existing HTML files
- **Save & Save As**: Flexible file saving options
- **Tab Management**: Easy file switching and organization

## 🛠️ Installation

### Prerequisites
- Python 3.7 or higher
- pip (Python package manager)

### Setup Instructions

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd HTML_VIEWER
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   python main.py
   ```

## 📦 Dependencies

The project uses the following Python packages:

- **tkinter**: GUI framework (included with Python)
- **pywebview**: Web browser integration for previews
- **tempfile**: Temporary file handling (included with Python)
- **webbrowser**: Fallback browser integration (included with Python)

## 🎯 Usage

### Getting Started

1. **Launch the Application**
   - Run `python main.py`
   - The application starts with an empty HTML template

2. **Create New Files**
   - Click "📄 New File" to create a new tab
   - Each tab represents a separate HTML file

3. **Edit Your Code**
   - Write HTML, CSS, and JavaScript in the editor
   - Use the large, readable Cascadia Code font
   - Multiple tabs allow working on different files

4. **Preview Your Work**
   - Click "🔄 Preview" to see your HTML in action
   - The preview opens in a full-screen WebView window
   - Close the preview to return to editing

5. **Save Your Files**
   - Click "💾 Save" to save the current file
   - Use "Save As" for new files or different locations

### Advanced Features

#### Tab Management
- **Multiple Tabs**: Work on several files simultaneously
- **Tab Switching**: Click tabs to switch between files
- **Close Tabs**: Use the "❌ Close" button in each tab

#### Web Preview
- **Full Screen**: Preview opens in full-screen mode
- **Top Bar Preserved**: Windows title bar remains visible for easy closing
- **Responsive**: Preview adapts to your screen size

#### File Operations
- **Open Files**: Load existing HTML files from your system
- **Save Files**: Save your work with custom file names
- **Auto-recovery**: Content is preserved between sessions

## 🎨 Customization

### Theme Colors
The application uses a modern dark theme with:
- **Background**: `#0a0a0a` (Pure black)
- **Surface**: `#1a1a1a` (Dark gray)
- **Editor**: `#2a2a2a` (Medium gray)
- **Primary**: `#1e40af` (Dark blue)
- **Secondary**: `#3b82f6` (Blue)
- **Accent**: `#60a5fa` (Light blue)

### Font Settings
- **UI Font**: Segoe UI (Modern, readable)
- **Code Font**: Cascadia Code (Developer-friendly)
- **Font Sizes**: Optimized for readability

## 🔧 Technical Details

### Architecture
- **Main Class**: `WebViewer` - Core application logic
- **UI Framework**: Tkinter with custom styling
- **Web Preview**: pywebview for embedded browser
- **File Handling**: Native Python file operations

### Key Components
- **Main Window**: Full-screen application with toolbar
- **Notebook Widget**: Tabbed interface for multiple files
- **Text Editor**: ScrolledText with syntax support
- **WebView Window**: Separate preview window
- **Status Bar**: Real-time application status

### Error Handling
- **Graceful Fallbacks**: WebView → Browser fallback
- **Exception Handling**: Comprehensive error messages
- **File Validation**: Safe file operations
- **Memory Management**: Automatic cleanup

## 🚀 Performance

### Optimizations
- **Lazy Loading**: Components load as needed
- **Memory Efficient**: Minimal resource usage
- **Fast Startup**: Quick application launch
- **Smooth UI**: Responsive interface

### System Requirements
- **RAM**: 512MB minimum, 2GB recommended
- **Storage**: 50MB for application files
- **Display**: 1024x768 minimum resolution
- **OS**: Windows 10+, macOS 10.14+, Linux

## 🐛 Troubleshooting

### Common Issues

**WebView Not Opening**
- Ensure pywebview is installed: `pip install pywebview`
- Check if your system supports WebView
- Try the browser fallback option

**File Save Errors**
- Check file permissions in the target directory
- Ensure sufficient disk space
- Verify file path is valid

**UI Display Issues**
- Update your graphics drivers
- Check display scaling settings
- Restart the application

### Getting Help
- Check the console output for error messages
- Verify all dependencies are installed
- Ensure Python version is 3.7+

## 📄 License

This project is open source and available under the MIT License.

## 🤝 Contributing

We welcome contributions! Please feel free to:
- Report bugs and issues
- Suggest new features
- Submit pull requests
- Improve documentation

## 📞 Support

For support and questions:
- Create an issue on GitHub
- Check the troubleshooting section
- Review the documentation

---

**Made with ❤️ for developers who love clean, modern tools.** 