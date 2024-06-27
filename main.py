import py_compile
import sys
import os

from pathlib import Path


def my_xor(data):
    """
    加密
    :param data:
    :return:
    """
    key = b"你的加密key"
    i = 0
    n_data = list(data)
    k_len = len(key)
    for v in data:
        n_data[i] = (v ^ key[i % k_len])
        i += 1
    return bytes(n_data)


def pyc2pye(pyc_path):
    """
    将加密过的pyc文件转换成专用的pye格式
    :param pyc_path:
    :return:
    """
    global file_count
    pe_header = "你的pe头的值"
    pye_path = pyc_path.replace(".pyc", ".pye")
    print("INFO: 正在转换" + pyc_path + "->" + Path(pye_path).name)
    try:
        with open(pyc_path, "rb") as pyc:
            pyc_bytes = pyc.read()
        with open(pye_path, "wb") as pe:
            pe.write(bytes.fromhex(pe_header))
            pe.write(my_xor(pyc_bytes))
        os.remove(pyc_path)
    except Exception as e:
        raise e


def compile_py(paths):
    for path in paths:
        if not Path(path).exists():
            print(path)
            print("ERROR: 输入路径不存在，请仔细检查！")
            return
        p = Path(path)
        p_name = str(path)
        if p_name.endswith("__pycache__") or p.name.startswith("."):
            continue
        if p.is_file() and p_name.endswith("py"):
            print("INFO:正在编译" + p_name + "->" + p.name + "c")
            try:
                py_compile.compile(p_name, p_name + "c")
                if not os.path.exists(p_name + "c"):
                    print("编译失败请检查文件夹读写权限")
                os.remove(p_name)
            except Exception as e:
                print("编译失败请检查文件夹读写权限")
                print(e)
                sys.exit(0)
            pyc2pye(p_name + "c")
        elif p.is_dir():
            compile_py(p.iterdir())


if __name__ == '__main__':
    compile_py(["文件或者项目的地址"])