def read_config(file_path):
    """读取配置文件并返回键值对字典"""
    config = {}
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            # 分割配置项（处理分号分隔的情况）
            items = [item.strip() for item in content.split(';') if item.strip()]
            
            for item in items:
                # 分割键和值
                parts = [part.strip() for part in item.split('=') if part.strip()]
                if len(parts) == 2:
                    key, value = parts
                    # 去除可能的引号
                    key = key.strip('"')
                    value = value.strip('"')
                    config[key] = value
    except FileNotFoundError:
        print(f"错误：文件 {file_path} 未找到")
    except Exception as e:
        print(f"读取 {file_path} 时发生错误：{e}")
    return config

def write_config(file_path, config):
    """将键值对字典写入配置文件"""
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            items = []
            for key, value in config.items():
                # 保持原始格式，用引号包裹值
                items.append(f'{key} = "{value}"')
            # 用分号分隔并添加最后的分号
            f.write('; '.join(items) + ';')
        print(f"已成功更新文件：{file_path}")
    except Exception as e:
        print(f"写入 {file_path} 时发生错误：{e}")

def merge_configs(a_path, b_path):
    """用b配置覆盖a配置中相同的键，并记录变化"""
    # 读取两个配置文件
    a_config = read_config(a_path)
    b_config = read_config(b_path)
    
    if not a_config:
        print("a配置文件为空或无法读取，无法进行合并")
        return
    
    # 记录发生变化的键
    changed_keys = []
    
    # 用b中的键值对覆盖a中的
    for key, value in b_config.items():
        if key in a_config:
            old_value = a_config[key]
            if old_value != value:  # 只有当值不同时才记录变化
                a_config[key] = value
                changed_keys.append((key, old_value, value))
    
    # 打印变化情况
    if changed_keys:
        print("\n以下键发生了更新：")
        for key, old_val, new_val in changed_keys:
            print(f"键 '{key}': 从 '{old_val}' 变为 '{new_val}'")
    else:
        print("\n没有键发生更新")
    
    # 写回a文件
    write_config(a_path, a_config)

if __name__ == "__main__":
    # 配置文件路径
    a_file = "a.txt"
    b_file = "b.txt"
    
    # 执行合并操作
    merge_configs(a_file, b_file)
    
