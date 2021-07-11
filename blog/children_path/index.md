> 小东西集合
# 文件工具
## 删除重复文件
- `file/file_filter.py` ，删除重复文件。 
- 应用场景： 假设我已经将相机中的部分相片分类放好，存在一个目录`existed_path`下（该目录可能有多个子目录）。 
  现在需要格式化存储卡，那么可以先将存储卡的全部照片拷贝出来，放到`new_path`目录下，执行`python file/file_filter.py existed_path new_path`。
  采用MD5摘要算法，构建文件信息时比较耗时。
- 个人感悟：为什么使用代码删除文件的时候很快？因为直接使用`os.remove`删除文件不用放到回收站。
![file_filter示例](./resources/file_filter.jpg)