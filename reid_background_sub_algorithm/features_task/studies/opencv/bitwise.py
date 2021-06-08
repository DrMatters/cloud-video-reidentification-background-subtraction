import cv2


def main():
    logo = cv2.imread('../data/images/im1.png')
    logo = cv2.cvtColor(logo, cv2.COLOR_BGR2RGB)
    image = cv2.imread('../data/images/test.jpeg')

    # I want to put logo on top-left corner, So I create a ROI
    rows, cols, channels = logo.shape
    roi = image[0:rows, 0:cols]

    # Now create a mask of logo and create its inverse mask also
    gray = cv2.cvtColor(logo, cv2.COLOR_BGR2GRAY)
    ret, mask = cv2.threshold(gray, 10, 255, cv2.THRESH_BINARY)
    mask_inv = cv2.bitwise_not(mask)

    # Now black-out the area of logo in ROI
    background = cv2.bitwise_and(roi, roi, mask=mask_inv)

    # Take only region of logo from logo image.
    logo_region = cv2.bitwise_and(logo, logo, mask=mask)

    # Put logo in ROI and modify the main image
    dst = cv2.add(background, logo_region)
    image[0:rows, 0:cols] = dst

    cv2.imshow('res', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
