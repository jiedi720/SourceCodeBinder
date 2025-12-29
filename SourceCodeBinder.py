from gui.main_gui import CodeBinderGUI
from function.combine import run_combine_logic
from function.pdf import run_pdf_logic

if __name__ == "__main__":
    # 启动应用，将两个功能函数传入 GUI
    app = CodeBinderGUI(run_combine_logic, run_pdf_logic)
    app.mainloop()