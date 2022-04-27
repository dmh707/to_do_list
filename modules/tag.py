#collect the list
#sort list into tags
#update list.txt
from typing import Dict
try:
    from generate_list import Main as List
except:
    from modules.generate_list import Main as List

class Main():
    def __init__(self) -> None:
        self.tags = self.get_tags()
        self.update_mainlist_file()
    def get_tags(self):
        pre_tag_list = List().list
        current_tag = ''
        tags=dict()
        for line in pre_tag_list:
            if len(line):
                if line[0]=='-':
                    current_tag=line
                    if current_tag not in tags:
                        tags[current_tag]=[]
                else:

                    tags[current_tag].append(line)
        return tags
    def clear_empty(self):
        tag_copy = self.tags.copy()
        for tag,lyst in self.tags.items():
            if not len(lyst):
                tag_copy.pop(tag)
        self.tags=tag_copy
    def update_mainlist_file(self):
        filename='.\list.txt'
        self.clear_empty()
        tags = list(self.tags.keys())
        tags.sort()
        with open(filename,'w') as f:
            for tag in tags:
                lyst=self.tags[tag]
                f.write(tag)
                f.write('\n')
                for line in lyst:
                    f.write(line)
                    f.write('\n')
                f.write('\n')
if __name__ == '__main__':
    print(Main().tags)