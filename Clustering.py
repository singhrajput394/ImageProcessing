import os
from glob import glob
import tempfile
import cv2
import numpy as np
from sklearn.cluster import KMeans

import time

def __prepare_cluster_sets__(files, nb_clusters):
        """ Internal function for clustering input image files, returns array of indexs of each input file
        (which determines which cluster a given file belongs)
 
        :param object: base class inheritance
        :type object: class:`Object`
        :param files: list of input image files 
        :type files: python list of opencv numpy images
        :return: Returns array containing index for each file for cluster belongingness 
        :rtype: np.array   
        """

        all_hists = []

        # Calculating the histograms for each image and adding them into **all_hists** list
        for img_file in files:
            img = cv2.cvtColor(img_file, cv2.COLOR_BGR2GRAY)
            hist = cv2.calcHist([img], [0], None, [256], [0, 256])
            hist = hist.reshape((256))
            all_hists.append(hist)

        # Kmeans clustering on the histograms
        kmeans = KMeans(n_clusters=nb_clusters, random_state=0).fit(all_hists)
        labels = kmeans.labels_

        # Identifying the label for each image in the cluster and tagging them
        files_clusters_index_array = []
        for i in np.arange(nb_clusters):
            index_array = np.where(labels == i)
            files_clusters_index_array.append(index_array)

        files_clusters_index_array = np.array(files_clusters_index_array)
        return files_clusters_index_array


def __variance_of_laplacian__(image):
        """Internal function to compute the laplacian of the image and then return the focus
        measure, which is simply the variance of the laplacian,
 
        :param object: base class inheritance
        :type object: class:`Object`
        :param image: input image
        :type image: Opencv Numpy Image   
        :return: result of cv2.Laplacian
        :rtype: opencv image of type CV_64F    
        """

        return cv2.Laplacian(image, cv2.CV_64F).var()


def __get_laplacian_scores(files, n_images):
        """Function to iteratre over each image in the cluster and calculates the laplacian/blurryness 
           score and adds the score to a list
        :param files: list of input filenames 
        :type files: python list of string
        :param n_images: number of images in the given cluster
        :type n_images: int
        :return: Returns list of laplacian scores for each image in the given cluster
        :rtype: python list 
        """

        variance_laplacians = []
        # Iterate over all images in image list
        for image_i in n_images:
            img_file = files[n_images[image_i]]
            img = cv2.cvtColor(img_file, cv2.COLOR_BGR2GRAY)

            # Calculating the blurryness of image
            variance_laplacian = __variance_of_laplacian__(img)
            variance_laplacians.append(variance_laplacian)

        return variance_laplacians



def __get_best_images_index_from_each_cluster__(
        files, files_clusters_index_array
    ):
        """ Internal function returns index of one best image from each cluster
        :param object: base class inheritance
        :type object: class:`Object`
        :param files: list of input filenames 
        :type files: python list of string
        :param files_clusters_index_array: Input is array containing index for each file for cluster belongingness 
        :type: np.array   
        :return: Returns list of filtered files which are best candidate from each cluster
        :rtype: python list 
        """

        filtered_items = []

        # Iterating over every image in each cluster to find the best images from every cluster
        clusters = np.arange(len(files_clusters_index_array))
        for cluster_i in clusters:
            curr_row = files_clusters_index_array[cluster_i][0]
            # kp_lengths = []
            n_images = np.arange(len(curr_row))
            variance_laplacians = __get_laplacian_scores(files, n_images)

            # Selecting image with low burr(high laplacian) score
            selected_frame_of_current_cluster = curr_row[np.argmax(variance_laplacians)]
            filtered_items.append(selected_frame_of_current_cluster)

        return filtered_items


def select_best_frames(input_key_frames, number_of_frames):
        """[summary] Public function for Image selector class: takes list of key-frames images and number of required
        frames as input, returns list of filtered keyframes
        :param object: base class inheritance
        :type object: class:`Object`
        :param input_key_frames: list of input keyframes in list of opencv image format 
        :type input_key_frames: python list opencv images
        :param number_of_frames: Required number of images 
        :type: int   
        :return: Returns list of filtered image files 
        :rtype: python list of images
        """

        nb_clusters = 20#number_of_frames/2

        filtered_images_list = []

        # Selecting only those images which have good brishtness and contrast
        #input_key_frames = self.__filter_optimum_brightness_and_contrast_images__(
        #    input_key_frames
        #)
        
        # Selecting the best images from each cluster by first preparing the clusters on basis of histograms 
        # and then selecting the best images from every cluster
        if len(input_key_frames) >= nb_clusters:
            files_clusters_index_array = __prepare_cluster_sets__(input_key_frames, nb_clusters)
            selected_images_index = __get_best_images_index_from_each_cluster__(
                input_key_frames, files_clusters_index_array
            )

            for index in selected_images_index:
                img = input_key_frames[index]
                filtered_images_list.append(img)
        else:
            # if number of required files are less than requested key-frames return all the files
            for img in input_key_frames:
                filtered_images_list.append(img)
        return filtered_images_list



if not os.path.exists('clusterscartoon'): 
	os.makedirs('clustersCartoon')

X_data = []
files = glob('C:/Users/abhishes/Source/Repos/HackAthon/HackAthon/dataCartoon/*.jpg')
for myFile in files:
    print(myFile)
    image = cv2.imread (myFile)
    X_data.append (image)

filtered_images_list = select_best_frames(X_data, 54)
i=0
for img in filtered_images_list:
    name = './clustersCartoon/frame' + str(i) + '.jpg'
    cv2.imwrite(name, img)
    i= i+1