# import random
# flag = True
# # for H in range(10,25):
# #     for S in range(10,61):
# #         for M in range(10,61):
# #             if (S % 10 == 3 or S % 10 == 8) and (M % random.randint(10,60) < 9):
# #                 if flag:
# #                     print('{}:{}:{}'.format(H,S,M))
# #                     flag = False
# #             if (S % 10 == 4 or S % 10 == 9):
# #                 flag = True

# for H in range(10,25):
#     for S in range(10,61):
#         for M in range(10,61):
#             if (S % 10 == 3 or S % 10 == 8) and (M % random.randint(10,60) < 9):
#                 if flag:
#                     flag  = False
#                 else :
#                     continue
#             elif (S % 10 == 4 or S % 10 == 9):
#                 flag = True
#                 continue
#             else:
#                 continue
#             print('{}:{}:{}'.format(H,S,M))
# # import time
# # print (time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
# # while True:
# #     H = time.strftime("%H",time.localtime())
# #     M = time.strftime("%M",time.localtime())
# #     S = time.strftime("%S",time.localtime())
    
# #     print('当前时间为：{}:{}:{}'.format(H,M,S))
# #     time.sleep(1)

import traceback
try:
    1/0
except Exception:
    traceback.print_exc()