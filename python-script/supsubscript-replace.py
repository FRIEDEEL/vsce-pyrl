import argparse

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("content",help="string to be converted",type=str)
    line=parser.parse_args().content
    print(replace_line(line))

class BracketTree(object):
    def __init__(self,outer=None) -> None:
        self.content=[]
        self.parent=None
        self.child=[]
        self.outer_bracket=outer
        # outer should be a tuple of a pair of brackets
    
    def gen_list(self):
        ls=[]
        for item in self.content:
            if isinstance(item,BracketTree):
                ls.append(item)
            elif isinstance(item,str):
                ls.extend(list(item))
        return ls

    def append_child(self,child):
        self.content.append(child)

    def append_string(self,string:str):
        self.content.append(string)

    def __str__(self) -> str:
        s="".join(map(str,self.content))
        if self.outer_bracket:
            s=self.outer_bracket[0]+s+self.outer_bracket[1]
        return s

def bracket_match(char:str):
    """return the matching bracket of the given one.

    For example, if '[' is given to the func, it returns ']'. And if '}' is given,
    it returns '{'.

    Raises ValueError if non-bracket, or string with length over 1 is given.
    """
    bracket_set=("[","]",
               "(",")",
               "{","}",)
    if char not in bracket_set:
        raise ValueError('{char} is not a bracket.'.format(char=char))
    else:
        idx=bracket_set.index(char)
        return bracket_set[idx^1]

def _bracket_match(char):
    bracket_set=("[","]","(",")","{","}",)
    return bracket_set[bracket_set.index(char)^1]

def bracket_parse(origin:str,outer=None):
    listed=list(origin)
    tree=BracketTree(outer)

    esc_flag=False
    p_stack=[] # stack of bracket
    temp_inside=[]
    
    for ptr in listed:
        temp_inside.append(ptr)

        if esc_flag:
            esc_flag=False
            continue
        elif ptr=="\\":
            esc_flag=True
            continue
        elif ptr in ("{"):
            if len(p_stack)==0:
                temp_inside.pop()
                if len(temp_inside)>0:
                    tree.append_string("".join(temp_inside))
                temp_inside=[]
            p_stack.append(ptr)
            continue
        elif ptr in ("}"):
            if p_stack.pop()!=bracket_match(ptr):
                raise Exception() # TODO: adjust this
            else:
                if len(p_stack)==0:
                    temp_inside.pop()
                    if len(temp_inside)>0:
                        child=bracket_parse("".join(temp_inside),outer=(bracket_match(ptr),ptr))
                        tree.append_child(child)
                    temp_inside=[]
    if len(p_stack)!=0:
        raise Exception() # TODO
    if len(temp_inside)!=0:
        tree.append_string("".join(temp_inside))
    return tree

def replace_line(line:str):
    listed = bracket_parse(line).gen_list()

    state = 0
    temp_indices = []
    new_list = []
    record_flag=False

    for i in range(len(listed)):
        cur = listed[i]
        if state==-1:
            raise Exception("syntax error!")
        if cur == "\n":
            break

        elif state == 0:
            if cur in ("_", "^"):
                state = 2
                record_flag=True
            else:
                state = 0

        elif state == 1:
            if cur in ("_", "^"):
                state = 2
                record_flag=True
            else:
                state = 1

        elif state == 2:
            if cur == " ":
                state = 2
            elif cur == "\\":
                state = 4

            elif isinstance(cur,BracketTree):
                state = 3
            else:
                state = 3
        elif state == 3:
            if cur in ("_","^"):
                state=2
            else:
                state=1
                record_flag=False
        elif state == 4:
            if cur in ("_","^"):
                state=2
            elif cur == " ":
                state=5
            elif isinstance(cur,BracketTree):
                state=3
            else:
                state=4

        elif state == 5:
            if cur==" ":
                state=5
            elif isinstance(cur,BracketTree):
                state=3
            elif cur=="\\":
                state=4
            else:
                state=1
                record_flag=False
        if record_flag:
            temp_indices.append(cur)
        else:
            if len(temp_indices)!=0:
                new_list.append(convert(temp_indices))
            temp_indices=[]
            new_list.append(cur)
    else:
        if len(temp_indices)!=0:
            new_list.append(convert(temp_indices))
    new_str=""
    for item in new_list:
        new_str+=str(item)
    return new_str

def convert(origin):
    indices=[]
    for item in origin:
        if item in ("^","_"):
            indices.append([item,""])
        else:
            indices[-1][1]+=str(item)
    if len(indices)==1:
        return "".join(indices[0])
    else:
        res=["",""] # up,down
        for index in indices:
            if index[0]=="^":
                res[0]+=index[1]
                res[1]+=r"\phantom{"+index[1]+"}"
            else:
                res[1]+=index[1]
                res[0]+=r"\phantom{"+index[1]+"}"
        return "^"+"{"+res[0]+"}"+"_"+"{"+res[1]+"}"

def change(file,line_num):
    with open(file,"a+") as f:
        f.seek(line_num)
        line=f.readline()
        replace=replace_line(line)
        f.seek(line_num)
        f.write(replace)

# if __name__=="__main__":
if True:
    main()