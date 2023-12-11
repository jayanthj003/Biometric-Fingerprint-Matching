import os
import cv2

# Load the sample fingerprint image
sample = cv2.imread("SOCOFing/Altered/Altered-Easy/2__F_Left_little_finger_Zcut.BMP")

#sample = cv2.resize(sample,None,fx=2.5,fy=2.5)

# cv2.imshow("Sample",sample)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

# Feature matching/Key point matching

# Initialize variables to track the best match
best_score = 0
filename = None
image = None

# Keypoints of sample image and original image and plot the connections between the individual key points
# Initialize variables for keypoints and matches for visualization
kp1, kp2, mp = None, None, None

# Algorithm to find the best match
for file in [file for file in os.listdir("SOCOFing\Real")]:
    # Read a real fingerprint image
    fingerprint_image = cv2.imread("SOCOFing/Real/" + file)

    # create a scale invariant feature transform(SIFT) object
    # SIFT object allows us to extract key points and descriptors for the individual images
    sift = cv2.SIFT_create()

    # keypoints - points in an image that are particularly interesting and stand out in some way
    # descriptors - ways of describing these key points
    # Detect keypoints and compute descriptors for the sample and real images
    keypoints_1, descriptors_1 = sift.detectAndCompute(sample,None)
    keypoints_2, descriptors_2 = sift.detectAndCompute(fingerprint_image,None)

    # for these keypoints find the matches
    # Perform keypoint matching using FLANN-based matcher
    matches = cv2.FlannBasedMatcher({'algorithm': 1, 'trees':10},{}).knnMatch(descriptors_1,descriptors_2,k=2)  
    # 1 - kd3 (data structure)
    # Flann - fast library for approximate nearest neighbors (approximately a good/best match)

    # find the relevant matches
    # Filter out relevant matches based on a distance threshold
    match_points = []
    for p, q in matches:
        # define a threshold for the tuple of two matches
        if p.distance < 0.1 * q.distance: # match to be relevant 
            match_points.append(p) 
        
    # Determine the number of keypoints for score calculation
    keypoints = min(len(keypoints_1), len(keypoints_2))
    
    # calculate the score
    if len(match_points) / keypoints * 100 > best_score:
        best_score = len(match_points) / keypoints * 100
        filename = file
        image = fingerprint_image
        kp1, kp2, mp = keypoints_1, keypoints_2, match_points

print("BEST MATCH: " + filename)
print("SCORE: " + str(best_score))

# draw the matches and resize the result image for visualization
result = cv2.drawMatches(sample,kp1,image,kp2,mp,None)
result = cv2.resize(result,None,fx=4,fy=4)
cv2.imshow("Result",result)
cv2.waitKey(0)
cv2.destroyAllWindows()
