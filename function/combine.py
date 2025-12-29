import os

# --- 配置部分 ---
# 排除不需要扫描的目录
exclude_dirs = {'.git', 'node_modules', '__pycache__', '.venv', 'dist', '.vscode', '.idea'}
# 定义支持的后缀及其对应的 Markdown 代码块语言标识
include_extensions = {
    '.py': 'python', '.js': 'javascript', '.ts': 'typescript', 
    '.c': 'c', '.cpp': 'cpp', '.java': 'java', 
    '.html': 'html', '.css': 'css', '.sh': 'bash', 
    '.md': 'markdown', '.json': 'json', '.sql': 'sql',
    '.xml': 'xml', '.yaml': 'yaml', '.yml': 'yaml'
}

def detect_language(file_path, ext):
    """
    智能检测代码块语言标签
    """
    if ext in include_extensions:
        return include_extensions[ext]
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            head = f.read(1000).lower()
            if "foamfile" in head or "c++" in head: return "cpp"
            if head.startswith("#!"):
                if "python" in head: return "python"
                if "sh" in head: return "bash"
    except: pass
    return "text"

def is_text_file(file_path):
    """
    强化版文本检测（过滤乱码/二进制文件）：
    1. 检查前 1024 字节是否包含空字符 \0 (二进制文件的典型特征)
    2. 尝试进行 utf-8 解码验证
    """
    try:
        with open(file_path, 'rb') as f:
            chunk = f.read(1024)
            if not chunk:
                return True # 空文件视为文本
            # 二进制文件（如 exe, pyc, jpg）通常包含 \0
            if b'\0' in chunk:
                return False
            # 尝试解码确认是否为文本
            chunk.decode('utf-8')
            return True
    except (UnicodeDecodeError, PermissionError):
        return False

def run_combine_logic(project_path, log_callback, progress_callback):
    """
    核心整合逻辑：扫描 -> 过滤 -> 合并 -> 进度反馈
    :param project_path: 源码根目录
    :param log_callback: GUI 日志刷新回调
    :param progress_callback: GUI 进度条刷新回调 (接收 0.0 到 1.0)
    :return: 生成的 Markdown 绝对路径
    """
    folder_name = os.path.basename(os.path.normpath(project_path))
    output_filename = f"{folder_name}.md"
    # 文件保存在用户选择的项目根目录下
    output_path = os.path.join(project_path, output_filename)
    
    valid_files = []
    log_callback(f"🔍 正在扫描并过滤乱码: {folder_name}")

    # 第一步：预扫描，计算需要处理的文件总数，以便计算进度
    all_potential_files = []
    for root, dirs, files in os.walk(project_path):
        dirs[:] = [d for d in dirs if d not in exclude_dirs]
        for file in files:
            if file == output_filename: continue # 不扫描自己
            full_path = os.path.join(root, file)
            ext = os.path.splitext(file)[1].lower()
            
            # 后缀匹配且通过文本特征检测
            if ext in include_extensions or (ext == ''):
                if is_text_file(full_path):
                    all_potential_files.append((full_path, os.path.relpath(full_path, project_path), ext))

    total_files = len(all_potential_files)
    if total_files == 0:
        log_callback("❌ 错误：未发现有效文本文件。")
        progress_callback(0)
        return None

    # 第二步：正式写入文件并反馈进度
    try:
        with open(output_path, 'w', encoding='utf-8') as outfile:
            # 写入标题和目录
            outfile.write(f"# {folder_name} Source Code Overview\n\n## Table of Contents\n\n")
            for _, rel, _ in all_potential_files:
                anchor = rel.replace(' ', '-').replace('.', '').replace('/', '').replace('\\', '').lower()
                outfile.write(f"- [{rel}](#file-{anchor})\n")
            outfile.write("\n---\n\n")

            # 遍历写入文件内容
            for i, (full, rel, ext) in enumerate(all_potential_files):
                # 更新进度条
                current_val = (i + 1) / total_files
                progress_callback(current_val)
                
                log_callback(f"📖 [{i+1}/{total_files}] 写入: {rel}")
                
                lang_tag = detect_language(full, ext)
                anchor_id = rel.replace(' ', '-').replace('.', '').replace('/', '').replace('\\', '').lower()
                
                outfile.write(f'<a name="file-{anchor_id}"></a>\n## File: {rel}\n\n```{lang_tag}\n')
                
                # 读取时使用 errors='ignore' 兜底，防止极个别特殊字符导致崩溃
                with open(full, 'r', encoding='utf-8', errors='ignore') as infile:
                    content = infile.read()
                    outfile.write(content)
                
                outfile.write("\n```\n\n[回到目录](#table-of-contents)\n\n---\n\n")
        
        log_callback(f"✨ 成功！已过滤乱码并生成 MD：\n{output_path}")
        return output_path
        
    except Exception as e:
        log_callback(f"❌ 写入失败: {str(e)}")
        return None