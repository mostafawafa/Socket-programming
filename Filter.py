
import cv2


class Filter:

    def __init__(self,img_path):
        self.img_path = img_path
        self.img = cv2.imread(self.img_path)

    def blackwhite(self):
        self.img = cv2.imread(self.img_path, 0)
        return self


    def blur(self):
        self.img = cv2.blur(self.img, (5, 5))

        return self


    def crop(self):
        self.img = self.img[0:500,0:500]
        return self

    def border(self):
        self.img = cv2.copyMakeBorder(self.img, 10, 10, 10, 10, cv2.BORDER_CONSTANT, value=[255,0,0])
        return self

    def remove_color(self,color):
        # in cv  it's BGR not RBG
        if(color == 'red'):
            self.img[:,:,2] = 0
        elif(color=='blue'):
            self.img[:,:,0] = 0
        elif(color == 'green'):
            self.img[:,:,1] = 0
        return self




    def save(self,saveAs):
        cv2.imwrite(saveAs, self.img)
        cv2.destroyAllWindows()



