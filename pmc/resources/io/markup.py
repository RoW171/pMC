__author__ = "Robin 'r0w' Weiland"
__date__ = "2019-02-24"
__version__ = "0.0.1"

from xml.etree import ElementTree
from pathlib import Path
# from battleships.resources.data import DataTypes

datatypes = DataTypes()


class ElementNotFound(Exception): pass


class AttributeNotFound(Exception): pass


class Element:
    def __init__(self, tag, text, attrib):
        self._tag = tag
        self._text = text
        self._attrib = attrib

    def __call__(self): return datatypes(self['dtype'])(self._text)

    def __getitem__(self, item):
        try: return self._attrib[item]
        except (KeyError,):
            raise AttributeNotFound('\'{attrib}\' is not an attribute of \'{tag}\''.format(attrib=item, tag=self._tag))

    def __getattribute__(self, item):
        try: return super().__getattribute__(item)
        except (AttributeError,):
            raise ElementNotFound('\'{element}\' is not an element of \'{tag}\''.format(element=item, tag=self._tag))

    def __setattr__(self, key, value):
        if key not in ['_tag', '_text', 'attrib']: raise NotImplementedError('READ-ONLY at the moment')

    __setitem__ = __setattr__

    def __len__(self): return len(self.__dict__) - 3

    def __repr__(self): return 'Element \'{}\''.format(self._tag)

    def __str__(self): return self._text.strip()

    def __bool__(self): return self._text != ''

    def __contains__(self, item): return item in self.__dict__ and item not in ['_tag', '_text', 'attrib']

    @property
    def tag(self): return self._tag

    @property
    def text(self): return self._text

    @property
    def attrib(self): return self._attrib


class XML:
    """READ-ONLY!!!"""
    def __init__(self, path):
        if not isinstance(path, Path): path = Path(path)
        if not path.is_file(): raise FileNotFoundError('XML file at \'{}\' not found'.format(path))
        self._parser = ElementTree.parse(path)
        root = self._parser.getroot()
        self.__dict__[root.tag] = Element(root.tag, root.text, root.attrib)
        self.traverse(self.__dict__[root.tag], root)

    def traverse(self, parent, element):
        for child in element:
            ne = Element(child.tag, child.text if child.text is not None else '', child.attrib)
            parent.__dict__[child.tag] = ne
            self.traverse(ne, child)

if __name__ == '__main__': pass
