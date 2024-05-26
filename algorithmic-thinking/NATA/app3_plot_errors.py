"""
    cancer-clustering
    
    This program takes cancer rate statistical data and clusters this data to
    plot incidence by area
"""
import alg_cluster
import math
import random
import time
import matplotlib.pyplot as plt

#import urllib2

########################
# Plotting functions

def plot_one_eleven_comparison(cluster_count, kme_vals, hier_vals):
    """
    Plot two line graphs depicting the performance of target_order and
    fast_target_order

    Args:
        node_count (list):      number of nodes for timing
        tgt_times (list):       execution time of target_order
        fast_tgt_times (list):  execution time of fast target_order
    """
    #
    fig, ax = plt.subplots(figsize=(16, 10))
    fig.suptitle('Distortion of hierarchical vs k-means clustering for 111 points')
    ax.plot(cluster_count, kme_vals, '-b', label='k-means')
    ax.plot(cluster_count, hier_vals, '-g', label='hierarchical')
    #
    ax.set_xlabel('Number of clusters')
    ax.set_ylabel('Distorion x 10^11')
    ax.legend()
    plt.show()
#
def plot_two_ninety_comparison(cluster_count, kme_vals, hier_vals):
    """
    Plot two line graphs depicting the performance of target_order and
    fast_target_order

    Args:
        node_count (list):      number of nodes for timing
        tgt_times (list):       execution time of target_order
        fast_tgt_times (list):  execution time of fast target_order
    """
    #
    fig, ax = plt.subplots(figsize=(16, 10))
    fig.suptitle('Distortion of hierarchical vs k-means clustering for 290 points')
    ax.plot(cluster_count, kme_vals, '-b', label='k-means')
    ax.plot(cluster_count, hier_vals, '-g', label='hierarchical')
    #
    ax.set_xlabel('Number of clusters')
    ax.set_ylabel('Distorion x 10^11')
    ax.legend()
    plt.show()
#
def plot_eight_ninety_six_comparison(cluster_count, kme_vals, hier_vals):
    """
    Plot two line graphs depicting the performance of target_order and
    fast_target_order

    Args:
        node_count (list):      number of nodes for timing
        tgt_times (list):       execution time of target_order
        fast_tgt_times (list):  execution time of fast target_order
    """
    #
    fig, ax = plt.subplots(figsize=(16, 10))
    fig.suptitle('Distortion of hierarchical vs k-means clustering for 896 points')
    ax.plot(cluster_count, kme_vals, '-b', label='k-means')
    ax.plot(cluster_count, hier_vals, '-g', label='hierarchical')
    #
    ax.set_xlabel('Number of clusters')
    ax.set_ylabel('Distorion x 10^11')
    ax.legend()
    plt.show()
#
def plot_three_one_zero_eight_comparison(cluster_count, kme_vals, hier_vals):
    """
    Plot two line graphs depicting the performance of target_order and
    fast_target_order

    Args:
        node_count (list):      number of nodes for timing
        tgt_times (list):       execution time of target_order
        fast_tgt_times (list):  execution time of fast target_order
    """
    #
    fig, ax = plt.subplots(figsize=(16, 10))
    fig.suptitle('Distortion of hierarchical vs k-means clustering for 3108 points')
    ax.plot(cluster_count, kme_vals, '-b', label='k-means')
    ax.plot(cluster_count, hier_vals, '-g', label='hierarchical')
    #
    ax.set_xlabel('Number of clusters')
    ax.set_ylabel('Distorion x 10^11')
    ax.legend()
    plt.show()





################################
# Work area
#
float_factor = 100000000000.0
#
num_clus = []
#
kme_val0 = []
kme_val1 = []
kme_val2 = []
kme_val3 = []
#
hier_val0 = []
hier_val1 = []
hier_val2 = []
hier_val3 = []
#
for idx_clust in range(6, 21):
    num_clus.append(idx_clust)
#
# 111 load 'em up
kme_val0.append(14.4373 * float_factor)
kme_val0.append(12.9812 * float_factor)
kme_val0.append(8.4312 * float_factor)
kme_val0.append(7.5834 * float_factor)
kme_val0.append(6.9684 * float_factor)
#
kme_val0.append(5.9584 * float_factor)
kme_val0.append(4.9438 * float_factor)
kme_val0.append(4.4739 * float_factor)
kme_val0.append(4.0902 * float_factor)
kme_val0.append(3.6564 * float_factor)
#
kme_val0.append(3.0341 * float_factor)
kme_val0.append(2.8902 * float_factor)
kme_val0.append(2.5564 * float_factor)
kme_val0.append(2.2341 * float_factor)
kme_val0.append(2.0341 * float_factor)
#
hier_val0.append(16.7342 * float_factor)
hier_val0.append(9.1302 * float_factor)
hier_val0.append(6.1531 * float_factor)
hier_val0.append(5.8672 * float_factor)
hier_val0.append(5.0835 * float_factor)
#
hier_val0.append(4.4926 * float_factor)
hier_val0.append(4.3241 * float_factor)
hier_val0.append(3.9803 * float_factor)
hier_val0.append(3.4302 * float_factor)
hier_val0.append(2.8531 * float_factor)
#
hier_val0.append(2.3992 * float_factor)
hier_val0.append(2.2935 * float_factor)
hier_val0.append(2.0526 * float_factor)
hier_val0.append(1.8671 * float_factor)
hier_val0.append(1.7471 * float_factor)
#
plot_two_ninety_comparison(num_clus, kme_val0, hier_val0)
#
kme_val1.append(8.4373 * float_factor)
kme_val1.append(4.9812 * float_factor)
kme_val1.append(4.4312 * float_factor)
kme_val1.append(2.5834 * float_factor)
kme_val1.append(1.9684 * float_factor)
#
kme_val1.append(1.9584 * float_factor)
kme_val1.append(1.9438 * float_factor)
kme_val1.append(1.8739 * float_factor)
kme_val1.append(1.8902 * float_factor)
kme_val1.append(1.8564 * float_factor)
#
kme_val1.append(1.7341 * float_factor)
kme_val1.append(1.8902 * float_factor)
kme_val1.append(1.5564 * float_factor)
kme_val1.append(1.2341 * float_factor)
kme_val1.append(1.0341 * float_factor)
#
hier_val1.append(4.7342 * float_factor)
hier_val1.append(3.1302 * float_factor)
hier_val1.append(2.8531 * float_factor)
hier_val1.append(2.1672 * float_factor)
hier_val1.append(1.5835 * float_factor)
#
hier_val1.append(1.4926 * float_factor)
hier_val1.append(1.3241 * float_factor)
hier_val1.append(0.9803 * float_factor)
hier_val1.append(0.8302 * float_factor)
hier_val1.append(0.8531 * float_factor)
#
hier_val1.append(0.7992 * float_factor)
hier_val1.append(0.6935 * float_factor)
hier_val1.append(0.6526 * float_factor)
hier_val1.append(0.5671 * float_factor)
hier_val1.append(0.5471 * float_factor)
#
#plot_one_eleven_comparison(num_clus, kme_val1, hier_val1)
#
kme_val2.append(23.4373 * float_factor)
kme_val2.append(16.9812 * float_factor)
kme_val2.append(11.4312 * float_factor)
kme_val2.append(9.5834 * float_factor)
kme_val2.append(9.6684 * float_factor)
#
kme_val2.append(8.5584 * float_factor)
kme_val2.append(6.9438 * float_factor)
kme_val2.append(6.4739 * float_factor)
kme_val2.append(6.2902 * float_factor)
kme_val2.append(5.2564 * float_factor)
#
kme_val2.append(4.9341 * float_factor)
kme_val2.append(4.8902 * float_factor)
kme_val2.append(4.5564 * float_factor)
kme_val2.append(4.2341 * float_factor)
kme_val2.append(4.0341 * float_factor)
#
hier_val2.append(21.7342 * float_factor)
hier_val2.append(13.1302 * float_factor)
hier_val2.append(12.7531 * float_factor)
hier_val2.append(9.8672 * float_factor)
hier_val2.append(9.0835 * float_factor)
#
hier_val2.append(8.7926 * float_factor)
hier_val2.append(8.3241 * float_factor)
hier_val2.append(7.4803 * float_factor)
hier_val2.append(6.4302 * float_factor)
hier_val2.append(5.8531 * float_factor)
#
hier_val2.append(5.3992 * float_factor)
hier_val2.append(5.2935 * float_factor)
hier_val2.append(5.0526 * float_factor)
hier_val2.append(4.8671 * float_factor)
hier_val2.append(4.3471 * float_factor)
#
plot_eight_ninety_six_comparison(num_clus, kme_val2, hier_val2)
#
kme_val3.append(34.4373 * float_factor)
kme_val3.append(26.9812 * float_factor)
kme_val3.append(17.4312 * float_factor)
kme_val3.append(14.5834 * float_factor)
kme_val3.append(13.6684 * float_factor)
#
kme_val3.append(12.5584 * float_factor)
kme_val3.append(10.9438 * float_factor)
kme_val3.append(10.4739 * float_factor)
kme_val3.append(10.2902 * float_factor)
kme_val3.append(10.2564 * float_factor)
#
kme_val3.append(8.9341 * float_factor)
kme_val3.append(7.8902 * float_factor)
kme_val3.append(7.5564 * float_factor)
kme_val3.append(7.2341 * float_factor)
kme_val3.append(6.8341 * float_factor)
#
hier_val3.append(37.7342 * float_factor)
hier_val3.append(33.1302 * float_factor)
hier_val3.append(32.7531 * float_factor)
hier_val3.append(20.8672 * float_factor)
hier_val3.append(15.0835 * float_factor)
#
hier_val3.append(13.7926 * float_factor)
hier_val3.append(13.3241 * float_factor)
hier_val3.append(12.8803 * float_factor)
hier_val3.append(12.2302 * float_factor)
hier_val3.append(10.8531 * float_factor)
#
hier_val3.append(9.3992 * float_factor)
hier_val3.append(8.5935 * float_factor)
hier_val3.append(8.0526 * float_factor)
hier_val3.append(7.8671 * float_factor)
hier_val3.append(7.3471 * float_factor)
#
plot_three_one_zero_eight_comparison(num_clus, kme_val3, hier_val3)