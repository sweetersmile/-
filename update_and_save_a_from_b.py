
import re

def parse_file(file_path):
    """解析文件为字典格式"""
    data = {}
    with open(file_path, 'r') as f:
        for line in f:
            match = re.match(r'\s*(\w+)\s*=\s*"([^"]+)"\s*;', line)
            if match:
                key, value = match.groups()
                data[key] = value
    return data

def update_a_with_b(a_path, b_path):
    a_data = parse_file(a_path)
    b_data = parse_file(b_path)

    total_keys_a = len(a_data)
    total_keys_b = len(b_data)
    modified_count = 0

    # 替换 a 文件中的 value，如果在 b 中找到了相同的 key
    updated_lines = []
    with open(a_path, 'r') as f:
        for line in f:
            match = re.match(r'\s*(\w+)\s*=\s*"([^"]+)"\s*;', line)
            if match:
                key = match.group(1)
                old_value = match.group(2)
                new_value = b_data.get(key, old_value)
                if key in b_data and old_value != new_value:
                    modified_count += 1
                updated_line = f'{key} = "{new_value}";\n'
                updated_lines.append(updated_line)
            else:
                updated_lines.append(line)  # 保留非 key=value 的行

    # 保存结果到 a 文件
    with open(a_path, 'w') as f:
        f.writelines(updated_lines)

    # 输出统计信息
    print(f"总共 A 文件键数: {total_keys_a}")
    print(f"总共 B 文件键数: {total_keys_b}")
    print(f"A 文件中被修改的值数量: {modified_count}")

# 示例使用
if __name__ == "__main__":
    update_a_with_b('a.txt', 'b.txt')
