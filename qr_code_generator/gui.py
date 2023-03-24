import tkinter as tk

from tkinter import filedialog

from PIL import ImageTk, Image

import qrcode
class QRCodeGenerator:

    def __init__(self, master):
        self.master = master
        master.title("QR Kodu Oluşturucu")

        self.url_label = tk.Label(master, text="URL:")
        self.url_label.grid(row=0, column=0, padx=5, pady=5)

        self.url_entry = tk.Entry(master)
        self.url_entry.grid(row=0, column=1, padx=5, pady=5)

        self.logo_label = tk.Label(master, text="Logo Dosyası:")
        self.logo_label.grid(row=1, column=0, padx=5, pady=5)

        self.logo_entry = tk.Entry(master)
        self.logo_entry.grid(row=1, column=1, padx=5, pady=5)

        self.browse_button = tk.Button(master, text="Gözat", command=self.browse_logo)
        self.browse_button.grid(row=1, column=2, padx=5, pady=5)        
        self.output_label = tk.Label(master, text="Çıktı Dosyası:")
        self.output_label.grid(row=2, column=0, padx=5, pady=5)

        self.output_entry = tk.Entry(master)
        self.output_entry.grid(row=2, column=1, padx=5, pady=5)
        self.output_entry.insert(0, "qr_code.png")

        self.generate_button = tk.Button(master, text="QR Kodu Oluştur", command=self.generate_qr_code)
        self.generate_button.grid(row=3, column=1, padx=5, pady=5)

    def browse_logo(self):
        logo_path = filedialog.askopenfilename(initialdir=".", title="Logo Seç", filetypes=[("PNG dosyaları", "*.png")])
        self.logo_entry.delete(0, tk.END)
        self.logo_entry.insert(0, logo_path)

    def generate_qr_code(self):
        url = self.url_entry.get()
        logo_path = self.logo_entry.get()
        output_path = self.output_entry.get()

        if not url:
            tk.messagebox.showerror("Hata", "Lütfen bir URL girin.")
            return

        try:
            qr = qrcode.QRCode(
                version=1,
                box_size=10,
                border=5
            )

            qr.add_data(url)
            qr.make(fit=True)

            img = qr.make_image(fill_color="black", back_color="white")

            if logo_path:
                try:
                    logo_img = qrcode.image(Image.open(logo_path))
                    img.paste(logo_img, (img.size[0]//2-logo_img.size[0]//2, img.size[1]//2-logo_img.size[1]//2))
                except Exception as e:
                    tk.messagebox.showerror("Hata", f"Logo eklenirken hata oluştu: {e}")
                    return

            img.save(output_path)
            tk.messagebox.showinfo("Başarılı", "QR kodu başarıyla oluşturuldu.")

        except Exception as e:
            tk.messagebox.showerror("Hata", f"QR kodu oluşturulurken hata oluştu: {e}")
            return


if __name__ == '__main__':
    root = tk.Tk()
    gui = QRCodeGenerator(root)
    root.mainloop()