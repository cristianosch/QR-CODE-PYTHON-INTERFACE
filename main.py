import qrcode
from PIL import Image, ImageDraw, ImageFont
import os
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import threading

class QRCodeGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("Gerador de QR Codes para Mesas")
        self.root.geometry("500x400")
        self.root.resizable(True, True)
        
        # Variáveis
        self.base_url = tk.StringVar(value="https://meusite.com/")
        self.num_tables = tk.IntVar(value=15)
        self.output_folder = tk.StringVar(value=os.getcwd())
        self.font_path = tk.StringVar(value="font/Ubuntu-B.ttf")
        self.is_generating = False
        
        self.create_widgets()
    
    def create_widgets(self):
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configurar grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Título
        title_label = ttk.Label(main_frame, text="Gerador de QR Codes", 
                               font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # URL base
        ttk.Label(main_frame, text="URL Base:").grid(row=1, column=0, sticky=tk.W, pady=5)
        url_entry = ttk.Entry(main_frame, textvariable=self.base_url, width=40)
        url_entry.grid(row=1, column=1, columnspan=2, sticky=(tk.W, tk.E), pady=5, padx=(5, 0))
        
        # Número de mesas
        ttk.Label(main_frame, text="Número de Mesas:").grid(row=2, column=0, sticky=tk.W, pady=5)
        tables_spinbox = ttk.Spinbox(main_frame, from_=1, to=1000, textvariable=self.num_tables, width=10)
        tables_spinbox.grid(row=2, column=1, sticky=tk.W, pady=5, padx=(5, 0))
        
        # Pasta de saída
        ttk.Label(main_frame, text="Pasta de Saída:").grid(row=3, column=0, sticky=tk.W, pady=5)
        ttk.Entry(main_frame, textvariable=self.output_folder, width=30).grid(row=3, column=1, sticky=(tk.W, tk.E), pady=5, padx=(5, 0))
        ttk.Button(main_frame, text="Procurar", command=self.browse_folder).grid(row=3, column=2, pady=5, padx=(5, 0))
        
        # Caminho da fonte
        ttk.Label(main_frame, text="Fonte:").grid(row=4, column=0, sticky=tk.W, pady=5)
        ttk.Entry(main_frame, textvariable=self.font_path, width=30).grid(row=4, column=1, sticky=(tk.W, tk.E), pady=5, padx=(5, 0))
        ttk.Button(main_frame, text="Procurar", command=self.browse_font).grid(row=4, column=2, pady=5, padx=(5, 0))
        
        # Botão gerar
        self.generate_btn = ttk.Button(main_frame, text="Gerar QR Codes", command=self.start_generation)
        self.generate_btn.grid(row=5, column=0, columnspan=3, pady=20)
        
        # Barra de progresso
        self.progress = ttk.Progressbar(main_frame, mode='determinate')
        self.progress.grid(row=6, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=5)
        
        # Label de status
        self.status_label = ttk.Label(main_frame, text="Pronto para gerar QR Codes")
        self.status_label.grid(row=7, column=0, columnspan=3, pady=5)
        
        # Frame de informações
        info_frame = ttk.LabelFrame(main_frame, text="Informações", padding="10")
        info_frame.grid(row=8, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)
        info_frame.columnconfigure(0, weight=1)
        
        info_text = """Os QR Codes serão gerados com:
        • Número da mesa no centro
        • Nome do arquivo: número.png
        • Formato: PNG
        • Os arquivos serão salvos na pasta selecionada"""
        
        ttk.Label(info_frame, text=info_text, justify=tk.LEFT).grid(row=0, column=0, sticky=tk.W)
    
    def browse_folder(self):
        folder = filedialog.askdirectory(initialdir=self.output_folder.get())
        if folder:
            self.output_folder.set(folder)
    
    def browse_font(self):
        filetypes = [
            ("Font files", "*.ttf *.otf"),
            ("All files", "*.*")
        ]
        font_file = filedialog.askopenfilename(
            title="Selecionar arquivo de fonte",
            filetypes=filetypes,
            initialdir=os.path.dirname(self.font_path.get()) if self.font_path.get() else os.getcwd()
        )
        if font_file:
            self.font_path.set(font_file)
    
    def start_generation(self):
        if self.is_generating:
            return
        
        # Validar entradas
        if not self.base_url.get().strip():
            messagebox.showerror("Erro", "Por favor, informe a URL base")
            return
        
        if self.num_tables.get() < 1:
            messagebox.showerror("Erro", "O número de mesas deve ser pelo menos 1")
            return
        
        if not os.path.exists(self.font_path.get()):
            messagebox.showerror("Erro", "Arquivo de fonte não encontrado")
            return
        
        # Criar pasta de saída se não existir
        if not os.path.exists(self.output_folder.get()):
            os.makedirs(self.output_folder.get())
        
        # Iniciar geração em thread separada para não travar a interface
        thread = threading.Thread(target=self.generate_qr_codes)
        thread.daemon = True
        thread.start()
    
    def generate_qr_codes(self):
        self.is_generating = True
        self.generate_btn.config(state='disabled')
        
        try:
            base_url = self.base_url.get().strip()
            num_tables = self.num_tables.get()
            output_folder = self.output_folder.get()
            font_path = self.font_path.get()
            
            # Configurar fonte
            font_size = 80
            try:
                font = ImageFont.truetype(font_path, font_size)
            except:
                # Fallback para fonte padrão se a selecionada falhar
                font = ImageFont.load_default()
                self.update_status("Usando fonte padrão (fonte selecionada não disponível)")
            
            # Configurar barra de progresso
            self.progress['maximum'] = num_tables
            self.progress['value'] = 0
            
            for table in range(1, num_tables + 1):
                if not self.is_generating:  # Permitir cancelamento
                    break
                
                url = f"{base_url}{table}"
                
                # Atualizar status
                self.update_status(f"Gerando QR Code para mesa {table}/{num_tables}")
                
                # Gerar QR Code
                qr = qrcode.QRCode(
                    version=1,
                    error_correction=qrcode.constants.ERROR_CORRECT_H,
                    box_size=10,
                    border=4,
                )
                qr.add_data(url)
                qr.make(fit=True)

                img = qr.make_image(fill_color="#555555", back_color="white").convert('RGB')
                w, h = img.size

                draw = ImageDraw.Draw(img)

                # Criar "espaço em branco" no centro do QR code
                box_size = 120
                left = (w - box_size) // 2
                top = (h - box_size) // 2
                right = left + box_size
                bottom = top + box_size
                draw.rectangle([left, top, right, bottom], fill="white")

                # Escrever o número da mesa dentro do quadrado branco
                text = str(table)
                bbox = draw.textbbox((0, 0), text, font=font)
                text_w = bbox[2] - bbox[0]
                text_h = bbox[3] - bbox[1]
                draw.text(((w - text_w) / 2, (h - text_h) / 2), text, font=font, fill="black")

                # Salvar arquivo
                filename = os.path.join(output_folder, f"{table}.png")
                img.save(filename)
                
                # Atualizar progresso
                self.progress['value'] = table
                self.root.update_idletasks()
            
            if self.is_generating:
                self.update_status(f"Concluído! {num_tables} QR Codes gerados em: {output_folder}")
                messagebox.showinfo("Sucesso", f"Geração concluída!\n{num_tables} QR Codes salvos em:\n{output_folder}")
            else:
                self.update_status("Geração cancelada")
                
        except Exception as e:
            self.update_status(f"Erro: {str(e)}")
            messagebox.showerror("Erro", f"Ocorreu um erro durante a geração:\n{str(e)}")
        
        finally:
            self.is_generating = False
            self.generate_btn.config(state='normal')
            self.progress['value'] = 0
    
    def update_status(self, message):
        self.status_label.config(text=message)
        self.root.update_idletasks()

def main():
    root = tk.Tk()
    app = QRCodeGenerator(root)
    root.mainloop()

if __name__ == "__main__":
    main()