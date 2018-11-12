import os
import xml.etree.ElementTree as ET
import scipy.misc as scp
# from keras.preprocessing import image


def get_crop_index(v_nose, h_nose, half_size):
    """Returns the index of a square of 2halfsize*2halfsize, centered around
    (vnose,hnose) or as close as possible, for an image of 768x512 pixels."""
    left_index = h_nose - half_size
    right_index = left_index + 2*half_size
    if left_index < 0:
        right_index -= left_index
        left_index = 0
    elif right_index > 511:
        left_index -= right_index - 511
        right_index = 511
    up_index = v_nose - half_size
    down_index = up_index + 2*half_size
    if up_index < 0:
        down_index -= up_index
        up_index = 0
    elif down_index > 767:
        up_index -= down_index - 767
        down_index = 767
    return left_index, up_index, right_index, down_index


root_path = "/home/laplace/claudio/proyecto_imagenes/colorferet/"
images1_path = root_path + "dvd1/data/images/"
images2_path = root_path + "dvd2/data/images/"
if not os.path.exists(root_path + "results/"):
    os.mkdir(root_path + "results/")
if not os.path.exists(root_path + "results/no_coords/"):
    os.mkdir(root_path + "results/no_coords/")
subjects_xml = ET.parse(root_path + "dvd1/data/ground_truths/xml/subjects.xml")
subjects_root = subjects_xml.getroot()
images_list = open(root_path + "dvd1/doc/partitions/fa.txt", 'r')
images_list_parsed = images_list.read().splitlines()
halfsize = 225
for element in images_list_parsed:
    if int(element.split()[0]) < 740:
        img_file = scp.imread(images1_path + '/'.join(element.split()))  # image.load_img(images1_path + '/'.join(element.split()))
        info_file = open(root_path + "dvd1/data/ground_truths/name_value/" +
                         '/'.join(element.split())[:-3] + "txt")
    else:
        img_file = scp.imread(images2_path + '/'.join(element.split()))
        info_file = open(root_path + "dvd2/data/ground_truths/name_value/" +
                         '/'.join(element.split())[:-3] + "txt")
    hnose = 256
    vnose = 284
    no_coords = True
    for line in info_file.read().splitlines():
        if line.split('=')[0] == "nose_coordinates":
            hnose, vnose = line.split('=')[1].split()
            no_coords = False
            break
    #print("hnose is {}, vnose is {}".format(hnose, vnose))
    info_file.close()
    left_index, up_index, right_index, down_index = get_crop_index(int(vnose), int(hnose), halfsize)
    #print("Index are {}, {}, {} and {}".format(left_index, right_index, up_index, down_index))
    img_cropped = img_file[up_index:down_index, left_index:right_index]
    #print("Original image is {}. Cropped image is {}".format(img_file.shape, img_cropped.shape))
    if no_coords:
        scp.imsave(root_path + "results/no_coords/" + element.split()[1], img_cropped)
    else:
        scp.imsave(root_path + "results/" + element.split()[1], img_cropped)
