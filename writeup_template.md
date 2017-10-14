## Project: Search and Sample Return

---


**The goals / steps of this project are the following:**  

**Training / Calibration**  

* Download the simulator and take data in "Training Mode"
* Test out the functions in the Jupyter Notebook provided
* Add functions to detect obstacles and samples of interest (golden rocks)
* Fill in the `process_image()` function with the appropriate image processing steps (perspective transform, color threshold etc.) to get from raw images to a map.  The `output_image` you create in this step should demonstrate that your mapping pipeline works.
* Use `moviepy` to process the images in your saved dataset with the `process_image()` function.  Include the video you produce as part of your submission.

**Autonomous Navigation / Mapping**

* Fill in the `perception_step()` function within the `perception.py` script with the appropriate image processing functions to create a map and update `Rover()` data (similar to what you did with `process_image()` in the notebook). 
* Fill in the `decision_step()` function within the `decision.py` script with conditional statements that take into consideration the outputs of the `perception_step()` in deciding how to issue throttle, brake and steering commands. 
* Iterate on your perception and decision function until your rover does a reasonable (need to define metric) job of navigating and mapping.  

[//]: # (Image References)

[image1]: ./misc/rover_image.jpg
[image2]: ./calibration_images/example_grid1.jpg
[image3]: ./calibration_images/example_rock1.jpg 

## [Rubric](https://review.udacity.com/#!/rubrics/916/view) Points
### Here I will consider the rubric points individually and describe how I addressed each point in my implementation.  

---
### Writeup / README

#### 1. Provide a Writeup / README that includes all the rubric points and how you addressed each one.  You can submit your writeup as markdown or pdf.  

### Notebook Analysis
#### 1. Run the functions provided in the notebook on test images (first with the test data provided, next on data you have recorded). Add/modify functions to allow for color selection of obstacles and rock samples.

First, I conducted the experiment by the test images provided. And I constructed the training data by recording via Unity rover environment. 


#### 2. Populate the `process_image()` function with the appropriate analysis steps to map pixels identifying navigable terrain, obstacles and rock samples into a worldmap.  Run `process_image()` on your test data using the `moviepy` functions provided to create video output of your result. 

I've included the movie clip representing driving images and processed image (the navigable terrain, world map).

#### 1. Fill in the `perception_step()` (at the bottom of the `perception.py` script) and `decision_step()` (in `decision.py`) functions in the autonomous mapping scripts and an explanation is provided in the writeup of how and why these functions were modified as they were.

I used the perception_step as similar as the process_image function since it is reasonable and working well. 
In the decision_step, I was struggling with the rover to make it drive autonomously at the beginning. I tried to apply k-means clustering to get the right direction when they meet the cross road. I adjusted some parameters to make it drive well but those tries make the rover weird and rough. Finally, I found out the way to satisfy the criteria (The rover must map at least 40% of the environment with 60% fidelity (accuracy) against the ground truth). Actually, that was simple. That is to give some bias rover to go to the left direction. In order to do that, I added the half of the standard deviation of nav_angles to the mean value of the nav_angles. That makes the rover to go slightly sticking with the wall on the left side of the rover. It is like a finding a path in a maze. By using this simple solution, I could achieve the criteria.

`Rover.steer = np.clip((np.mean(Rover.nav_angles) + np.std(Rover.nav_angles)/2)* 180 / np.pi, -20, 20)`

#### 2. Launching in autonomous mode your rover can navigate and map autonomously.  Explain your results and how you might improve them in your writeup.  

Aside from the biased driving strategy, I added the stuck_mode to handle the rover when it comes to the stucked situation.
If the velocity of the rover is lower than 0.05, I increased the stuck_count one. And if the stuck_count reaches 20, then the state of the rover would be changed to the stuck_mode. In the stuck_mode, the rover a little go back out and roll the steer.

[Result image]



