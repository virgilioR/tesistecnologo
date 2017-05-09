#!/usr/bin/env python

import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from skimage.segmentation import clear_border
from skimage.measure import label, regionprops
from skimage.morphology import closing, square
from skimage.color import label2rgb
from PIL import Image
from numpy import array
import os
import math
import settings as config

# runs the detection on a single image
def processImage(file):
    obj = Detection(file)
    obj.process()
    config.printObjInfoToLog(obj)
    return obj

# loops on the given folder (from settings)
def processFolder():
    # variables initialization
    obj_list = []
    index = 0

    listing = os.listdir(config.getSourceFolderName())    
    for file in listing:
        for search_str in config.getSupportedFormats():
            if search_str in file:
                obj_list.append(processImage(file))
                index = index + 1

    return obj_list

# runs the detection over the given file/folder
def run(file, is_folder):
    if (is_folder==1):
        config.setSourceFolderName(file)
        proc_list = processFolder()
        config.printListInfoToLog(proc_list)
    else:
        proc_img = processImage(file)
        return proc_img

class Detection(object):

    def __init__(self, image_file):
        # IMAGE PROPERTIES
        # PIL image object
        original = Image.open(config.getImagePath(image_file))
        # apply resizing (from settings)
        self.img_RGB = original.resize( [int(config.getResize() * s) for s in original.size] )
        # image filename
        self.img_file = image_file
        # width, height of the image
        self.img_width, self.img_height = self.img_RGB.size
        # margin (in pixels)
        self.margin = int(self.img_height*(config.getExclusionMargin()*0.01))
        # number of detected regions
        self.regions_n = 0
        # distance between a corner of the image and it's centroid
        self.img_dist = 0
        # image centroid coords
        self.img_centroid = [-1, -1]
        
        # GROUP PROPERTIES
        # bounding box of the group, including centroid = [x, y, width, height, centroid_x, centroid_y]
        self.group_bbox = [-1, -1, -1, -1, -1, -1]
        # area of regions detected and filtered
        self.regions_area = []

        # calculated distance between group centroid and image centroid
        self.final_distance = 0
        # calculated score of the detection (from 0 to 1)
        self.final_score = -1

    # returns the mask (lookup table) to apply the threshold
    def mask(self, low, high):
        return [255 if low <= x <= high else 0 for x in range(0, 256)]

    # applies threshold, detects regions, calculates score
    def process(self):  
        # convert image into array      
        arr_RGB = array(self.img_RGB)

        # apply threshold and convert into binary
        mask_R = self.mask(config.threshold[0][0], config.threshold[0][1])
        mask_G = self.mask(config.threshold[1][0], config.threshold[1][1])
        mask_B = self.mask(config.threshold[2][0], config.threshold[2][1])
        img_binary = self.img_RGB.point(mask_R+mask_G+mask_B).convert('L').point([0]*255+[255])
        if config.getDebugMode() == 2:
            # save binary image
            img_binary.save(config.getBinaryPath(self.img_file))

        #binary closing
        arr_binary = array(img_binary)
        arr_closed = closing(arr_binary > 100, square(3))

        # remove artifacts connected to image border by using margin
        #arr_cleared = clear_border(arr_closed, self.margin)

        # label image regions
        #arr_labeled = label(arr_cleared)
        arr_labeled = label(arr_closed)
        arr_overlay = label2rgb(arr_labeled, image=arr_RGB)
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.imshow(arr_overlay)
    
        # variables to get group bbox coords
        min_x=self.img_width
        min_y=self.img_height
        max_x=0
        max_y=0

        # filter detected regions by area
        for region in regionprops(arr_labeled):
            if region.area >= config.getMinAreaSize():
                # draw rectangle around segmented areas
                minr, minc, maxr, maxc = region.bbox

                if config.getDebugMode() >= 1:
                    rect = mpatches.Rectangle((minc, minr), maxc - minc, maxr - minr,
                                              fill=False, edgecolor='yellow', linewidth=1)
                    ax.add_patch(rect)
                    
                    # calculate region's centroid and draw over segmented areas
                    centroid = mpatches.Circle(((minc+maxc)/2, (minr+maxr)/2), 0.5, fill=False, edgecolor='yellow', linewidth=1)
                    ax.add_patch(centroid)

                # get group bbox coords
                if maxr > max_y:
                    max_y = maxr
                if minc < min_x:
                    min_x = minc
                if minr < min_y:
                    min_y = minr
                if maxc > max_x:
                    max_x = maxc

                # count number of regions on image
                self.regions_n = self.regions_n + 1
                self.regions_area.append(region.area)

        # remove artifacts connected to image border by using margin
        arr_regions_cleared = clear_border(arr_labeled, self.margin)

        # check if number of cleared detected regions is equal to detected regions
        # (to avoid cases when the group is in contact with the margin)
        regions_counter = 0
        for region in regionprops(arr_regions_cleared):
            if region.area >= config.getMinAreaSize():
                regions_counter = regions_counter + 1

        if self.regions_n != regions_counter:
            self.regions_n = 0

        if self.regions_n > 0:
            # group centroid
            #group_centroid = 
            self.calculateGroupCentroid((min_x+max_x), (min_y+max_y))

            # bounding box of the group
            # group_bbox = [x, y, width, height, centroid_x, centroid_y]
            self.group_bbox = [min_x, min_y, max_x-min_x, max_y-min_y, (min_x+max_x)/2, (min_y+max_y)/2]
            
            if config.getDebugMode() >= 1:
                # draw rectangle around group
                group_bbox_rect = mpatches.Rectangle((self.group_bbox[0], self.group_bbox[1]), self.group_bbox[2], self.group_bbox[3], fill=False, edgecolor='red', linewidth=1)
                ax.add_patch(group_bbox_rect)

                # draw group's centroid
                group_cent_circ = mpatches.Circle((self.group_bbox[4], self.group_bbox[5]), 0.5, fill=False, edgecolor='red', linewidth=1)
                ax.add_patch(group_cent_circ)

        # image centroid
        self.calculateImageCentroid()
        
        # distances and score
        self.img_dist = self.calculateDistance([0, 0], self.img_centroid)
        if self.regions_n == 0:
            self.final_distance = self.calculateDistance(self.img_centroid, self.img_centroid)
        else:
            self.final_distance = self.calculateDistance([self.group_bbox[4], self.group_bbox[5]], self.img_centroid)
        self.calculateScore()

        if self.regions_n > 0:
            if config.getDebugMode() >= 1:
                # draw a line between centroids
                plt.plot([self.img_centroid[0], self.group_bbox[4]], [self.img_centroid[1], self.group_bbox[5]])
        
        ax.set_axis_off()
        plt.tight_layout()
            
        if config.getDebugMode() == 1:
            # show labeled image
            plt.show()
        elif config.getDebugMode() == 2:
            # save labeled image
            plt.savefig(config.getLabelingPath(self.img_file))

        # Agregado para liberar memoria
        plt.close(fig)
        plt.cla()
        plt.clf()
        plt.close()
        fig.clear()
        del fig
   
    def calculateCentroid(self, x_side, y_side):
        centroid = [x_side/2, y_side/2]
        return centroid
    
    def calculateImageCentroid(self):
        self.img_centroid = self.calculateCentroid(self.img_width, self.img_height)

    def calculateGroupCentroid(self, x_side, y_side):
        self.group_centroid = self.calculateCentroid(x_side, y_side)

    # calculates distance between two given arrays of coords
    def calculateDistance(self, coords1, coords2):
        x_side = coords2[0]-coords1[0]
        y_side = coords2[1]-coords1[1]
        dist = math.sqrt((x_side)**2+(y_side)**2)
        return dist

    # calculates the score, based on reference distance and centroid-to-centroid distance
    def calculateScore(self):
        self.final_score = format(self.final_distance/self.img_dist, '.2f')

    # returns the image's centroid coordinates [x,y]
    def getImageCentroid(self):
        return self.img_centroid

    # returns number of detected regions on the image (integer)
    def getRegionsN(self):
        return self.regions_n

    # returns the score of the detection
    def getScore(self):
        return self.final_score

    # returns the name of the image file
    def getFileName(self):
        return self.img_file

    # returns the width of the image
    def getImageWidth(self):
        return self.img_width 

    # returns the width of the image
    def getImageHeight(self):
        return self.img_height

    # returns the area of each region detected and filtered
    def getRegionsArea(self):
        return self.regions_area