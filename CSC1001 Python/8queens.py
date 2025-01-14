import random
import math

# 棋盘初始化
# params
# -d: 矩阵的大小
def initial_chessboard(d):
  chessboard = [[(x+1, y+1) for y in range(d)] for x in range(d)]
  print(chessboard)
  return chessboard


# 指定行过滤出可选位置并随机选取一个，作为本行queen的填入位置
# params
# -chessboard：棋盘矩阵
# -rowIndex: 指定矩阵的某一行的序号
# -placePicked：已被选的位置
# -exclusions: 回溯时的排除项列表
def filter_and_pick_place(chessboard, rowIndex, placePicked, exclusions):
  # 取到该行
  row = chessboard[rowIndex]
  # 在后续过程中保存本行过滤完的可选位置
  alternative = []

  if len(placePicked) != 0:
    # 遍历本行的每一项
    for column in row:
      # 这个变量标志了该位置是否可用，初始化的时候是False，可用
      available = True
      # 遍历已被选的位置
      for item in placePicked:
        # 只要有一个出现同列或同对角线，或位于排除项列表中时，将available标记为不可用
        if column[1] == item[1] or column[0]+column[1] == item[0]+item[1] or \
          column[0]-column[1] == item[0]-item[1] or column in exclusions:
          available = False
      # 该位置可用，添加进可用项数组里
      if available:
        alternative.append(column)
  else:
    alternative = row

  if len(alternative) == 0:
    # 死解，返回0，指示不成功
    return 0
  else:
    # 活解，随机挑选位置点，返回1，指示成功
    randomIndex = math.floor(len(alternative) * random.random())
    pick = alternative[randomIndex]
    placePicked.append(pick)
    return 1

# 根据最终结果用图表展示出来
# params
# -positions: 最终挑选的位置列表
def generate_figure(positions):
  figureSring = ''
  for row in range(8):
    for col in range(8):
      if col == 0:
        figureSring += '|'
      if (row+1, col+1) in positions:
        figureSring += 'Q|'
      else:
        figureSring += ' |'
    figureSring += '\n'
  return figureSring


if __name__ == '__main__':
  chessboard = initial_chessboard(8)
  placePicked = []
  exclusions = [[] for i in range(8)]
  row = 0

  while row < 8:
    success = filter_and_pick_place(chessboard, row, placePicked, exclusions[row])
    if success == 1:
      # 没有遇到死解，继续往下
      row += 1
    else:
      # 遇到了死解，回退到上一行并且将死解的点存入排除项中，重新选点
      row -= 1
      exclusions[row].append(placePicked.pop())
      # 由于是自上而下选点的方式，当上一行的点重新选取时，后一行的排除项已经没有意义了，清空
      if row < 7:
        exclusions[row+1] = []
  
  # 打印出棋盘
  print(generate_figure(placePicked))