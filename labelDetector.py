from ultralytics import YOLO
# import matplotlib.pyplot as plt 
from PIL import Image

class LabelDetector():
    def __init__(self):
        self.Model_Frozen = YOLO('./weights/Freeze_Best_Model.pt')
        self.LabelModel_Fully_Retrained = YOLO('./weights/FullyRetrain_Best_Model.pt')
    
    def getBookCrops(self,image_path):
        crop_paths = []
        result = self.Model_Frozen.predict(source=image_path, classes = 0, conf = 0.8)

        if(len(result) == 0):
            return (0,[])

        result = result[0]
        for i in range(len(result.boxes)):
            print(result.boxes.xywh[i])
            print(result.boxes.xyxy[i])
            x1,y1,x2,y2=result.boxes.xyxy[i].numpy()
            x1=round(x1)
            y1=round(y1)
            x2=round(x2)
            y2=round(y2)
            print(x1,x2)
            img=result.orig_img
            # plt.imshow(img[y1:y2,x1:x2,:])
            crop=img[y1:y2,x1:x2,:]
            print(img.shape)
            im = Image.fromarray(crop)
            im.save(f"./crops/Book/{i}.jpg")
            crop_paths.append(f"./crops/Book/{i}.jpg")
        return (1, crop_paths)
     
    
    def getLabelCrops(self, image, index):
        label_paths = []
        result = self.Model_Frozen.predict(source=image, classes = 0, conf = 0.9)

        if(len(result) == 0):
            return (0,[])

        result = result[0]
        
        for i in range(len(result)):
            # plt.imshow(result.plot())
            x1,y1,x2,y2=result.boxes.xyxy[i].numpy()
            x1=round(x1)
            y1=round(y1)
            x2=round(x2)
            y2=round(y2)
            print(x1,x2)
            img=result.orig_img
            # plt.imshow(img[y1:y2,x1:x2,:])
            crop=img[y1:y2,x1:x2,:]
            print(img.shape)
            im = Image.fromarray(crop)
            im.save(f"./crops/Label/{index}_{i}.jpg")
            label_paths.append(f"./crops/Label/{index}_{i}.jpg")
        return (1, label_paths)
    
    def run(self,image_path):
        Book_crop=self.getBookCrops(image_path)
        labels = []
        if(Book_crop[0] == 1):
            got_label = False
            for j, path in enumerate(Book_crop[1]):
                Label_crop = self.getLabelCrops(path, j)
                if(Label_crop[0] == 1):
                    got_label = True
                    labels += Label_crop[1]
            if(got_label):
                return (1, labels)
            else:
                return (0,[])
        else:
            return (0,[])  