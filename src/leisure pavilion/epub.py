# -*- coding: UTF-8 -*-

from zipfile import *
import re
import os

class epub:
    def __init__(self, epub_dir):
        self.epub_dir = epub_dir
        self.epub_name = os.path.split(self.epub_dir)[-1]

    def ex_epub(self):
        """Extract the ePub file"""
        self.epub = ZipFile(self.epub_dir)
        self.file_list = self.epub.namelist()
        for name in self.file_list:
            if not os.path.exists('cache'):
                os.mkdir('cache')
            f_path = os.path.split(name)
            if f_path[0] != '':
                if not os.path.exists('cache/' + f_path[0]):
                    os.makedirs('cache/' + f_path[0])
            with open('cache/' + name, mode='wb') as f_handle:
                f_handle.write(self.epub.read(name))
        self.epub.close()

if __name__ == "__main__":
    my_epub = epub("E:\坚果铺子\Book\epub\天命【高仿实体版】.epub")
    my_epub.ex_epub()




