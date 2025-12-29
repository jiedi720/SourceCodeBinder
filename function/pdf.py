import os
import markdown2
import pdfkit

def run_pdf_logic(md_path, log_callback):
    """
    PDF 转换逻辑模块
    :param md_path: 合并后的 .md 文件绝对路径（由 combine 逻辑返回）
    :param log_callback: 日志回调函数
    """
    # 检查 MD 文件是否存在
    if not md_path or not os.path.exists(md_path):
        log_callback("⚠️ 错误：未找到生成的 Markdown 文件！请确保已先执行“整合为 Markdown”。")
        return

    # 定义生成的 PDF 路径（将 .md 替换为 .pdf，路径保持在源目录）
    pdf_path = md_path.replace(".md", ".pdf")
    log_callback(f"⏳ 正在转换 PDF，请稍候...")

    # 指定 wkhtmltopdf 的安装路径
    config = pdfkit.configuration(wkhtmltopdf=r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe")

    try:
        with open(md_path, 'r', encoding='utf-8') as f:
            md_content = f.read()
            # 将 Markdown 转换为带有扩展功能的 HTML
            html_body = markdown2.markdown(md_content, extras=["fenced-code-blocks", "tables", "break-on-newline"])
            
            # 注入精美样式
            full_html = f"""
            <html>
            <head><meta charset="UTF-8"><style>
                body {{ font-family: 'Segoe UI', Arial, sans-serif; padding: 40px; line-height: 1.6; color: #333; }}
                pre {{ background: #f6f8fa; padding: 16px; border-radius: 6px; border: 1px solid #ddd; white-space: pre-wrap; font-size: 12px; }}
                code {{ font-family: 'Consolas', 'Courier New', monospace; color: #000; }}
                h2 {{ border-bottom: 2px solid #eaecef; padding-bottom: 5px; margin-top: 40px; color: #0366d6; }}
                a {{ color: #0366d6; text-decoration: none; }}
                ul {{ background: #f1f8ff; padding: 20px 40px; border-radius: 8px; }}
            </style></head>
            <body>{html_body}</body>
            </html>
            """
            
            # 使用指定配置执行转换
            pdfkit.from_string(full_html, pdf_path, configuration=config)
            log_callback(f"🚀 成功！PDF 已生成在源目录：\n{pdf_path}")
            
    except Exception as e:
        log_callback(f"❌ PDF 转换失败: {str(e)}")