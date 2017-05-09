import logging
import time, datetime

# initializes the configuration settings
def initConfig():
    # debug mode:
    #   0 = do nothing, just process
    #   1 = show results
    #   2 = save results
    global DEBUG_MODE
    DEBUG_MODE = 0

    # folder to read images from
    global images_folder
    images_folder = "fotos_dron"
    
    # exclusion margin (in percentage) from the border of the image
    global exclusion_margin
    exclusion_margin = 3
    
    # minimal area to consider detected regions (in pixels)
    global min_area_size
    min_area_size = 400

    # image formats supported
    global supp_formats
    supp_formats = ('jpg', 'png')

    # file extension to save results as
    global results_format
    results_format = '.jpg'

    # name of the results folder
    global results_folder
    results_folder = 'results'

    # suffix to save binary results
    global binary_suffix
    binary_suffix = '_binary'

    # suffix to save labeling results
    global labeling_suffix
    labeling_suffix = '_labeling'

    # threshold (RGB)
    global threshold
    threshold = [(0,51), (0,255), (80,255)]

    #resize image (0 to 1.0, means 0% to 10% of original size)
    global resize
    resize = 1.0

# initializes log file and prints header
def initLog(log_name):
    global st_time
    st_time = datetime.datetime.now()
    logging.basicConfig(filename=log_name + '.log', filemode='w', level=logging.DEBUG)
    logging.info("CURRENT SETTINGS")
    logging.info("Current folder: " + images_folder)
    logging.info("Results folder: %s", results_folder)
    logging.info("Debug mode: %d", DEBUG_MODE)
    logging.info("Supported formats: " + str(supp_formats))
    logging.info("Resize (%): " + str(resize*100))
    logging.info("Exclusion margin (%): " + str(exclusion_margin))
    logging.info("Minimal area size (px): %d", min_area_size)
    logging.info("Binary results path: " + getBinaryPath('*'))
    logging.info("---------------------------------")
    logging.info("Started at: " + str(st_time))
    logging.info("---------------------------------")

# prints results for each object
def printObjInfoToLog(obj):
    logging.info(" File name: " + obj.getFileName() )
    logging.info("    Width (px): " + str(obj.getImageWidth()) )
    logging.info("    Height (px): " + str(obj.getImageHeight()) )
    logging.info("    Regions detected: " + str(obj.getRegionsN()) )
    logging.info("    Regions areas (px): " + str(obj.getRegionsArea()) )
    logging.info("    SCORE (0 to 1.0): " + str(obj.getScore()) )
    logging.info("---------------------------------")

# prints results for a list of objects
def printListInfoToLog(obj_list):
    logging.info("Images processed: " + str(len(obj_list)))

# closes the log file and prints footer
def closeLog():
    fn_time = datetime.datetime.now()
    logging.info("Finished at: " + str(fn_time))
    tot_time = fn_time - st_time
    logging.info("Total time: " + str(tot_time))


# BASIC SETs/GETs METHODS
def setDebugMode(var):
    global DEBUG_MODE
    DEBUG_MODE = var

def getDebugMode():
    return DEBUG_MODE

def setSourceFolderName(var):
    global images_folder
    images_folder = var

def getSourceFolderName():
    return images_folder

def setExclusionMargin(var):
    global exclusion_margin
    exclusion_margin = var

def getExclusionMargin():
    return exclusion_margin

def setMinAreaSize(var):
    global min_area_size
    min_area_size = var

def getMinAreaSize():
    return min_area_size

def setSupportedFormats(var):
    global supp_formats
    supp_formats = var    

def getSupportedFormats():
    return supp_formats

def setResultsFormats(var):
    global results_format
    results_format = "." + var

def getResultsFormats():
    return results_format

def setResultsFolderName(var):
    global results_folder
    results_folder = var

def getResultsFolderName():
    return results_folder

def setBinarySuffix(var):
    global binary_suffix
    binary_suffix = var

def getBinarySuffix():
    return binary_suffix

def setLabelingSuffix(var):
    global labeling_suffix
    labeling_suffix = var

def getLabelingSuffix():
    return labeling_suffix

def setThreshold(var):
    global threshold
    threshold = var

def getThreshold():
    return threshold

def setResize(var):
    global resize
    resize = var

def getResize():
    return resize

# OTHER METHODS
# returns relative path to an original image
def getImagePath(image_name):
    image_path = images_folder + '/' + image_name
    return image_path

# returns relative path to save binary images
def getBinaryPath(image_name):
    binary_path = getSourceFolderName() + '/' + getResultsFolderName() + '/' + image_name + getBinarySuffix() + getResultsFormats()
    return binary_path

# returns relative path to save labeled images
def getLabelingPath(image_name):
    labeling_path = getSourceFolderName() + '/' + getResultsFolderName() + '/' + image_name + getLabelingSuffix() + getResultsFormats()
    return labeling_path