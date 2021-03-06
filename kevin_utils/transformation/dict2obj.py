#coding=utf-8

class Dict2Obj(object):
    def __init__(self,map):
        #print(map)
        self.map = map

    def __setattr__(self, name, value):
        if name == 'map':
             object.__setattr__(self, name, value)
             return;
        self.map[name] = value

    def __getattr__(self,name):
        v = self.map[name]
        if isinstance(v,(dict)):
            return Dict2Obj(v)
        if isinstance(v, (list)):
            r = []
            for i in v:
                if isinstance(i,(dict)):
                    r.append(Dict2Obj(i))
                else:
                    r.append(i)
            return r                 
        else:
            return self.map[name];

    def __getitem__(self,name):
        return self.map[name]

if __name__ == '__main__':
    m = {'haha':{'a':55},'bb':[{'c':32,'d':45},{'c':22,'d':56}]}
    book = Dict2Obj(m);
    print(book.bb[0].c)