def find_duplicate_keys(file_path):
    """
    查找文件中重复的key，并返回这些key及其所有value
    """
    # 存储所有key的信息，格式: {key: [value1, value2, ...]}
    key_values = {}
    # 存储每行的原始内容，用于定位重复项
    line_contents = []
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            # 按行读取并处理
            for line_num, line in enumerate(f, 1):
                # 去除首尾空白和分号
                stripped_line = line.strip().rstrip(';').strip()
                if not stripped_line:
                    continue
                
                # 记录原始行内容
                line_contents.append((line_num, line.strip()))
                
                # 查找等号位置
                eq_index = stripped_line.find('=')
                if eq_index == -1:
                    continue  # 跳过没有等号的行
                
                # 提取key和value部分
                key_part = stripped_line[:eq_index].strip()
                value_part = stripped_line[eq_index+1:].strip()
                
                # 去除可能的引号
                key = key_part.strip('"')
                value = value_part.strip('"')
                
                # 添加到字典中
                if key in key_values:
                    key_values[key].append((value, line_num))
                else:
                    key_values[key] = [(value, line_num)]
    
    except FileNotFoundError:
        print(f"错误：文件 {file_path} 未找到")
        return None
    except Exception as e:
        print(f"处理文件时发生错误：{e}")
        return None
    
    # 筛选出重复的key
    duplicate_keys = {k: v for k, v in key_values.items() if len(v) > 1}
    return duplicate_keys

def print_duplicates(duplicate_keys, file_path):
    """打印重复的key及其value"""
    if not duplicate_keys:
        print(f"文件 {file_path} 中没有重复的key")
        return
    
    print(f"文件 {file_path} 中发现以下重复的key：\n")
    for key, values in duplicate_keys.items():
        print(f"key: '{key}' 出现 {len(values)} 次，对应的值为：")
        for value, line_num in values:
            print(f"  行号 {line_num}: {value}")
        print()  # 空行分隔不同的key

if __name__ == "__main__":
    # 要检查的文件路径
    file_to_check = "a.txt"
    
    # 查找重复的key
    duplicates = find_duplicate_keys(file_to_check)
    
    # 打印结果
    if duplicates is not None:
        print_duplicates(duplicates, file_to_check)
    