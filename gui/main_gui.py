import threading
import os
import subprocess
import platform
from tkinter import filedialog
import customtkinter as ctk

class CodeBinderGUI(ctk.CTk):
    def __init__(self, combine_func, pdf_func):
        super().__init__()
        self.combine_func = combine_func
        self.pdf_func = pdf_func
        self.last_md_path = None  # 记录生成的 MD 文件路径
        
        # 窗口设置
        self.title("SourceCodeBinder")
        self.width, self.height = 750, 650
        self.center_window()
        
        ctk.set_appearance_mode("dark")
        self.grid_columnconfigure((0, 1), weight=1) 
        self.grid_rowconfigure(4, weight=1)

        # 1. 标题
        self.label = ctk.CTkLabel(self, text="📁 SourceCodeBinder", font=("Arial", 24, "bold"))
        self.label.grid(row=0, column=0, columnspan=2, pady=20)

        # 2. 路径选择区 (修改点：增加“打开”按钮)
        self.frame = ctk.CTkFrame(self)
        self.frame.grid(row=1, column=0, columnspan=2, padx=20, pady=5, sticky="ew")
        self.frame.grid_columnconfigure(0, weight=1)
        
        self.entry = ctk.CTkEntry(self.frame, placeholder_text="请选择项目根目录...")
        self.entry.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        
        # 打开文件夹按钮
        self.btn_open = ctk.CTkButton(self.frame, text="打开", width=60, fg_color="#4a4a4a", hover_color="#666666", command=self.open_folder)
        self.btn_open.grid(row=0, column=1, padx=(5, 5), pady=10)
        
        # 浏览按钮
        self.btn_browse = ctk.CTkButton(self.frame, text="浏览", width=60, command=self.browse)
        self.btn_browse.grid(row=0, column=2, padx=(5, 10), pady=10)

        # 3. 进度条及百分比显示区
        self.progress_label = ctk.CTkLabel(self, text="等待开始: 0%", font=("Arial", 13))
        self.progress_label.grid(row=2, column=0, columnspan=2, padx=25, pady=(10, 12), sticky="w")
        
        self.progress_bar = ctk.CTkProgressBar(self, orientation="horizontal")
        self.progress_bar.grid(row=2, column=0, columnspan=2, padx=20, pady=(35, 10), sticky="ew")
        self.progress_bar.set(0)

        # 4. 按钮区 - 并排两个按钮
        self.btn_combine = ctk.CTkButton(self, text="合并为Markdown", height=45, fg_color="#2c6e49", command=self.start_combine)
        self.btn_combine.grid(row=3, column=0, padx=(20, 10), pady=15, sticky="ew")

        self.btn_pdf = ctk.CTkButton(self, text="导出为PDF", height=45, fg_color="#1f538d", command=self.start_pdf)
        self.btn_pdf.grid(row=3, column=1, padx=(10, 20), pady=15, sticky="ew")

        # 5. 日志区
        self.log_box = ctk.CTkTextbox(self, font=("Consolas", 13))
        self.log_box.grid(row=4, column=0, columnspan=2, padx=20, pady=(0, 20), sticky="nsew")

    def center_window(self):
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width // 2) - (self.width // 2)
        y = (screen_height // 2) - (self.height // 2)
        self.geometry(f"{self.width}x{self.height}+{x}+{y}")

    def log(self, msg):
        self.after(0, lambda: self._update_log(msg))

    def _update_log(self, msg):
        self.log_box.insert("end", f"{msg}\n")
        self.log_box.see("end")

    def update_progress(self, val):
        self.after(0, lambda: self._set_progress(val))

    def _set_progress(self, val):
        self.progress_bar.set(val)
        self.progress_label.configure(text=f"当前进度: {int(val * 100)}%")

    def browse(self):
        path = filedialog.askdirectory()
        if path:
            self.entry.delete(0, "end")
            self.entry.insert(0, path)

    def open_folder(self):
        """打开输入框中指定的文件夹"""
        path = self.entry.get().strip()
        if not path or not os.path.exists(path):
            self.log("⚠️ 路径不存在，无法打开！")
            return
        
        try:
            # 根据系统平台调用不同的资源管理器打开指令
            current_os = platform.system()
            if current_os == "Windows":
                os.startfile(path)
            elif current_os == "Darwin":  # macOS
                subprocess.Popen(["open", path])
            else:  # Linux
                subprocess.Popen(["xdg-open", path])
        except Exception as e:
            self.log(f"❌ 无法打开文件夹: {str(e)}")

    def start_combine(self):
        path = self.entry.get().strip()
        if not path:
            self.log("⚠️ 请先选择路径！")
            return
        self.update_progress(0)
        self.btn_combine.configure(state="disabled")
        threading.Thread(target=self._run_combine, args=(path,), daemon=True).start()

    def _run_combine(self, path):
        try:
            self.last_md_path = self.combine_func(path, self.log, self.update_progress)
        except Exception as e:
            self.log(f"❌ 运行异常: {str(e)}")
        finally:
            self.btn_combine.configure(state="normal")

    def start_pdf(self):
        if not self.last_md_path:
            self.log("⚠️ 请先完成步骤 ① 合并代码！")
            return
        self.btn_pdf.configure(state="disabled")
        self.progress_bar.configure(mode="indeterminate")
        self.progress_bar.start()
        threading.Thread(target=self._run_pdf, daemon=True).start()

    def _run_pdf(self):
        try:
            self.pdf_func(self.last_md_path, self.log)
        finally:
            self.progress_bar.stop()
            self.progress_bar.configure(mode="determinate")
            self.update_progress(1.0)
            self.btn_pdf.configure(state="normal")