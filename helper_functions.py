# Helper Functions for rendering visual input
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

def show_rgb(image_array):
    """
    Given an image array, show the image
    in RGB mode. Does not save.
    """
    b = image_array*255.999
    img = Image.fromarray(b.astype(np.uint8), 'RGB')
    img.show()

def show_depth(image_array):
    """
    Given an image depth array, show the depth
    image in RGB mode. Does not save.
    """
    b = ((image_array - image_array.min()) / (image_array.max() - image_array.min())*255.999)
    img = Image.fromarray(b.astype(np.uint8), 'L')
    img.show()

def show_all_rgb(observation):
    """
    Given an observation object, stack
    the Left, Right, Front and Wrist
    RGB input and render.
    """
    show_rgb(np.concatenate([observation.left_shoulder_rgb, observation.right_shoulder_rgb, observation.wrist_rgb, observation.front_rgb], axis=1))

def show_all_depth(observation):
    """
    Given an observation object, stack
    the Left, Right, Front and Wrist
    depth input and render.
    """
    show_depth(np.concatenate([observation.left_shoulder_depth, observation.right_shoulder_depth, observation.wrist_depth, observation.front_depth], axis=1))

def save_rgb(image_array, file_name):
    """
    Given an image array, save the image
    in RGB mode.
    """
    b = image_array*255.999
    img = Image.fromarray(b.astype(np.uint8), 'RGB')
    img.save(file_name+'.png')

def save_depth(image_array, file_name):
    """
    Given an image depth array, save the depth
    image in RGB mode.
    """
    b = ((image_array - image_array.min()) / (image_array.max() - image_array.min())*255.999)
    img = Image.fromarray(b.astype(np.uint8), 'L')
    img.save(file_name+'.png')
    
def save_all_rgb(observation, file_name):
    """
    Given an observation object, stack
    the Left, Right, Front and Wrist
    RGB input and save.
    """
    save_rgb(np.concatenate([observation.left_shoulder_rgb, observation.right_shoulder_rgb, observation.wrist_rgb, observation.front_rgb], axis=1), file_name)

def save_all_depth(observation, file_name):
    """
    Given an observation object, stack
    the Left, Right, Front and Wrist
    depth input and save.
    """
    save_depth(np.concatenate([observation.left_shoulder_depth, observation.right_shoulder_depth, observation.wrist_depth, observation.front_depth], axis=1), file_name)
    
    
def show_observations(obs):
    """
    Given an observation object,
    print the RGB and Depth image
    frames.
    """
    stacked_rgb = np.concatenate([obs.left_shoulder_rgb, obs.right_shoulder_rgb, obs.wrist_rgb, obs.front_rgb], axis=1)
    stacked_depth = np.concatenate([obs.left_shoulder_depth, obs.right_shoulder_depth, obs.wrist_depth, obs.front_depth], axis=1)
    for image in [stacked_rgb, stacked_depth]:
        plt.figure(num=None, figsize=(12,8), dpi=80, facecolor='w', edgecolor='k')
        plt.imshow(image)