# coding:utf-8
# Created by Equator at 2021/4/29
import hashlib
import sys
import os
import time

handle_file_count = 0


def get_file_md5(file_path):
    """
    计算文件的md5（处理较大文件）
    :param file_path:
    :return:
    """
    m = hashlib.md5()
    with open(file_path, 'rb') as file_obj:
        while True:
            data = file_obj.read(4096)
            if not data:
                break
            m.update(data)
    return m.hexdigest()


def get_file_create_time(file_path):
    timestamp = os.path.getctime(file_path)
    return time.strftime("%Y%m%d%H%M%S", time.localtime(timestamp))


def get_file_meta_recursion(file_path):
    """
    递归获取文件名，返回文件元数据列表
    :param file_path:
    :return:
    """
    file_meta_list = []
    paths = os.listdir(file_path)
    for path in paths:
        full_path = os.path.join(file_path, path)
        if not os.path.exists(full_path):
            continue
        if os.path.isfile(full_path):
            global handle_file_count
            handle_file_count += 1
            print(f"scan file：{full_path}, count {handle_file_count}")

            file_md5 = get_file_md5(full_path)
            file_create_time = get_file_create_time(full_path)

            file_meta_list.append({
                'full_path': full_path,
                'file_md5': file_md5,
                'file_create_time': file_create_time,
                'file_ext_arr': os.path.splitext(full_path)
            })
        else:
            children_file_meta_list = get_file_meta_recursion(full_path)
            if children_file_meta_list is not None:
                file_meta_list += children_file_meta_list
    return file_meta_list


def normalize_path(path):
    return path.replace('\\', os.sep)


if __name__ == '__main__':
    if len(sys.argv) < 1:
        raise Exception('请输入文件路径参数')

    target_path = normalize_path(sys.argv[1])

    print(f"rename_by_create_time_md5 target_path：{target_path}")

    file_meta_list = get_file_meta_recursion(target_path)

    for file_meta in file_meta_list:
        # new_file_name = f"{file_meta['file_create_time']}_{file_meta['file_md5']}{file_meta['file_ext_arr'][1]}"
        new_file_name = f"{file_meta['file_md5']}{file_meta['file_ext_arr'][1]}"
        file_path_without_ext = file_meta['file_ext_arr'][0]
        new_file_path = file_path_without_ext[0:file_path_without_ext.rindex(os.sep)] + os.sep + new_file_name
        current_file_path = file_meta['full_path']
        print(f"rename_by_create_time_md5 rename {current_file_path} to {new_file_path}")

        if current_file_path == new_file_path:
            # 名字已是符合格式的，跳过
            print(f"rename_by_create_time_md5 skip {current_file_path}")
            continue

        if os.path.exists(new_file_path):
            print(f"rename_by_create_time_md5 delete file {new_file_path}")
            os.remove(new_file_path)

        os.rename(current_file_path, new_file_path)
