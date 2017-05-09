#!/usr/bin/env python
"""
===================
Label image regions
===================

This example shows how to segment an image with image labelling. The following
steps are applied:

1. Thresholding with automatic Otsu method
2. Close small holes with binary closing
3. Remove artifacts touching image border
4. Measure image regions to filter small objects

http://scikit-image.org/docs/dev/auto_examples/plot_label.html
"""
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

#from skimage import data
#from skimage.filters import threshold_otsu
from skimage.segmentation import clear_border
from skimage.measure import label, regionprops
from skimage.morphology import closing, square
from skimage.color import label2rgb

from PIL import Image
from numpy import array
import os
import math

#show process results (yes/no)
show_result = 1
#minimal area of regions
min_area_size = 400
#margin of image to discard regions (percentage of image height)
exclusion_margin = 3
#supported image formats
supp_formats = ('jpg', 'png')

def mask(low, high):
    return [255 if low <= x <= high else 0 for x in range(0, 256)]

def process(image_name):
    orig_img_RGB = Image.open(image_name)
    if orig_img_RGB.format != 'JPEG':
        return

    width, height = orig_img_RGB.size
    margin = int(height*(exclusion_margin/100))

    #orig_img_GS = orig_img_RGB.convert('L')
    #orig_arr_GS = array(orig_img_GS)
    orig_arr_RGB = array(orig_img_RGB)

    # apply threshold and convert into binary
    thres_img_bin = orig_img_RGB.point(mask(0,51)+mask(0,255)+mask(80,255)).convert('L').point([0]*255+[255])
    thres_img_bin.save(image_name + '_thres.png')
    thresh_arr_bin = array(thres_img_bin)
    #if show_result == 1:
        #thres_img_bin.show()

    #binary closing
    bw = closing(thresh_arr_bin > 100, square(3))

    # remove artifacts connected to image border
    cleared = clear_border(bw, margin)

    # label image regions
    label_image = label(cleared)
    image_label_overlay = label2rgb(label_image, image=orig_arr_RGB)

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.imshow(image_label_overlay)

    region_counter = 0
    min_x=width
    min_y=height
    max_x=0
    max_y=0

    for region in regionprops(label_image):
        # take regions with large enough areas
        if region.area >= min_area_size:
            # draw rectangle around segmented areas
            minr, minc, maxr, maxc = region.bbox
            rect = mpatches.Rectangle((minc, minr), maxc - minc, maxr - minr,
                                      fill=False, edgecolor='yellow', linewidth=1)
            ax.add_patch(rect)
            # calculate centroid and draw over segmented areas
            centroid = mpatches.Circle(((minc+maxc)/2, (minr+maxr)/2), 0.5, fill=False, edgecolor='yellow', linewidth=1)
            ax.add_patch(centroid)

            # get group bbox coordinates
            if maxr > max_y:
                max_y = maxr
            if minc < min_x:
                min_x = minc
            if minr < min_y:
                min_y = minr
            if maxc > max_x:
                max_x = maxc

            # count number of regions on image
            region_counter = region_counter + 1

    # bounding box of the group of regions
    # group_bbox = [x, y, width, height, centroid_x, centroid_y]
    group_bbox = [min_x, min_y, max_x-min_x, max_y-min_y, (min_x+max_x)/2, (min_y+max_y)/2]
    group_bbox_rect = mpatches.Rectangle((group_bbox[0], group_bbox[1]), group_bbox[2], group_bbox[3], fill=False, edgecolor='red', linewidth=1)
    ax.add_patch(group_bbox_rect)

    # draw centroid over group
    group_cent_circ = mpatches.Circle((group_bbox[4], group_bbox[5]), 0.5, fill=False, edgecolor='red', linewidth=1)
    ax.add_patch(group_cent_circ)

    print "--> Image:", image_name + ". Regions found:", region_counter

    # image centroid coordinates [x, y]
    image_cent = [width/2, height/2]
    d = int(math.sqrt((image_cent[0])**2+(image_cent[1])**2))
    print "--> d =", d

    # distance from group centroid to image centroid and score
    x_side = image_cent[0]-group_bbox[4]
    if x_side<0:
        x_side = x_side*-1
    y_side = image_cent[1]-group_bbox[5]
    if y_side<0:
        y_side = y_side*-1
    distance = math.sqrt(x_side**2+y_side**2)
    score = format(distance/d, '.2f')
    print "--> SCORE:", score

    plt.plot([image_cent[0], group_bbox[4]], [image_cent[1], group_bbox[5]])

    ax.set_axis_off()
    plt.tight_layout()
    if show_result == 1:
        plt.show()

    #Agregado para liberar memoria

    plt.close(fig)
    plt.cla()
    plt.clf()
    plt.close()
    fig.clear()
    del fig

    #plt.savefig(image_name + '_label.png')

#if executed as script
if __name__ == '__main__':
    #folder = "FotosDron-4mAltura"
    folder = "fotos_dron"
    image_counter = 0

    print "-> Folder:", folder
    print "-> Show processing results:", show_result
    print "-> Minimal area of regions:", min_area_size, "px"
    print "-> Exclusion margin:", exclusion_margin, "%"

    listing = os.listdir(folder)    
    for file in listing:
        for search_str in supp_formats:
            if search_str in file and 'thres' not in file and 'label' not in file:
                process(folder + "/" + file)
                image_counter = image_counter + 1

    print "-> Images processed:", image_counter
