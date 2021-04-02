import cv2


cap = cv2.VideoCapture(0)
while 1:
    success, frame=cap.read()
    # load image
    img = frame
    
    # add blur because of pixel artefacts 
    img = cv2.GaussianBlur(img, (5, 5),5)
    # convert to HSV
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV) 
    # set lower and upper color limits
    lower_val = (38,47,152)
    upper_val = (83,255,255)
    # Threshold the HSV image to get only green colors
    mask = cv2.inRange(hsv, lower_val, upper_val)
    # apply mask to original image
    res = cv2.bitwise_and(img,img, mask= mask)
    #show imag
    cv2.imshow("Result", res)
    # detect contours in image
    contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    # draw filled contour on result
    for cnt in contours:
        cv2.drawContours(res, [cnt], 0, (0,0,255), 2)
    # detect edges in mask
    edges = cv2.Canny(mask,100,100)
    # to save an image use cv2.imwrite('filename.png',img)
    #show images
    cv2.imshow("Result_with_contours", res)
    cv2.imshow("Mask", mask)
    cv2.imshow("Edges", edges)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cv2.waitKey(0)
cv2.destroyAllWindows()