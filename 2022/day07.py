from typing import List, Tuple, Optional, Type
from abc import ABC, abstractmethod
from dataclasses import dataclass
import helper


class FileSystemObject(ABC):

    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @property
    @abstractmethod
    def size(self) -> int:
        pass

    @property
    @abstractmethod
    def parent(self) -> Optional['FileSystemObject']:
        pass


class Directory(FileSystemObject):

    def __init__(self, name: str, parent: Optional['FileSystemObject']=None):
        self._name = name
        self._parent = parent
        self.contents: List['FileSystemObject'] = []
    
    def add_contents(self, object: 'FileSystemObject'):
        self.contents.append(object)

    @property
    def parent(self) -> Optional['Directory']:
        return self._parent

    @property
    def name(self) -> str:
        return self._name

    @property
    def size(self) -> int:
        total_size = sum(o.size for o in self.contents)
        return total_size

    def get(self, name: str, type: Type['FileSystemObject']) -> Optional['FileSystemObject']:
        objs = [o for o in self.contents if isinstance(o, type) and o.name == name] 
        return None if len(objs) == 0 else objs[0]


class File(FileSystemObject):
    def __init__(self, name: str, size: int, parent: Optional['FileSystemObject']=None):
        self._name = name
        self._size = size
        self._parent = parent
    
    @property
    def parent(self) -> Optional['Directory']:
        return self._parent 

    @property
    def name(self) -> str:
        return self._name

    @property
    def size(self) -> int:
        return self._size


def create_filesystem(input: List[str]) -> Directory:
    root = Directory('/')
    current_dir = root
    for line in input:
        if line.startswith('$ cd '):
            new_dir = line[5:]
            if new_dir == '/':
                current_dir = root
            elif new_dir == '..':
                current_dir = current_dir.parent
            elif new_dir := current_dir.get(new_dir, Directory):
                current_dir = new_dir
            else:
                new_dir = Directory(new_dir, current_dir)
                current_dir.add_contents(new_dir)
                current_dir = new_dir
        elif line.startswith('$ ls'):
            pass
        else:
            size_or_dir, name = line.split()
            if size_or_dir == 'dir' and not (obj := current_dir.get(name, Directory)):
                current_dir.add_contents(Directory(name, current_dir))
            elif size_or_dir != 'dir' and not (obj := current_dir.get(name, File)):
                current_dir.add_contents(File(name, int(size_or_dir), current_dir))
            else:
                raise ValueError(f'Invalid line: {line}')
    return root


def print_filesystem(root: Directory, indent: int=0):
    print(f'{" " * indent}- {root.name} (dir)')
    for o in root.contents:
        if isinstance(o, Directory):
            print_filesystem(o, indent + 2)
        else:
            print(f'{" " * (indent + 2)}- {o.name} (file, size={o.size})')


def find_directories_up_to_size(root: Directory, size: int=100000) -> List[Directory]:
    dirs = []
    if root.size < size:
        dirs.append(root)
    for o in root.contents:
        if isinstance(o, Directory):
            dirs.extend(find_directories_up_to_size(o, size))
    return dirs


def find_directories_with_at_least_size(root: Directory, size: int) -> List[Directory]:
    dirs = []
    if root.size >= size:
        dirs.append(root)
    for o in root.contents:
        if isinstance(o, Directory):
            dirs.extend(find_directories_with_at_least_size(o, size))
    return dirs


def directory_to_delete(root: Directory) -> Optional[Directory]:
    total_space = 70_000_000
    space_needed = 30_000_000
    current_free_space = total_space - root.size
    
    if current_free_space >= space_needed:
        return None

    dirs = find_directories_with_at_least_size(root, space_needed - current_free_space)

    if len(dirs) == 0:
        return None
    else:
        return min(dirs, key=lambda d: d.size)


if __name__ == '__main__':
    ### THE TESTS
    test_input = '''$ cd /
$ ls
dir a
14848514 b.txt
8504156 c.dat
dir d
$ cd a
$ ls
dir e
29116 f
2557 g
62596 h.lst
$ cd e
$ ls
584 i
$ cd ..
$ cd ..
$ cd d
$ ls
4060174 j
8033020 d.log
5626152 d.ext
7214296 k'''.split('\n')
    test_root = create_filesystem(test_input)
    print_filesystem(test_root)
    dirs = find_directories_up_to_size(test_root, 100000)
    assert sum(d.size for d in dirs) == 95437
    dir = directory_to_delete(test_root)
    assert dir.name == 'd'
    assert dir.size == 24933642

    ### THE REAL THING
    puzzle_input = helper.read_input_lines()
    root = create_filesystem(puzzle_input)
    dirs = find_directories_up_to_size(root, 100000)
    total_size = sum(d.size for d in dirs)
    print(f'Part 1: {total_size}')
    dir = directory_to_delete(root)
    print(f'Part 2: {dir.size}')
