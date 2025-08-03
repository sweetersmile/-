def format_a_with_semicolon():
    """处理a.txt文件，遇到分号就换行，处理后覆盖原文件"""
    filename = "a.txt"
    
    try:
        # 读取文件内容
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 处理分号换行逻辑
        # 先替换"; "为";\n"，再处理单独的";"
        formatted = content.replace('; ', ';\n').replace(';', ';\n')
        
        # 去除空行并保持每行内容整洁
        lines = [line.strip() for line in formatted.split('\n') if line.strip()]
        result = '\n'.join(lines)
        
        # 写回原文件
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(result)
        
        print(f"文件 '{filename}' 已格式化，分号后已自动换行")
        
    except FileNotFoundError:
        print(f"错误：文件 '{filename}' 不存在")
    except Exception as e:
        print(f"处理文件时出错：{e}")

if __name__ == "__main__":
    format_a_with_semicolon()
    