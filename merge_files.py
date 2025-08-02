def read_key_value_pairs(file_path):
    """读取配置文件并返回键值对字典，不处理格式"""
    pairs = {}
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            items = [item.strip() for item in content.split(';') if item.strip()]
            
            for item in items:
                # 分割键和值（只考虑等号两边的空格）
                eq_index = item.find('=')
                if eq_index == -1:
                    continue
                    
                key_part = item[:eq_index].strip()
                value_part = item[eq_index+1:].strip()
                
                # 提取实际的键和值（去除引号）
                key = key_part.strip('"')
                value = value_part.strip('"')
                
                pairs[key] = {
                    'original_line': item,  # 原始行内容
                    'key_part': key_part,   # 原始键部分（包括可能的引号）
                    'value_part': value_part, # 原始值部分（包括可能的引号）
                    'value': value          # 实际值
                }
    except FileNotFoundError:
        print(f"错误：文件 {file_path} 未找到")
    except Exception as e:
        print(f"读取 {file_path} 时发生错误：{e}")
    return pairs

def read_values(file_path):
    """读取配置文件的值，用于比较"""
    values = {}
    pairs = read_key_value_pairs(file_path)
    for key, data in pairs.items():
        values[key] = data['value']
    return values

def update_a_file(a_path, b_values):
    """更新a文件，保持原有格式，只修改有变化的key"""
    a_pairs = read_key_value_pairs(a_path)
    if not a_pairs:
        print("a配置文件为空或无法读取，无法进行更新")
        return
    
    changed_keys = []
    
    # 读取原始内容
    with open(a_path, 'r', encoding='utf-8') as f:
        original_content = f.read()
    
    # 按分号分割但保留分隔符
    parts = []
    start = 0
    for i, c in enumerate(original_content):
        if c == ';':
            parts.append(original_content[start:i+1])  # 包含分号
            start = i+1
    if start < len(original_content):
        parts.append(original_content[start:])
    
    # 处理每个部分
    new_parts = []
    for part in parts:
        stripped = part.strip()
        if not stripped:
            new_parts.append(part)
            continue
            
        # 查找键
        eq_index = stripped.find('=')
        if eq_index == -1:
            new_parts.append(part)
            continue
            
        key = stripped[:eq_index].strip().strip('"')
        
        # 检查是否需要更新
        if key in b_values and key in a_pairs:
            old_value = a_pairs[key]['value']
            new_value = b_values[key]
            
            if old_value != new_value:
                # 提取原始格式
                key_part = a_pairs[key]['key_part']
                # 保持值的引号格式，只替换内容
                if a_pairs[key]['value_part'].startswith('"') and a_pairs[key]['value_part'].endswith('"'):
                    new_value_part = f'"{new_value}"'
                else:
                    new_value_part = new_value
                
                # 保持等号周围的空格
                original_line = a_pairs[key]['original_line']
                eq_pos = original_line.find('=')
                left_space = original_line[:eq_pos].replace(key_part, '')
                right_space = original_line[eq_pos+1:].replace(a_pairs[key]['value_part'], '')
                
                # 构建新行
                new_line = f"{key_part}{left_space}={right_space}{new_value_part}"
                
                # 替换部分内容
                part = part.replace(stripped, new_line.strip())
                changed_keys.append((key, old_value, new_value))
        
        new_parts.append(part)
    
    # 写回文件
    with open(a_path, 'w', encoding='utf-8') as f:
        f.write(''.join(new_parts))
    
    # 打印变化情况
    if changed_keys:
        print("\n以下键发生了更新：")
        for key, old_val, new_val in changed_keys:
            print(f"键 '{key}': 从 '{old_val}' 变为 '{new_val}'")
    else:
        print("\n没有键发生更新")
        
    print(f"已成功更新文件：{a_path}")

if __name__ == "__main__":
    # 配置文件路径
    a_file = "a.txt"
    b_file = "b.txt"
    
    # 读取b文件的键值对
    b_values = read_values(b_file)
    
    # 更新a文件
    update_a_file(a_file, b_values)
