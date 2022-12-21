import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import os
import matplotlib
import networkx as nx


def plot_images_by_id(id_list,file_classes):
    '''
    Plot up to 5 images by id
    '''
    if len(id_list) > 5:
        raise ValueError("Can only plot 5 images")
    loaded_images = []
    for img_id in id_list:
        loaded_images.append(mpimg.imread(os.path.join("Images",file_classes[img_id,0])))
    fig, axes = plt.subplots(1,5)
    for i,image in enumerate(loaded_images):
        axes[i].imshow(image)
        axes[i].axis('off')
    for i in range(len(loaded_images),len(axes)):
        axes[i].set_visible(False)

    plt.title("Images with ids: {}".format(id_list))

def plot_image_by_class_label(classes, file_classes, no_images = 5):
    '''
    Plot no_images (default: 5) from each class.
    '''
    for img_class in np.unique(classes):
        file_by_class = file_classes[np.where(file_classes[:,1]==img_class)]
        images = file_by_class[0:no_images,0]
        loaded_images = []

        rng = np.random.default_rng()
        random_numbers = rng.choice(file_by_class.shape[0], size=no_images, replace=False)
        random_images = file_by_class[random_numbers,0]
        for file_name in random_images:
            loaded_images.append(mpimg.imread(os.path.join("Images",file_name)))

        fig, axes = plt.subplots(1,no_images)

        for ax,image in zip(axes,loaded_images):
            ax.imshow(image)
            ax.axis('off')
        plt.title("Class: {}, ids = {}".format(img_class,random_numbers))
    matplotlib.pyplot.close()

def visualize(G, color=None, figsize=(7,7)):
    if color == "degree":
        degrees = G.degree() #Dict with Node ID, Degree
        nodes = G.nodes()
        color = np.asarray([degrees[n] for n in nodes])
    plt.figure(figsize=figsize)
    plt.xticks([])
    plt.yticks([])
    nx.draw_networkx(G, 
                     pos=nx.spring_layout(G, seed=42),
                     with_labels=True,
                     node_color=color,
                     cmap="Set2")
    plt.show();
