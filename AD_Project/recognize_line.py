import cv2
import numpy as np

img = cv2.imread('testparking.png', cv2.IMREAD_COLOR)
height = img.shape[0] - 1
weight = img.shape[1] - 1
print("The image dimension is %d x %d" % (weight, height))

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
blur = cv2.GaussianBlur(gray, (5, 5), 0)

edge = cv2.Canny(blur, 60, 150)
point = []

for h in range(height // 2):
    for w in range(weight // 2):
        if edge[h, w] == 255:
            point.append([w, h])
            break
    if len(point) != 0:
        break
print(point[0])

for h in range(height // 2):
    for w in range(weight, weight // 2, -1):
        if edge[h, w] == 255:
            point.append([w, h])
            break
    if len(point) != 1:
        break
print(point[1])

for h in range(height, height // 2, -1):
    for w in range(weight // 2):
        if edge[h, w] == 255:
            point.append([w, h])
            break
    if len(point) != 2:
        break
print(point[2])

for h in range(height, height // 2, -1):
    for w in range(weight, weight // 2, -1):
        if edge[h, w] == 255:
            point.append([w, h])
            break
    if len(point) != 3:
        break
print(point[3])


src = np.float32([point[0], point[1], point[2], point[3]])
dst = np.float32([[0, 0], [800, 0], [0, 450], [800, 450]])

M = cv2.getPerspectiveTransform(src, dst)
warp = cv2.warpPerspective(edge.copy(), M, (800, 450))

lines = cv2.HoughLinesP(warp, 1, np.pi/180, 200, 200, 20)

x_list = []
for line in lines:
    for li in line:
        x1, y1, x2, y2 = li
        if abs(y2 - y1) > 10:
            if abs(x2 - x1) < 10:
                x_list.append(x1)
x_list.sort()

point_x = 0
x_last_list = []
x_last_list.append(x_list[0])
for i in range(1, len(x_list)):
    if abs(x_list[point_x] - x_list[i]) > 30:
        point_x = i
        x_last_list.append(x_list[i])
print(x_last_list)

cnt_list = []
for i in range(len(x_last_list) -1):
    roi = warp[:, x_last_list[i]:x_last_list[i + 1]]
    cnt_list.append(cv2.countNonZero(roi))
a = cnt_list.index(min(cnt_list))
print(x_last_list[a], "부터", x_last_list[a + 1], "까지로 주차 할 수 있습니다.")

warp = cv2.cvtColor(warp, cv2.COLOR_GRAY2BGR)

for line in lines:
    for li in line:
        x1, y1, x2, y2 = li
        if abs(y2 - y1) > 10:
            if abs(x2 - x1) < 10:
                cv2.line(warp, (x1, y1), (x2, y2), (255, 0, 125), 2)

edge = cv2.line(edge, (point[0][0], point[0][1]), (point[1][0], point[1][1]), (255, 0, 125), 2)
edge = cv2.line(edge, (point[2][0], point[2][1]), (point[3][0], point[3][1]), (255, 0, 125), 2)
# cv2.imshow('Mrl', img)
cv2.imshow('zxc', warp)
cv2.imshow("edge", edge)

cv2.waitKey(0)
cv2.destroyAllWindows()
