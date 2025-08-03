#!/bin/bash

# 按顺序执行Python脚本，前一个成功才会执行下一个
python merge_configs.py && \
python find_duplicates.py && \
python split_semicolons.py

# 检查最后一个命令的执行结果
if [ $? -eq 0 ]; then
    echo "所有脚本执行成功"
else
    echo "脚本执行失败"
    exit 1
fi
    