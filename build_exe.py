import PyInstaller.__main__
import sys
import os
import matplotlib

# 获取matplotlib的数据目录，这里包含了所需的字体文件
mpl_data_dir = os.path.dirname(matplotlib.__file__)
mpl_data_files = [(os.path.join(mpl_data_dir, 'mpl-data'), 'mpl-data')]

PyInstaller.__main__.run([
    'descaling_animation.py',  # 主程序文件
    '--name=BaihongDescaling',  # exe文件名
    '--onefile',  # 打包成单个文件
    '--noconsole',  # 不显示控制台窗口
    '--clean',  # 清理临时文件
    '--noupx',  # 不使用UPX压缩
    '--add-data={}/*.ttf;fonts/'.format(os.path.join(mpl_data_dir, 'mpl-data/fonts/ttf')),  # 添加字体文件
    '--hidden-import=numpy',
    '--hidden-import=matplotlib',
    '--hidden-import=tkinter',
    '--hidden-import=matplotlib.backends.backend_tkagg',
    '--hidden-import=matplotlib.font_manager'
]) 