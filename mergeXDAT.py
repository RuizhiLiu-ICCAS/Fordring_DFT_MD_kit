def merge_files():
    # 让用户输入两个文件名和希望写出的文件名
    file1 = input("请输入第一个文件的名称（包括扩展名）：")
    file2 = input("请输入第二个文件的名称（包括扩展名）：")
    output = input("请输入输出文件的名称（包括扩展名）：")

    # 打开两个文件
    with open(file1, 'r') as f1, open(file2, 'r') as f2:
        lines1 = f1.readlines()
        lines2 = f2.readlines()

    # 计算两个文件中空行的数量
    empty_lines = lines1.count('\n') + lines2.count('\n')
    total_lines_files = len(lines1) + len(lines2) - empty_lines

    # 找到第一个文件中Direct configuration的最后一个值
    last_configuration1 = 0
    for line in reversed(lines1):
        if "Direct configuration" in line:
            last_configuration1 = int(line.split("=")[-1])
            break

    # 找到第二个文件中Direct configuration的最后一个值
    last_configuration2 = 0
    for line in reversed(lines2):
        if "Direct configuration" in line:
            last_configuration2 = int(line.split("=")[-1])
            break

    # 将第二个文件中的Direct configuration的值加上第一个文件中的最后一个值
    output_lines = [line for line in lines1 if line.strip() != ''] # 移除空行 
    actual_total_configs = last_configuration1
    for line in lines2:
        if "Direct configuration" in line:
            current_config = int(line.split("=")[-1])
            actual_total_configs = last_configuration1 + current_config
            line = "Direct configuration=     " + str(actual_total_configs) + '\n'
        if line.strip() != '':  # 移除空行
            output_lines.append(line)

    # 检查最后的Direct configuration数字和总的行数是否正确
    expected_total_configs = last_configuration1 + last_configuration2
    print(f"Expected total configurations: {expected_total_configs}")
    print(f"Actual total configurations: {actual_total_configs}")

    total_lines_result = len(output_lines)
    print(f"Expected total lines: {total_lines_files}")
    print(f"Actual total lines: {total_lines_result}")

    if expected_total_configs != actual_total_configs:
        print("错误：合并后的Direct configuration总数与预期不符。")
        
    if total_lines_files != total_lines_result:
        print("错误：合并后的文件总行数与预期不符。")

    # 将修改后的内容写入新文件
    with open(output, 'w') as f:
        f.writelines(output_lines)

merge_files()
