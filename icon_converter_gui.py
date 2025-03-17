# By R.H. Amezqueta

import os
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import platform
import subprocess
from tkinterdnd2 import DND_FILES, TkinterDnD

class IconConverterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Icon Converter")
        self.root.geometry("500x700")
        
        # Configure style
        style = ttk.Style()
        style.configure("Custom.TFrame", background="#f0f0f0")
        
        # Main frame
        self.main_frame = ttk.Frame(root, style="Custom.TFrame", padding="20")
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Drop zone
        self.drop_frame = ttk.Frame(self.main_frame, style="Custom.TFrame")
        self.drop_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create a canvas for the drop zone with a visible border
        self.drop_canvas = tk.Canvas(
            self.drop_frame,
            highlightthickness=1,  # Add highlight thickness
            highlightbackground="#000000",  # Add highlight color
            bg="#f0f0f0",
            width=400,  # Fixed width
            height=150  # Fixed height
        )
        self.drop_canvas.pack(pady=20, expand=True)
        
        # Draw initial border
        self.drop_canvas.create_rectangle(
            10, 10,  # Left, Top
            390, 140,  # Right, Bottom (width-10, height-10)
            dash=(10, 5),
            outline="#000000",
            width=2,
            tags="drop_border"
        )
        
        # Create a frame for the content inside the canvas
        self.drop_content = ttk.Frame(self.drop_canvas, style="Custom.TFrame")
        self.canvas_window = self.drop_canvas.create_window(
            200, 75,  # Center of canvas (width/2, height/2)
            window=self.drop_content,
            anchor="center"
        )
        
        self.drop_label = ttk.Label(
            self.drop_content,
            text="Drag and drop your PNG image here\nor browse to select",
            justify="center",
            font=("Arial", 12)
        )
        self.drop_label.pack(pady=20)
        
        # Browse button
        self.browse_button = ttk.Button(
            self.drop_frame,
            text="Browse Image",
            command=lambda: self.browse_file(None)
        )
        self.browse_button.pack(pady=10)
        
        # Preview frame
        self.preview_frame = ttk.Frame(self.drop_frame)
        self.preview_frame.pack(fill=tk.BOTH, expand=True)
        
        self.preview_label = ttk.Label(self.preview_frame)
        self.preview_label.pack()
        
        # Progress bar
        self.progress = ttk.Progressbar(
            self.main_frame,
            orient="horizontal",
            length=300,
            mode="determinate"
        )
        self.progress.pack(pady=10)
        
        # Status label
        self.status_label = ttk.Label(
            self.main_frame,
            text="Ready",
            justify="center"
        )
        self.status_label.pack(pady=5)
        
        # Convert button
        self.convert_button = ttk.Button(
            self.main_frame,
            text="Convert",
            command=self.convert_image,
            state="disabled"
        )
        self.convert_button.pack(pady=10)
        
        # Credits label
        self.credits_label = ttk.Label(
            self.main_frame,
            text="by R.H. Amezqueta",
            justify="center",
            font=("Arial", 8, "italic"),
            foreground="gray"
        )
        self.credits_label.pack(pady=5)
        
        # Bind drag and drop
        self.drop_label.drop_target_register(DND_FILES)
        self.drop_label.dnd_bind("<<Drop>>", self.handle_drop)
        self.drop_label.bind("<Button-1>", self.browse_file)
        
        self.current_image = None
        
    def handle_drop(self, event):
        file_path = event.data
        # Remove curly braces if present (Windows)
        file_path = file_path.strip('{}')
        self.load_image(file_path)
    
    def browse_file(self, event):
        from tkinter import filedialog
        file_path = filedialog.askopenfilename(
            filetypes=[("PNG files", "*.png")]
        )
        if file_path:
            self.load_image(file_path)
    
    def load_image(self, file_path):
        if not file_path.lower().endswith('.png'):
            messagebox.showerror("Error", "Please select a PNG image")
            return
            
        try:
            # Load and display preview
            image = Image.open(file_path)
            # Resize for preview while maintaining aspect ratio
            display_size = (200, 200)
            image.thumbnail(display_size, Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(image)
            
            self.preview_label.configure(image=photo)
            self.preview_label.image = photo  # Keep a reference
            
            self.current_image = file_path
            self.convert_button.configure(state="normal")
            self.status_label.configure(text="Image loaded - Ready to convert")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load image: {str(e)}")
    
    def convert_image(self):
        if not self.current_image:
            return
            
        try:
            self.progress["value"] = 0
            self.status_label.configure(text="Creating output directory...")
            
            # Create assets directory if it doesn't exist
            if not os.path.exists('assets'):
                os.makedirs('assets')
            
            # Copy image to assets directory
            img = Image.open(self.current_image)
            assets_path = os.path.join('assets', 'logo.png')
            img.save(assets_path)
            print(f"Saved original image to {assets_path}")
            
            self.progress["value"] = 20
            self.status_label.configure(text="Creating Windows icons...")
            
            # Create Windows icons with different sizes
            windows_sizes = [
                (16, 16), (32, 32), (48, 48), (64, 64),
                (128, 128), (256, 256), (512, 512)
            ]
            
            for size in windows_sizes:
                width, height = size
                output_file = f'assets/icon_{width}x{height}.ico'
                resized_img = img.resize((width, height), Image.Resampling.LANCZOS)
                # Save as ICO with the specific size
                resized_img.save(output_file, format='ICO', sizes=[(width, height)])
                print(f"Created Windows icon: {output_file} with size {width}x{height}")
            
            self.progress["value"] = 40
            self.status_label.configure(text="Creating MacOS icons...")
            
            # Create MacOS icons
            iconset_dir = 'logo.iconset'
            if os.path.exists(iconset_dir):
                if platform.system() == 'Windows':
                    subprocess.run(['rmdir', '/s', '/q', iconset_dir], shell=True)
                else:
                    subprocess.run(['rm', '-rf', iconset_dir])
            
            os.makedirs(iconset_dir)
            
            # Generate MacOS icon sizes (including @2x for retina displays)
            mac_sizes = [
                (16, 16), (32, 32), (64, 64),  # Standard sizes
                (128, 128), (256, 256), (512, 512),  # Retina sizes
                (1024, 1024)  # App Store size
            ]
            
            for size in mac_sizes:
                width, height = size
                # Create standard size
                output_file = f'{iconset_dir}/icon_{width}x{height}.png'
                resized_img = img.resize((width, height), Image.Resampling.LANCZOS)
                resized_img.save(output_file, 'PNG')
                print(f"Created MacOS icon: {output_file}")
                
                # Create @2x size for smaller icons
                if width <= 32:
                    output_file = f'{iconset_dir}/icon_{width}x{height}@2x.png'
                    resized_img = img.resize((width*2, height*2), Image.Resampling.LANCZOS)
                    resized_img.save(output_file, 'PNG')
                    print(f"Created MacOS @2x icon: {output_file}")
            
            self.progress["value"] = 60
            self.status_label.configure(text="Creating iconset file...")
            
            # Create iconset file for MacOS
            iconset_file = f'{iconset_dir}/Contents.json'
            with open(iconset_file, 'w') as f:
                f.write('''{
  "images" : [
    {
      "filename" : "icon_16x16.png",
      "idiom" : "mac",
      "scale" : "1x",
      "size" : "16x16"
    },
    {
      "filename" : "icon_16x16@2x.png",
      "idiom" : "mac",
      "scale" : "2x",
      "size" : "16x16"
    },
    {
      "filename" : "icon_32x32.png",
      "idiom" : "mac",
      "scale" : "1x",
      "size" : "32x32"
    },
    {
      "filename" : "icon_32x32@2x.png",
      "idiom" : "mac",
      "scale" : "2x",
      "size" : "32x32"
    },
    {
      "filename" : "icon_64x64.png",
      "idiom" : "mac",
      "scale" : "1x",
      "size" : "64x64"
    },
    {
      "filename" : "icon_128x128.png",
      "idiom" : "mac",
      "scale" : "1x",
      "size" : "128x128"
    },
    {
      "filename" : "icon_128x128@2x.png",
      "idiom" : "mac",
      "scale" : "2x",
      "size" : "128x128"
    },
    {
      "filename" : "icon_256x256.png",
      "idiom" : "mac",
      "scale" : "1x",
      "size" : "256x256"
    },
    {
      "filename" : "icon_256x256@2x.png",
      "idiom" : "mac",
      "scale" : "2x",
      "size" : "256x256"
    },
    {
      "filename" : "icon_512x512.png",
      "idiom" : "mac",
      "scale" : "1x",
      "size" : "512x512"
    },
    {
      "filename" : "icon_512x512@2x.png",
      "idiom" : "mac",
      "scale" : "2x",
      "size" : "512x512"
    }
  ],
  "info" : {
    "author" : "xcode",
    "version" : 1
  }
}''')
            
            self.progress["value"] = 80
            self.status_label.configure(text="Creating MacOS icon...")
            
            # Create .icns file for MacOS
            if platform.system() == 'Darwin':
                subprocess.run(['iconutil', '-c', 'icns', iconset_dir], 
                             capture_output=True, text=True)
                if os.path.exists('logo.icns'):
                    os.rename('logo.icns', 'assets/logo.icns')
                    print("Created MacOS .icns file")
            else:
                # On Windows, create a placeholder .icns file
                with open('assets/logo.icns', 'wb') as f:
                    f.write(b'\x00' * 100)  # Create a small placeholder file
                print("Created placeholder .icns file for Windows")
            
            # Clean up iconset directory
            if platform.system() == 'Windows':
                subprocess.run(['rmdir', '/s', '/q', iconset_dir], shell=True)
            else:
                subprocess.run(['rm', '-rf', iconset_dir])
            
            self.progress["value"] = 100
            self.status_label.configure(text="Conversion completed successfully!")
            
            # Verify files were created
            created_files = []
            for file in os.listdir('assets'):
                if file.endswith(('.ico', '.icns', '.png')):
                    created_files.append(file)
            
            messagebox.showinfo(
                "Success",
                f"Icons created successfully in the 'assets' directory!\n\n"
                f"Created files:\n"
                f"- Windows icons: {', '.join([f for f in created_files if f.startswith('icon_') and f.endswith('.ico')])}\n"
                f"- MacOS icon: logo.icns\n"
                f"- Original image: logo.png\n\n"
                f"All files found in assets directory:\n{', '.join(created_files)}"
            )
            
        except Exception as e:
            self.status_label.configure(text="Error during conversion")
            messagebox.showerror("Error", f"Failed to convert image: {str(e)}")
            print(f"Error details: {str(e)}")
            import traceback
            print(f"Traceback: {traceback.format_exc()}")

    def update_drop_zone(self, event):
        # Get the canvas dimensions
        canvas_width = self.drop_canvas.winfo_width()
        canvas_height = self.drop_canvas.winfo_height()
        
        # Update the border to match canvas size
        self.drop_canvas.delete("drop_border")
        self.drop_canvas.create_rectangle(
            10, 10,  # Left, Top
            canvas_width - 10, canvas_height - 10,  # Right, Bottom
            dash=(10, 5),
            outline="#000000",
            width=2,
            tags="drop_border"
        )
        
        # Center the content window
        self.drop_canvas.coords(
            self.canvas_window,
            canvas_width/2,
            canvas_height/2
        )

def main():
    root = TkinterDnD.Tk()
    app = IconConverterApp(root)
    root.mainloop()

if __name__ == "__main__":
    main() 