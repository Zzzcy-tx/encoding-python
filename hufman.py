from heapq import heapify, heappop, heappush
import heapq


class TreeNodes():
    def __init__(self, val, lchild=None, rchild=None):  # 构造函数参数设置为None，就可以在构造时先不用提供，等到先构造完毕后再用语句提供
        self.val = val
        self.lchild = lchild
        self.rchild = rchild

    def __lt__(self, other):
        return self.val < other.val  # change the '<' function if used on those objects:just compare the val between the two object


def Huffman_Tree(arr):
    heapq.heapify(arr)
    arrNode = [TreeNodes(val) for val in arr]

    while len(arrNode) > 1:
        min1 = heapq.heappop(arrNode)
        min2 = heapq.heappop(arrNode)
        # print(min1.val,min2.val)

        newNode = TreeNodes(val=min1.val + min2.val, lchild=min1, rchild=min2)
        heapq.heappush(arrNode, newNode)

    return arrNode


arr = [0.07, 0.13, 0.22, 0.01, 0.57]
arrNode = Huffman_Tree(arr)
root = arrNode[0]


def recurseTreeNode(Node):
    if Node == None:
        return

    print(Node.val)
    recurseTreeNode(Node.lchild)
    recurseTreeNode(Node.rchild)


# recurseTreeNode(root)


def encoder(root):
    if root is None:
        return

    myqueue = []
    myqueue.append(root)

    turn = 1
    realTurn = 0
    dict = {}
    while len(myqueue) != 0:
        node = myqueue.pop(0)
        flag = 0 if turn % 2 == 0 else 1  # flag每轮交替 用来编写[层内编码]

        realTurn += 1 if turn % 2 == 0 else 0  # 用来编[层编码]的位数

        layerCode = str(flag) * realTurn

        if node.lchild is not None:
            layerInCode = '0'
            huffmanCode = layerCode + layerInCode
            dict[node.lchild.val] = huffmanCode
            myqueue.append(node.lchild)
            # 把val作为键 把encode作为值 后面再提取子集
        if node.rchild is not None:
            myqueue.append(node.rchild)
            layerInCode = '1'
            huffmanCode = layerCode + layerInCode
            dict[node.rchild.val] = huffmanCode

            # 把val作为键 把encode作为值 后面再提取子集

        turn += 1

    return dict


dict = encoder(root)

arrDict = {}
for key, value in dict.items():
    if key in arr:
        arrDict[key] = value

print(arrDict)





