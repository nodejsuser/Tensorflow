import os
from PIL import Image
from array import *
from random import shuffle
import gzip

Names = [['./training-images', 'train'], ['./test-images' , 'tk10']]
for name in Names:
    data_image = array('B')
    data_label = array('B')

    FileList = []
    for dirname in os.listdir(name[0])[1:]:  # [1:] Excludes .DS_Store from Mac OS
        path = os.path.join(name[0], dirname)
        for filename in os.listdir(path):
            if filename.endswith(".png"):
                FileList.append(os.path.join(name[0], dirname, filename))

    shuffle(FileList)  # Usefull for further segmenting the validation set

    for filename in FileList:
        print(filename)
        # 获取标签值
        labelArr = filename.split('/')
        #i = str(label[1])
        #print(label)
        #j = str(i.split('\\')[1])
        label = int(labelArr[2])
        # label = int(filename.split('/')[1])

        Im = Image.open(filename)

        pixel = Im.load()

        width, height = Im.size

        for x in range(0, width):
            for y in range(0, height):
                data_image.append(pixel[y, x])

        data_label.append(label)  # labels start (one unsigned byte each)

    hexval = "{0:#0{1}x}".format(len(FileList), 6)  # number of files in HEX

    # header for label array

    header = array('B')
    header.extend([0, 0, 8, 1, 0, 0])
    header.append(int('0x' + hexval[2:][:2], 16))
    header.append(int('0x' + hexval[2:][2:], 16))

    data_label = header + data_label

    # additional header for images array

    if max([width, height]) <= 256:
        header.extend([0, 0, 0, width, 0, 0, 0, height])
    else:
        raise ValueError('Image exceeds maximum size: 256x256 pixels');

    header[3] = 3  # Changing MSB for image data (0x00000803)

    data_image = header + data_image

    #shutil.rmtree('../MNIST_data/')
    #os.mkdir('../MNIST_data/')
    #os.mkdir('../MNIST_data/')
    output_file = open('../MNIST_data/' + name[1] + '-images-idx3-ubyte', 'wb')
    data_image.tofile(output_file)
    output_file.close()

    output_file = open('../MNIST_data/' + name[1] + '-labels-idx1-ubyte', 'wb')
    data_label.tofile(output_file)
    output_file.close()

    #image_gz=tarfile.open('../MNIST_data/' + name[1] + '-images-idx3-ubyte.idx3-ubyte',"r:gz")
    #label_gz = tarfile.open('../MNIST_data/' + name[1] + '-labels-idx1-ubyte.idx1-ubyte', "r:gz")
    #gzip.GzipFile('images-idx3-ubyte.gz','wb',9,'../MNIST_data/' + name[1] + '-images-idx3-ubyte.idx3-ubyte')
    #g = gzip.GzipFile(filename="", mode="wb", compresslevel=9, fileobj=open('../MNIST_data/images-idx3-ubyte.gz', 'wb'))

    image_in = open('../MNIST_data/' + name[1] + '-images-idx3-ubyte', 'rb')
    image_out = gzip.open('../MNIST_data/' + name[1] + '-images-idx3-ubyte.gz','wb')
    image_out.writelines(image_in)
    image_out.close()
    image_in.close()

    labels_in = open('../MNIST_data/' + name[1] + '-labels-idx1-ubyte', 'rb')
    labels_out = gzip.open('../MNIST_data/' + name[1] + '-labels-idx1-ubyte.gz' ,'wb')
    labels_out.writelines(labels_in)
    labels_out.close()
    labels_in.close()

    #os.system('gzip ' + '../MNIST_data/' + name[1] + '-images.idx3-ubyte')
    #os.system('gzip ' + '../MNIST_data/' + name[1] + '-labels.idx1-ubyte')