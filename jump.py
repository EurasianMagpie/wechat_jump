# -*- coding: utf-8 -*-

import os
import random
import time
import ia

adb_path = "F:\\Android\\android-sdk-windows\\platform-tools\\adb.exe"
shot_path_phone = "/sdcard/_jumper"
shot_path_pc = "F:\\Test_Program\\jumper\\shot"
s_pre = "pre.png"
s_cur = "cur.png"
s_file = "s.png"

# 根据水平距离差计算点击事件的系数,经验值
r = 1.5840

def jump(ms):
    x1 = random.randint(10, 15)
    y1 = random.randint(10, 15)
    x2 = random.randint(16, 19)
    y2 = random.randint(16, 20)
    cmd = "%s shell input swipe %d %d %d %d %d" % (adb_path, x1, y1, x2, y2, ms)
    os.system(cmd)
    pass

def _shot():
    _path_phone = shot_path_phone + "/" + s_file;
    cmd = "%s shell screencap -p %s" % (adb_path, _path_phone)
    print cmd
    os.system(cmd)
    pass

def cap_next():
    _shot();
    cmd_rm_pre = "rm %s\\%s" % (shot_path_pc, s_pre)
    print cmd_rm_pre
    os.system(cmd_rm_pre)
    cmd_mv_cur = "move %s\\%s %s\\%s" % (shot_path_pc, s_cur, shot_path_pc, s_pre)
    print cmd_mv_cur
    os.system(cmd_mv_cur)
    cmd_pull_new = "%s pull %s/%s %s\\%s" % (adb_path, shot_path_phone, s_file, shot_path_pc, s_cur)
    print cmd_pull_new
    os.system(cmd_pull_new)
    pass

# 截图,计算出下一步跳跃需要跨越的水平距离,
# 根据跳跃距离计算出点击时间
def jump_to_next_target():
    cap_next()
    s_path = "%s\\%s" % (shot_path_pc, s_cur)
    delta = ia.ia(s_path)
    ms = delta * r
    print "press %s ms" % ms
    jump(ms)

if __name__ == "__main__":
    #jump_to_next_target()
    while (True):
        jump_to_next_target()
        time.sleep(1)
    
