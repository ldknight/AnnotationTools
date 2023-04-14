import numpy as np

# 定义掩码矩阵
mask = np.array([[0, 0, 0, 0, 0],
                 [0, 0, 1, 0, 0],
                 [0, 1, 1, 1, 0],
                 [0, 0, 1, 0, 0],
                 [0, 0, 0, 0, 0]], dtype=np.uint8)

# 定义递归函数进行边缘检测
def detect_edges(mask, row, col):
    if row < 0 or row >= mask.shape[0] or col < 0 or col >= mask.shape[1]:
        return
    if mask[row][col] == 1:
        mask[row][col] = 2  # 将边缘标记为2
        detect_edges(mask, row-1, col)
        detect_edges(mask, row+1, col)
        detect_edges(mask, row, col-1)
        detect_edges(mask, row, col+1)

# 遍历掩码矩阵的每个像素进行边缘检测
for row in range(mask.shape[0]):
    for col in range(mask.shape[1]):
        if mask[row][col] == 1:
            detect_edges(mask, row, col)

# 将边缘标记为1，其他像素标记为0
edges = np.where(mask == 2, 1, 0)

# 打印边缘检测结果
print("Edges:")
print(edges)