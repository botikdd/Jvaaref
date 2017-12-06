import cv2
import numpy

if __name__ == '__main__':
    img = cv2.imread('./Resources/way2.png')
    # gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # edges = cv2.Canny(gray, 50, 150, apertureSize=3)
    # cv2.imwrite('./Resources/gray.png', gray)
    # cv2.imwrite('./Resources/edges.png', edges)

    img = img[175:, ]

    boundaries = [
        ([169, 176, 184], [255, 255, 255])
    ]

    output = None
    for (lower, upper) in boundaries:
        # create NumPy arrays from the boundaries
        lower = numpy.array(lower, dtype = "uint8")
        upper = numpy.array(upper, dtype = "uint8")
    
        # find the colors within the specified boundaries and apply
        # the mask
        mask = cv2.inRange(img, lower, upper)
        output = cv2.bitwise_and(img, img, mask = mask)
    
        # show the images
        cv2.imshow("images", numpy.hstack([img, output]))
        cv2.waitKey(0)

    gray = cv2.cvtColor(output, cv2.COLOR_BGR2GRAY)
    edge = cv2.Canny(gray, 50, 150, apertureSize=3)
    
    cv2.imwrite('./Resources/gray.png', gray)
    cv2.imwrite('./Resources/edges.png', edge)
    lines = cv2.HoughLines(edge,1,numpy.pi/180,200)
    for line in lines:
        for rho,theta in line:
            a = numpy.cos(theta)
            b = numpy.sin(theta)
            x0 = a*rho
            y0 = b*rho
            x1 = int(x0 + 1000*(-b))
            y1 = int(y0 + 1000*(a))
            x2 = int(x0 - 1000*(-b))
            y2 = int(y0 - 1000*(a))

            cv2.line(img,(x1,y1),(x2,y2),(0,0,255),2)





    # lines = cv2.HoughLinesP(edges, 20, numpy.pi/180, 100, minLineLength=500, maxLineGap=150)

    # for line in lines:
    #     for x1, y1, x2, y2 in line:
    #         cv2.line(img, (x1, y1), (x2, y2), (0, 255, 0), 2)

    cv2.imwrite('./Resources/houghlines3.png', img)
    cv2.imshow("image", img)
    # cv2.waitKey(0)