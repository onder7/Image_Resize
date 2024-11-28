import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image

class ImageResizerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Toplu Resim Boyutlandırma")
        self.root.geometry("600x400")

        # Menü oluşturma
        self.menu_bar = tk.Menu(self.root)
        self.root.config(menu=self.menu_bar)
        
        # Hakkında menüsü
        self.about_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Hakkında", menu=self.about_menu)
        self.about_menu.add_command(label="Uygulama Hakkında", command=self.show_about)
        self.about_menu.add_command(label="Özellikler", command=self.show_features)

        # Ana frame
        self.main_frame = ttk.Frame(self.root, padding="10")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Klasör seçme
        self.folder_path = tk.StringVar()
        ttk.Label(self.main_frame, text="Resim Klasörü:").grid(row=0, column=0, sticky=tk.W)
        ttk.Entry(self.main_frame, textvariable=self.folder_path, width=50).grid(row=0, column=1, padx=5)
        ttk.Button(self.main_frame, text="Gözat", command=self.browse_folder).grid(row=0, column=2, padx=5)

        # Boyut girişleri
        ttk.Label(self.main_frame, text="Genişlik:").grid(row=1, column=0, sticky=tk.W, pady=10)
        self.width_var = tk.StringVar(value="800")
        ttk.Entry(self.main_frame, textvariable=self.width_var, width=10).grid(row=1, column=1, sticky=tk.W, pady=10)

        ttk.Label(self.main_frame, text="Yükseklik:").grid(row=2, column=0, sticky=tk.W, pady=10)
        self.height_var = tk.StringVar(value="600")
        ttk.Entry(self.main_frame, textvariable=self.height_var, width=10).grid(row=2, column=1, sticky=tk.W, pady=10)

        # İşlem butonu
        ttk.Button(self.main_frame, text="Resimleri Boyutlandır", 
                  command=self.resize_images).grid(row=3, column=0, columnspan=3, pady=20)

        # İlerleme çubuğu
        self.progress = ttk.Progressbar(self.main_frame, mode='determinate')
        self.progress.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)

        # Log alanı
        self.log_text = tk.Text(self.main_frame, height=10, width=60)
        self.log_text.grid(row=5, column=0, columnspan=3, pady=10)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(self.main_frame, orient=tk.VERTICAL, command=self.log_text.yview)
        scrollbar.grid(row=5, column=3, sticky=(tk.N, tk.S))
        self.log_text.configure(yscrollcommand=scrollbar.set)

    def browse_folder(self):
        folder_path = filedialog.askdirectory()
        if folder_path:
            self.folder_path.set(folder_path)

    def show_about(self):
        about_text = """
        Image Resize v1.0
        
        Toplu resim boyutlandırma uygulaması.
        
        Geliştirici: Mustafa Önder Aköz
        
        İletişim & Sosyal Medya:
        GitHub: https://github.com/onder7
        LinkedIn: www.linkedin.com/in/mustafa-önder-aköz-23174592
        Medium: https://medium.com/@onder7
        Web: https://ondernet.net
        
        © 2024 Mustafa Önder Aköz - Tüm hakları saklıdır.
        """
        messagebox.showinfo("Hakkında", about_text)

    def show_features(self):
        features_text = """
        Özellikler:
        
        • Toplu resim boyutlandırma
        • Klasör seçme ve gözatma özelliği
        • Özel genişlik ve yükseklik ayarlama
        • İşlem ilerleme çubuğu
        • Detaylı işlem günlüğü
        • Hata yakalama ve kullanıcı bildirimleri
        • Desteklenen formatlar: JPEG, JPG, PNG
        """
        messagebox.showinfo("Özellikler", features_text)

    def resize_images(self):
        folder = self.folder_path.get()
        
        try:
            width = int(self.width_var.get())
            height = int(self.height_var.get())
        except ValueError:
            messagebox.showerror("Hata", "Genişlik ve yükseklik sayısal değer olmalıdır!")
            return

        if not folder:
            messagebox.showerror("Hata", "Lütfen bir klasör seçin!")
            return

        try:
            # Resim dosyalarını listele
            image_files = [f for f in os.listdir(folder) 
                         if f.lower().endswith(('.jpeg', '.jpg', '.png'))]
            
            if not image_files:
                messagebox.showinfo("Bilgi", "Seçili klasörde resim dosyası bulunamadı!")
                return

            # İlerleme çubuğunu ayarla
            self.progress['maximum'] = len(image_files)
            self.progress['value'] = 0
            
            # Log alanını temizle
            self.log_text.delete(1.0, tk.END)

            # Her resmi işle
            for i, filename in enumerate(image_files, 1):
                try:
                    img_path = os.path.join(folder, filename)
                    img = Image.open(img_path)
                    img = img.resize((width, height), Image.Resampling.LANCZOS)
                    
                    # Yeni dosya adı
                    new_filename = f"resized_{filename}"
                    new_path = os.path.join(folder, new_filename)
                    
                    # Resmi kaydet
                    img.save(new_path)
                    
                    # Log mesajı
                    log_msg = f"{i}. {filename} boyutlandırıldı -> {new_filename}\n"
                    self.log_text.insert(tk.END, log_msg)
                    self.log_text.see(tk.END)
                    
                    # İlerleme çubuğunu güncelle
                    self.progress['value'] = i
                    self.root.update()
                    
                except Exception as e:
                    self.log_text.insert(tk.END, f"HATA: {filename} işlenemedi: {str(e)}\n")
                    self.log_text.see(tk.END)

            messagebox.showinfo("Başarılı", "Tüm resimler boyutlandırıldı!")
            
        except Exception as e:
            messagebox.showerror("Hata", f"Bir hata oluştu: {str(e)}")
        
        finally:
            self.progress['value'] = 0

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageResizerGUI(root)
    root.mainloop()
