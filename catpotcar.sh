#!/bin/bash

# 获取用户的家目录的绝对路径
home_directory=$HOME

# 清空当前的POTCAR文件以准备生成新的POTCAR文件
> POTCAR

# 从POSCAR文件中读取第6行，移除额外的空格和非打印字符
element_string=$(awk 'NR==6' POSCAR | tr -d '[:cntrl:]' | tr -s ' ')

# 使用bash的IFS（internal field separator字段分隔符）对字符串进行分割
IFS=' ' read -ra element_array <<< "$element_string"

# 打印元素数组
printf "Elements: %s\n" "${element_array[*]}"

# 遍历所有元素，并且尝试将每个元素的POTCAR文件添加到全新的POTCAR文件上
for element in "${element_array[@]}"; do
    # 构建每个元素的POTCAR文件的路径
    potcar_path="$home_directory/POTCAR_database/PBE_POTCAR/PBE/$element/POTCAR"
    # 检查每个元素的POTCAR文件是否存在
    if [[ -f "$potcar_path" ]]; then
        # 如果存在，将该元素的POTCAR文件添加到全新的POTCAR文件
        cat "$potcar_path" >> POTCAR
        printf "Processed %s POTCAR\n" "$element"
    else 
        # 如果文件不存在，打印一个警告信息
        printf "Warning: POTCAR for %s does not exist at %s\n" "$element" "$potcar_path"
    fi
done

printf "Done.\n"
