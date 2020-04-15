import os
import sys

import cv2
import numpy as np
import pydicom as dicom

import logging

def setup_dest(dest_path):
    if os.path.exists(dest_path) and os.path.isdir(dest_path):
        return
    try:
        os.mkdir(dest_path)
    except OSError:
        logging.warning('Could not access destination folder', exc_info=True)

def conversion(dicom_path, dest_path, file_format):
    formats = {
        'PNG': '.png',
        'JPEG':'.jpg',
        'BMP': '.bmp'
    }
    image_list = []

    if dicom_path.endswith('.dcm'):
        image_list.append(dicom_path)
        logging.info('Identified source as a single DCM file')
    else:
        image_list = os.listdir(dicom_path)
        logging.info('Identified source folder with %d files', len(image_list))

    total_conversion = 0
    for image in image_list:
        try:
            ds = dicom.dcmread(os.path.join(dicom_path, image))
            shape = ds.pixel_array.shape

            image_2d = ds.pixel_array.astype(float)

            image_2d_scaled = (np.maximum(image_2d, 0) / image_2d.max()) * 255.0

            image_2d_scaled = np.uint8(image_2d_scaled)
            
            image = image.replace('.dcm', formats[file_format])

            cv2.imwrite(os.path.join(dest_path, image), image_2d_scaled)

            logging.info('Successfully converted %s', image)
            total_conversion += 1
        except:
            logging.warning('Could not convert %s', image)
    logging.info('Successfully converted %d files', total_conversion)


def print_usage():
    print('Usage: \npython dicomConverter.py [src] [dest_folder] [file_format]\n\
        Refer to README for more inforamtion.')



if __name__ == "__main__":
    if len(sys.argv) == 1 or '--help' in sys.argv or '-h' in sys.argv:
        print_usage()
        quit()
    if '-q' in sys.argv:
        logging.basicConfig(level=logging.WARNING, format='%(levelname)s: %(message)s')
    else:
        logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
    try:
        src, dest_folder, file_format = sys.argv[1:]
        setup_dest(dest_folder)
        conversion(src, dest_folder, file_format)
    except ValueError:
        print_usage()