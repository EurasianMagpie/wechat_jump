# -*- coding: utf-8 -*-

import Image
import math

# 测试手机只有一加5 one plus 5
# 屏幕尺寸 1080 * 1920

# 忽略顶部,底部,左右的边缘区域
pending_top = 300
pending_bottom = 200
pending_h = 50

# 我的棋子顶部像素颜色分部
px_me_1 = (51, 51, 55)
px_me_2 = (53, 54, 60)

def px_in_range(px, px1, px2):
    for i in range(0, 3):
        if (px1[i] <= px[i] and px[i] <= px2[i]) or (px2[i] <= px[i] and px[i] <= px1[i]):
            continue
        else:
            return False
    return True

def px_is_me(px):
    for i in range(0, 3):
        if (px_me_1[i] <= px[i] and px[i] <= px_me_2[i]):
            continue
        else:
            return False
    return px[2] > px[0] and px[2] > px[1]

# 因为目标的在左上或右上的角度的是固定的,简单认为是常亮,
# 所以计算跳跃按压时间仅以目标与自己位置的水平距离差做唯一变量
# 找到目标的水平中心位置,找到自己的水平中心位置,并计算下一次的水平相对距离
def calc_gap(im):
    w = im.size[0]
    h = im.size[1]
    px_begin = im.getpixel((pending_h, pending_top))
    print "bg px begin : ", px_begin
    px_end = im.getpixel((w - pending_h, h - pending_bottom))
    print "bg px end : ", px_end
    # 找到目标
    top_1 = (0,0)
    top_2 = (0,0)
    find_top = False
    for i in range(pending_top, h - pending_bottom):
        if find_top:
            break;
        for j in range(pending_h, w - pending_h):
            px = im.getpixel((j, i))
            if not px_in_range(px, px_begin, px_end):
                top_2 = top_1 = (j, i)
                find_top = True
                break
    if not find_top:
        print "can not find target"
        return 0
    for i in range(top_1[0]+1, w - pending_h):
        px = im.getpixel((i, top_1[1]))
        if not px_in_range(px, px_begin, px_end):
            top_2 = (i, top_1[1])
        else:
            break
    t_top = ((top_1[0]+top_2[0])/2, top_1[1])
    t_end = t_top
    for j in range(t_top[1], h - pending_bottom):
        px = im.getpixel((t_top[0], j))
        if not px_in_range(px, px_begin, px_end):
            t_end = ((t_top[0], j))
        else:
            break
    print "target pos : ", t_top, t_end
    # 找到棋子
    me_top_1 = (0, 0)
    me_top_2 = (0, 0)
    find_me = False
    for i in range(pending_top, h - pending_bottom):
        if find_me:
            break;
        for j in range(pending_h, w - pending_h):
            px = im.getpixel((j, i))
            if px_is_me(px):
                if px_is_me(im.getpixel((j+1, i))) and px_is_me(im.getpixel((j+3, i))):
                    me_top_2 = me_top_1 = (j, i)
                    find_me = True
                    break
    if not find_me:
        print "can not find me"
        return 0
    for i in range(me_top_1[0]+1, w - pending_h):
        px = im.getpixel((i, me_top_1[1]))
        if px_is_me(px):
            me_top_2 = (i, me_top_1[1])
        else:
            break
    me_top = ((me_top_1[0]+me_top_2[0])/2, me_top_1[1])
    print "my pos : ", me_top
    # 计算出目标和棋子的水平距离差
    delta = abs(t_top[0] - me_top[0])
    print "delta x : ", delta
    return delta

def ia(file_path):
    im = Image.open(file_path)
    return calc_gap(im)

if __name__ == "__main__":
    ia('''F:\Test_Program\jumper\shot\cur.png''')
