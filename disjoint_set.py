class dset(object):
    def __init__(self, data):
        self.data = data
        self.parent = self

    def find(self):
        if self.parent == self:
            return self
        else:
            self.parent = self.parent.find()
            return self.parent

    def union(self, set2):
        p1 = self.find()
        p2 = set2.find()
        p1.parent = p2

class disjoint_set(object):
    def __init__(self, initList):
        self.setList = map(lambda x: dset(x), initList)
        #print self.setList

    def find(self, data):
        for item in self.setList:
            if item.data == data:
                return item.find()

    def union(self, data1, data2):
        for item in self.setList:
            if item.data == data1:
                item1 = item
            if item.data == data2:
                item2 = item
        return item1.union(item2)

    def size(self):
        count = 0
        for item in self.setList:
            if item.parent == item:
                count += 1
        return count
