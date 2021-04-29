# coding:utf-8
# Created by Equator at 2021/4/29
import hashlib
import sys
import os


def get_file_md5(file_name):
    """
    计算文件的md5（处理较大文件）
    :param file_name:
    :return:
    """
    m = hashlib.md5()
    with open(file_name, 'rb') as file_obj:
        while True:
            data = file_obj.read(4096)
            if not data:
                break
            m.update(data)
    return m.hexdigest()


def get_file_meta_recursion(file_path):
    """
    递归获取文件名，返回文件MD5值与文件名集合
    :param file_path:
    :return:
    """
    file_name_dict = {}
    paths = os.listdir(file_path)
    for path in paths:
        full_path = os.path.join(file_path, path)
        if not os.path.exists(full_path):
            continue
        if os.path.isfile(full_path):
            file_md5 = get_file_md5(full_path)
            file_name_dict[file_md5] = full_path
            print(f"读取文件：{full_path}")
        else:
            children_file_name_set = get_file_meta_recursion(full_path)
            if children_file_name_set is not None:
                file_name_dict.update(children_file_name_set)
    return file_name_dict


def delete_existed_file_by_md5(existed_path, new_path):
    """
    通过文件名删除已经存在的文件：判断new_path下每一个文件是否存在existed_path目录下，是的话则删除
    :param existed_path: 已经存在的文件的目录，下面可以有很多子目录
    :param new_path: 一个新的文件集合的目录
    :return:
    """
    existed_file_meta_dict = get_file_meta_recursion(existed_path)
    new_file_meta_dict = get_file_meta_recursion(new_path)
    existed_file_md5_set = existed_file_meta_dict.keys()
    deleted_file_num = 0
    for new_file_md5, new_file_path in new_file_meta_dict.items():
        if new_file_md5 in existed_file_md5_set:
            print(f"删除重复文件：{new_file_path}")
            os.remove(new_file_path)
            deleted_file_num += 1
    print(f"总共删除文件数量：{deleted_file_num}")


def normalize_path(path):
    return path.replace('\\', os.sep)


if __name__ == '__main__':
    if len(sys.argv) == 1:
        raise Exception('请输入文件路径参数，分别为existed_path new_path')
    existed_path = normalize_path(sys.argv[1])
    new_path = normalize_path(sys.argv[2])
    print(f"existed_path：{existed_path}，new_path：{new_path}")
    delete_existed_file_by_md5(existed_path, new_path)
