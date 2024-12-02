题目描述：

这是1960年的拐小孩招数，但放到今天都依然可行。



提示：或许可以使用pyzipper和py7zr

flag：

```
r00t2024{cLos3_y0ur_3yE5}
```

wp：

这个压缩包套娃每一层的密码就是压缩包名，格式为7z或zip，于是就可以写出对应的脚本进行解压，或者直接对ai提出你的诉求让它来写，比如下面这个python脚本：

```
import os
import re
import pyzipper
import py7zr

# 从文件名中提取密码
def get_password_from_filename(filename):
    # 匹配文件名中的四位数字作为密码
    match = re.search(r'\b\d{4}\b', filename)
    return match.group() if match else None

# 使用文件名密码解压文件
def decompress_with_filename_password(file_path, output_dir):
    password = get_password_from_filename(os.path.basename(file_path))
    if password is None:
        print(f"No valid password found in filename {file_path}.")
        return False, None
    try:
        if file_path.endswith('.zip'):
            with pyzipper.AESZipFile(file_path) as zipf:
                zipf.setpassword(password.encode())
                zipf.extractall(output_dir)
            print(f"Success! Password for {file_path} is {password}")
            return True, os.path.join(output_dir, os.listdir(output_dir)[0])

        elif file_path.endswith('.7z'):
            with py7zr.SevenZipFile(file_path, password=password) as archive:
                archive.extractall(output_dir)
            print(f"Success! Password for {file_path} is {password}")
            return True, os.path.join(output_dir, os.listdir(output_dir)[0])

    except Exception as e:
        print(f"Failed to extract {file_path} with password {password}: {e}")
        return False, None

# 逐层解压缩
def decompress_multiple_layers(compressed_file, layers=1000):
    current_file = compressed_file
    output_base_dir = R"decompressed_files"  # 指定解压后的文件夹
    if not os.path.exists(output_base_dir):
        os.makedirs(output_base_dir)  # 如果目录不存在则创建

    for layer in range(layers):
        layer_output_dir = os.path.join(output_base_dir, f"layer_{layer + 1}")
        os.makedirs(layer_output_dir, exist_ok=True)

        success, next_file = decompress_with_filename_password(current_file, layer_output_dir)
        if not success:
            print(f"Unable to decrypt layer {layer + 1}. Exiting.")
            break

        print(f"Layer {layer + 1}: Successfully extracted.")
        current_file = next_file

        # 如果已达到解压完成的文件（非压缩文件），则停止
        if not (current_file.endswith('.zip') or current_file.endswith('.7z')):
            print("Reached final uncompressed file.")
            break

    print(f"Final extracted file path: {current_file}")

def main():
    final_compressed_file = R"5155.7z"  # 替换为最终生成的压缩文件路径
    decompress_multiple_layers(final_compressed_file, layers=1000)

if __name__ == '__main__':
    main()
```



解压1000层得到文件flag.zip，可以按照之前的格式用4位数字暴力破解，或者直接根据题目描述得到密码1960，解压后的txt中含有零宽度字符隐写，通过https://www.mzy0.com/ctftools/zerowidth1/解密得到flag。