#!/bin/bash

# Created by: ZLaoShi
# Last modified: 2025-03-06 17:02:54 UTC

# 字符映射规则：
# 0 => 空格 (space)
# 1 => I（大写字母I）
# 2 => l（小写字母l）
# 3 => |（竖线）
# 4 => ∣（U+2223）
# 5 => ╸（U+2578）
# 6 => ⏐（U+23D0）
# 7 => ｜（U+FF5C）

# 历史记录文件
HISTORY_FILE="${HOME}/.gun_history"

# 添加历史记录
add_to_history() {
    local text="$1"
    local oct_hash="$2"
    local gun_code="$3"
    local timestamp=$(date -u "+%Y-%m-%d %H:%M:%S UTC")
    
    # 创建目录和文件（如果不存在）
    mkdir -p "$(dirname "$HISTORY_FILE")"
    touch "$HISTORY_FILE"
    
    # 使用 { } 组合命令，确保一次性写入所有内容
    {
        echo "---"
        echo "时间: $timestamp"
        echo "文本: $text"
        echo "八进制: $oct_hash"
        echo "棍语言: $gun_code"
    } >> "$HISTORY_FILE"    # 使用 >> 进行追加
}

# 从历史记录中查找
search_history() {
    local search_hash="$1"
    if [ ! -f "$HISTORY_FILE" ]; then
        return 1
    fi
    
    # 修改 awk 脚本以支持多条记录
    awk -v hash="$search_hash" '
        BEGIN { found = 0 }
        /^---$/ { 
            if (record && found) {
                printf "%s", record
            }
            found = 0
            record = ""
        }
        { record = record $0 "\n" }
        /^八进制:/ && index($0, hash) { found = 1 }
        END { 
            if (record && found) {
                printf "%s", record
            }
        }
    ' "$HISTORY_FILE"
}

# 十六进制转二进制映射表
declare -A HEX_TO_BIN=(
    ['0']='0000' ['1']='0001' ['2']='0010' ['3']='0011'
    ['4']='0100' ['5']='0101' ['6']='0110' ['7']='0111'
    ['8']='1000' ['9']='1001' ['a']='1010' ['b']='1011'
    ['c']='1100' ['d']='1101' ['e']='1110' ['f']='1111'
)

# MD5哈希转换为8位棍语言的函数
str_to_oct_hash() {
    local text="$1"
    local extension=""
    
    # 只特殊处理 .md 扩展名
    if [[ "$text" == *.md ]]; then
        extension=".md"
        text="${text%.*}"
    fi
    
    # 生成文本的MD5哈希
    local hash_hex=$(echo -n "$text" | md5sum | cut -d' ' -f1)
    
    # 转换为二进制
    local binary=""
    for ((i=0; i<8; i++)); do
        local hex_char="${hash_hex:$i:1}"
        binary="${binary}${HEX_TO_BIN[${hex_char}]}"
    done
    
    # 每3位二进制转换为一个八进制数字
    local oct_result=""
    for ((i=0; i<24; i+=3)); do
        local group="${binary:$i:3}"
        while [ ${#group} -lt 3 ]; do
            group="${group}0"
        done
        # 手动计算三位二进制转八进制
        local val=$((
            ${group:0:1} * 4 +
            ${group:1:1} * 2 +
            ${group:2:1} * 1
        ))
        oct_result="${oct_result}${val}"
    done
    
    # 处理扩展名
    if [ -n "$extension" ]; then
        oct_result="${oct_result}${extension}"
    elif [[ "$1" == *.* ]]; then
        # 对于非 .md 文件，简单地对扩展名进行MD5并取前两位作为编码
        local ext="${1#*.}"
        local ext_hash=$(echo -n "$ext" | md5sum | cut -d' ' -f1)
        local ext_code="${ext_hash:0:2}"
        # 确保扩展名编码在0-7范围内
        local ext_val1=$((16#${ext_code:0:1} % 8))
        local ext_val2=$((16#${ext_code:1:1} % 8))
        oct_result="${oct_result}.${ext_val1}${ext_val2}"
    fi
    
    echo "$oct_result"
}

# 将八进制转换为棍语言
oct_to_gun() {
    local input="$1"
    
    # 只特殊处理 .md 扩展名
    if [[ "$input" == *.md ]]; then
        local main_part="${input%.*}"
        local gun_main=$(echo "$main_part" | sed -e 's/0/ /g' \
                                               -e 's/1/I/g' \
                                               -e 's/2/l/g' \
                                               -e 's/3/|/g' \
                                               -e 's/4/∣/g' \
                                               -e 's/5/╸/g' \
                                               -e 's/6/⏐/g' \
                                               -e 's/7/｜/g')
        echo "${gun_main}.md"
    else
        echo "$input" | sed -e 's/0/ /g' \
                           -e 's/1/I/g' \
                           -e 's/2/l/g' \
                           -e 's/3/|/g' \
                           -e 's/4/∣/g' \
                           -e 's/5/╸/g' \
                           -e 's/6/⏐/g' \
                           -e 's/7/｜/g'
    fi
}

# 将棍语言转换回八进制
gun_to_oct() {
    local input="$1"
    local main_part extension=""
    
    # 分离扩展名，特殊处理 .md
    if [[ "$input" == *.md ]]; then
        extension=".md"
        main_part="${input%.*}"
    elif [[ "$input" == *.* ]]; then
        main_part="${input%.*}"
        local ext_part="${input#*.}"
        
        # 先处理主要部分
        local main_oct=$(echo "$main_part" | sed -e 's/ /0/g' \
                                               -e 's/I/1/g' \
                                               -e 's/l/2/g' \
                                               -e 's/|/3/g' \
                                               -e 's/∣/4/g' \
                                               -e 's/╸/5/g' \
                                               -e 's/⏐/6/g' \
                                               -e 's/｜/7/g')
        
        # 对扩展名部分进行相同的转换
        local ext_oct=$(echo "$ext_part" | sed -e 's/ /0/g' \
                                             -e 's/I/1/g' \
                                             -e 's/l/2/g' \
                                             -e 's/|/3/g' \
                                             -e 's/∣/4/g' \
                                             -e 's/╸/5/g' \
                                             -e 's/⏐/6/g' \
                                             -e 's/｜/7/g')
        
        echo "${main_oct}.${ext_oct}"
        return
    else
        main_part="$input"
    fi
    
    local oct_str=$(echo "$main_part" | sed -e 's/ /0/g' \
                                         -e 's/I/1/g' \
                                         -e 's/l/2/g' \
                                         -e 's/|/3/g' \
                                         -e 's/∣/4/g' \
                                         -e 's/╸/5/g' \
                                         -e 's/⏐/6/g' \
                                         -e 's/｜/7/g')
    
    if [ -n "$extension" ]; then
        oct_str="${oct_str}${extension}"
    fi
    
    echo "$oct_str"
}

# 搜索历史记录
search_history() {
    local search_hash="$1"
    if [ ! -f "$HISTORY_FILE" ]; then
        return 1
    fi
    
    # 提取主要部分和扩展名部分（如果存在）
    local main_part ext_part
    if [[ "$search_hash" == *.* ]]; then
        main_part="${search_hash%.*}"
        ext_part="${search_hash#*.}"
    else
        main_part="$search_hash"
        ext_part=""
    fi
    
    awk -v hash="$main_part" -v ext="$ext_part" '
        BEGIN { found = 0; record = "" }
        /^---$/ {
            if (found) {
                printf "%s", record
            }
            record = $0 "\n"
            found = 0
            next
        }
        {
            record = record $0 "\n"
        }
        /^八进制:/ {
            # 提取八进制值并分离主要部分和扩展名
            split($0, parts, ": ")
            split(parts[2], hash_parts, ".")
            
            # 如果有扩展名，检查两部分都匹配
            if (ext != "") {
                if (hash_parts[1] == hash && index(parts[2], ext) > 0) {
                    found = 1
                }
            } else {
                # 如果没有扩展名，只检查主要部分
                if (hash_parts[1] == hash) {
                    found = 1
                }
            }
        }
        END {
            if (found) {
                printf "%s", record
            }
        }
    ' "$HISTORY_FILE"
}

# 显示历史记录
show_history() {
    if [ ! -f "$HISTORY_FILE" ]; then
        echo "没有找到历史记录"
        return 1
    fi
    
    echo "编码历史记录："
    local count=0
    local in_record=0
    local record=""
    
    while IFS= read -r line; do
        if [[ "$line" == "---" ]]; then
            if [ $in_record -eq 1 ]; then
                echo -e "$record"
            fi
            ((count++))
            echo -e "\n记录 #$count:"
            record=""
            in_record=1
        else
            record="${record}${line}\n"
        fi
    done < "$HISTORY_FILE"
    
    # 打印最后一条记录
    if [ $in_record -eq 1 ]; then
        echo -e "$record"
    fi
    
    if [ $count -eq 0 ]; then
        echo "暂无记录"
    else
        echo -e "\n共找到 $count 条记录"
    fi
}

# 显示使用方法
show_usage() {
    cat << EOF
棍语言编码器 v2.0 - 使用方法：
    编码文本:     $0 encode-text
    解码:         $0 decode
    显示历史:     $0 history
    清空历史:     $0 clear-history
    查看帮助:     $0 help

字符映射关系：
    0 => [空格]
    1 => I（大写字母I）
    2 => l（小写字母l）
    3 => |（竖线）
    4 => ∣（U+2223）
    5 => ╸（U+2578）
    6 => ⏐（U+23D0）
    7 => ｜（U+FF5C）
EOF
}

# 主函数
main() {
    if [ $# -lt 1 ]; then
        show_usage
        exit 1
    fi

    case "$1" in
        "encode-text")
            echo "请输入要编码的文本（支持中文）："
            read -r text
            if [ -z "$text" ]; then
                echo "错误：输入不能为空"
                exit 1
            fi
            oct_hash=$(str_to_oct_hash "$text")
            gun_code=$(oct_to_gun "$oct_hash")
            echo -e "\n编码结果："
            echo "输入文本: $text"
            echo "八进制值: $oct_hash"
            echo "棍语言码: $gun_code"
            
            # 添加到历史记录
            add_to_history "$text" "$oct_hash" "$gun_code"
            ;;
            
        "decode")
            echo "请输入棍语言代码："
            read -r gun_code
            if [ -z "$gun_code" ]; then
                echo "错误：输入不能为空"
                exit 1
            fi
            oct_str=$(gun_to_oct "$gun_code")
            echo -e "\n解码结果："
            echo "棍语言码: $gun_code"
            echo "八进制值: $oct_str"
            
            # 查找历史记录
            echo -e "\n查找历史记录..."
            if result=$(search_history "$oct_str"); then
                echo -e "找到匹配记录：\n$result"
            else
                echo "未找到对应的原始文本"
            fi
            ;;
        
        "history")
            show_history
            ;;
            
        "clear-history")
            rm -f "$HISTORY_FILE"
            echo "历史记录已清空"
            ;;
            
        "help")
            show_usage
            ;;
            
        *)
            echo "无效的命令"
            show_usage
            exit 1
            ;;
    esac
}

# 运行主函数
main "$@"