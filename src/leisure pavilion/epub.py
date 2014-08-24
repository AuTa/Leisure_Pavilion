# -*- coding: UTF-8 -*-

from zipfile import *
import xml.etree.ElementTree as ET
import hashlib
import re
import os

def get_namespace(element):
    try:
        m = re.match('\{.*\}', element.tag)
    except:
        m = re.match('\{.*\}', element)
    return m.group(0) if m else ''

class epub:
    def __init__(self, epub_dir):
        self.epub_dir = epub_dir
        self.epub_name = os.path.split(self.epub_dir)[-1]

    def get_md5(self):
        """Get the ePub's md5"""
        self.epub_md5 = hashlib.md5()
        with open(self.epub_dir, 'rb') as f:
            self.epub_md5.update(f.read())
        return self.epub_md5.hexdigest()


    def ex_epub(self):
        """Extract the ePub file"""
        self.cache_path = 'cache/' + self.get_md5() + '/'
        self.epub = ZipFile(self.epub_dir)
        self.file_list = self.epub.namelist()
        for name in self.file_list:
            if not os.path.exists(self.cache_path):
                os.mkdir(self.cache_path)
            f_path = os.path.split(name)
            if f_path[0] != '':
                if not os.path.exists(self.cache_path + f_path[0]):
                    os.makedirs(self.cache_path + f_path[0])
            with open(self.cache_path + name, mode='wb') as f_handle:
                f_handle.write(self.epub.read(name))
        self.epub.close()

    def get_info(self):
        # self.ex_epub()
        self.cache_path = 'cache/' + self.get_md5() + '/'
        container_tree = ET.ElementTree(file=self.cache_path + 'META-INF/container.xml')
        container_namespace = get_namespace(container_tree.getroot())
        container_rootfile = container_tree.find('.//{0}rootfile'.format(container_namespace)) # '.' + '//'
        opf_path = '{0}/{1}'.format(self.cache_path, container_rootfile.get('full-path'))
        opf_tree = ET.ElementTree(file=opf_path)
        opf_namespace = get_namespace(opf_tree.getroot())
        dc_namespace = get_namespace(opf_tree.find('.//{0}metadata/*'.format(opf_namespace)))
        metadata_tree = opf_tree.findall('.//{0}metadata/*'.format(opf_namespace))
        metadate_dic = {}
        for elem in metadata_tree:
            elem_namespace = get_namespace(elem)
            if elem_namespace == dc_namespace:
                elem_tag = elem.tag.split(elem_namespace)[1]
                elem_attrib = elem.items()
                for i in range(0, len(elem_attrib)):
                    elem_attrib_list = list(elem_attrib[i])
                    i_ns = get_namespace(elem_attrib_list[0])
                    if i_ns:
                        fact_key = elem_attrib_list[0].split(i_ns)[1]
                        elem_attrib_list[0] = fact_key
                        elem_attrib = tuple(elem_attrib_list)
                elem_text = elem.text
                metadate_dic.update({elem_tag:[elem_attrib, elem_text]})
        return metadate_dic


if __name__ == "__main__":
    my_epub = epub("E:\坚果铺子\Book\epub\天命【高仿实体版】.epub")
    my_epub.get_info()




