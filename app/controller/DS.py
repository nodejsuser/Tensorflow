from PIL import Image, ImageFilter
import os

base = [str(x) for x in range(10)] + [ chr(x) for x in range(ord('a'),ord('a')+6)]

def imageprepare(argv):
    im = Image.open(argv).convert('L')
    width = float(im.size[0])
    height = float(im.size[1])
    if width > 28:
        img = im.resize((28, 28), Image.ANTIALIAS).filter(ImageFilter.SHARPEN)
        tv = list(img.getdata())  # get pixel values
    elif width < 28:
        img = im.resize((28, 28), Image.ANTIALIAS).filter(ImageFilter.SHARPEN)
        tv = list(img.getdata())  # get pixel values
    else:
        tv = list(im.getdata())
        return tv  # get pixel values
    return tv

def dec2hex(string_num):
    num = int(string_num)
    mid = []
    while True:
        if num == 0: break
        num,rem = divmod(num, 16)
        mid.append(base[rem])

    return ''.join([str(x) for x in mid[::-1]])

def getArr(picture):
    x=imageprepare(picture)
    result=[None]*784
    i=0
    for pixel in x:
        if(dec2hex(str(x[i]))==''):
            result[i]='00'
        else:
            result[i]=dec2hex(str(x[i]))
        i=i+1

    return result


Names = [['app/training-images','train'], ['app/test-images','tk10']]
def toDS(file,tag):
    for name in Names:
        FileList = []
        for dirname in os.listdir(name[0])[1:]:  # [1:] Excludes .DS_Store from Mac OS
            path = os.path.join(name[0], dirname)
            for filename in os.listdir(path):
                if filename.endswith(".png"):
                    FileList.append(os.path.join(name[0], dirname, filename))

            #获取像素数组
        arr=getArr(file)
        #获取标签值
        #labelArr = file.split('/')
        #label = int(labelArr[2])

            #打开数据集
        image= open('../MNIST_data/'+name[1]+'-images-idx3-ubyte','wb')

    for pixel in arr:
        pixel_byte=bytes(pixel,encoding="utf-8")
        #print(pixel_byte)
        image.write(pixel_byte)

    image.close()
    print("DS: ",file)
    #打开标签集
    label_ds = open('../MNIST_data/' + name[1] + '-labels-idx1-ubyte', 'wb')
    label_ds_byte=bytes(str(tag),encoding="utf-8")
    print(label_ds_byte)
    label_ds.write(label_ds_byte)
    label_ds.close()