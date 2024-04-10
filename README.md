## Harmony-Image

#### HarmonyImage is a fast and efficient tool for finding similar images based on structural similarity and keypoint matching in images. The application allows users to upload images or provide URLs to images, which are then compared against a database of images to find the most similar ones. To calculate similar images, the application uses asynchronous functions to download images from external sources and then process them.
![image](https://wikimedia.org/api/rest_v1/media/math/render/svg/4203f29f732e5cdc9d8a95907ef6d8e12f08ca09)
#### The SSIM formula is based on three comparative measurements between the X and Y samples, brightness, contrast and structure. Separatecomparison functions:
![image](https://wikimedia.org/api/rest_v1/media/math/render/svg/96b4f1c3840c3707a93197798dcbfbfff24fa92b)
![image](https://wikimedia.org/api/rest_v1/media/math/render/svg/fcda97086476fa420b3b06568a0d202980a600d0)
![image](https://wikimedia.org/api/rest_v1/media/math/render/svg/1aebd62ba5b7e6ae47780ccfa659333f078d6eac)
#### The excluded SSIM index ranges from -1 to +1. The value of +1 is achieved only with complete authenticity of the samples. As a rule, the metric is designed for an 8×8 pixel window.
#### To compare images, SSIM (Structural Similarity Index) is used to assess the similarity of images, as well as the ORB (Oriented FAST and Rotated BRIEF) algorithm to detect key points and their descriptors.

#### ORB (Oriented FAST and Rotated BRIEF) is a method used in computer vision, especially popular for tasks related to object recognition, image matching, and tracking. It's aimed at quickly finding key points in images and describing them in a way that allows for efficient comparison. Let's break down what ORB does into simpler terms:

Using the ORB algorithm, key points and descriptors are determined for both the current and target images.
![image](https://i.stack.imgur.com/spSvt.png)
#### The found key points are compared with each other to determine matches. These matches allow assessing the similarity of images from a perspective other than SSIM. The final similarity score is calculated as the average between the SSIM score and the relative number of matching key points (using the ORB algorithm), providing a comprehensive approach to analyzing the similarity of images.
