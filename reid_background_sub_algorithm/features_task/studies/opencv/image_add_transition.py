import cv2


def main():
    im1 = cv2.imread('../data/images/im1.png')
    im1 = cv2.cvtColor(im1, cv2.COLOR_BGR2RGB)
    im2 = cv2.imread('../data/images/im2.jpg')
    im2 = cv2.cvtColor(im2, cv2.COLOR_BGR2RGB)

    i = 0
    maximum = 100
    increasing = True

    while True:
        alpha = i / maximum
        cv2.imshow('weighted', cv2.addWeighted(im1, alpha, im2, 1 - alpha, 0))
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break
        if i == maximum:
            increasing = False
            i -= 1
            continue
        if i == 0:
            increasing = True
            i += 1
            continue

        if increasing:
            i += 1
        else:
            i -= 1


if __name__ == "__main__":
    main()
