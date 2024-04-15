#pip install opencv-python

from moviepy.editor import ImageSequenceClip, ImageClip
import moviepy.editor as mp
import numpy as np
import imageio
import random
from moviepy.editor import * 
from PIL import Image
import cv2
import numpy as np
import os





def generate_random_code():
    # Generate a 7-digit random code
    random_code = ''.join([str(random.randint(0, 9)) for _ in range(7)])
    return random_code

#a function to adjust two photos
def adjust(base_image,overlay_image,out):
	base_image = Image.open(base_image)
	overlay_image = Image.open(overlay_image)


	base_width, base_height = base_image.size
	overlay_width, overlay_height = overlay_image.size

	x_position = (base_width - overlay_width) // 2
	y_position = (base_height - overlay_height) // 2

	position = (x_position, y_position) 

	base_image.paste(overlay_image, position)


	base_image.save('outputs/adjusted/{}.jpg'.format(out))
	base_image.show()


#a function to get the contour of a png photo
def draw_contours_jpg(input_image_path, base, out):
    # Read the image in grayscale
    image = cv2.imread(input_image_path, cv2.IMREAD_GRAYSCALE)
    blurred = cv2.GaussianBlur(image, (5, 5), 0)
    _, thresh = cv2.threshold(blurred, 127, 255, cv2.THRESH_BINARY_INV)
    # Find contours using only the external contours
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)


    scale_factor = 2
    base_center = (image.shape[1] // 2, image.shape[0] // 2)
    translation_vector = (base_center[0] - image.shape[1] // 2, base_center[1] - image.shape[0] // 2)
    scaled_contours = [np.int32(scale_factor * (contour - translation_vector)) for contour in contours]


    # Create an empty image for drawing contours
    contour_image = np.zeros_like(image)
    contour_on_base = cv2.imread(base, cv2.IMREAD_COLOR)

    # Draw the contours on the new image
    cv2.drawContours(contour_on_base, scaled_contours, -1, (255, 255, 255), 3)  # White color contour
    # Save the contour image
    cv2.imwrite('outputs/contours/{}.png'.format(out), contour_on_base)


def draw_contours(input_image_path, base, out):
    # Read the image with an alpha channel
    image = cv2.imread(input_image_path, cv2.IMREAD_UNCHANGED)

    # Extract the alpha channel if available, otherwise create one
    alpha_channel = image[:, :, 3] if image.shape[-1] == 4 else np.ones_like(image[:, :, 0], dtype=np.uint8) * 255

    # Convert the image to grayscale
    grayscale_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply threshold to get a binary image and detect contours
    _, thresh = cv2.threshold(grayscale_image, 127, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    center_x = image.shape[1] // 2
    center_y = image.shape[0] // 2

    for contour in contours:
    	for point in contour :
    		point[0][0] += center_x
    		point[0][1] += center_y

    # Create an empty image with an alpha channel for drawing contours
    contour_image = np.zeros_like(image)
    contour_on_base = cv2.imread(base, cv2.IMREAD_COLOR)
    # Draw the contours on the new image
    cv2.drawContours(contour_on_base, contours, -1, (147, 20, 255, 255), 3)  # White color contour with alpha

    # Save the contour image
    cv2.imwrite('outputs/contours/{}.png'.format(out), contour_on_base)



def draw_contours_(input_image_path, out):
    # Read the image in grayscale
    image = cv2.imread(input_image_path, cv2.IMREAD_GRAYSCALE)

    # Apply threshold to get binary image and detect contours
    _, thresh = cv2.threshold(image, 127, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Create an empty image for drawing contours
    contour_image = np.zeros_like(image)

    # Draw the contours on the new image
    cv2.drawContours(contour_image, contours, -1, (255, 255, 255), 3)  # White color contour

    # Save the contour image
    cv2.imwrite('outputs/contours/{}.png'.format(out), contour_image)

def photos_to_video(base_photos, output_video_path, fps=1):
    clips = [mp.ImageClip(image_path, duration=5/fps) for image_path in base_photos]
    # Create the video by concatenating the image clips
    video = mp.concatenate_videoclips(clips, method="compose")
    # Write the video to the output path
    video.write_videofile(output_video_path, fps=fps, codec="libx264")



def read_file_to_list(directory_path):
	file_names = []

	for filename in os.listdir(directory_path):
		if os.path.isfile(os.path.join(directory_path, filename)):
			file_names.append(filename)
	return file_names


def movingPngIntoVideo(img_in, video_in,out):
	video = VideoFileClip(video_in)
	image = ImageClip(img_in, duration = video.duration)

	def random_position(t):
		random_x = random.randint(-50, 50)
		random_y = random.randint(-50, 50)

		new_x = int(100 * t) + random_y #'center'
		new_y = int(100 * t) + random_y

		return new_x, new_y

	print("random position == ", random_position)
	new_clip = image.set_position(random_position)#.resize(height=50)
	final_clip = CompositeVideoClip([video, new_clip])

	final_clip.write_videofile("outputs/final_videos/final_{}.mp4".format(out))

	# video = VideoFileClip(video_in)
	# image = ImageClip(img_in, duration=video.duration) 
	
	# new_clip = image.set_position(lambda t: ('center', int(100 * t)) ).resize(height=50)
	# final_clip = CompositeVideoClip([video , new_clip]) 

	# final_clip.write_videofile("outputs/final_videos/final_{}.mp4".format(out)) 


file_path = "outputs/contours"  # Replace with the path to your file
filenames_list = read_file_to_list('outputs/contours')
print("content ::: ", filenames_list)



caracter_images = read_file_to_list('inputs/caracters')
background_images = read_file_to_list('inputs/backgrounds')

#associate each background with all the caracters
for back in background_images:
	for caracter in caracter_images:
		print("Generating Videos ....")

		num_countour=generate_random_code()
		draw_contours("inputs/caracters/{}".format(caracter),"inputs/backgrounds/{}".format(back),num_countour)
		video_base = ['outputs/contours/{}.png'.format(num_countour),'outputs/contours/{}.png'.format(num_countour),'outputs/contours/{}.png'.format(num_countour)]
		photos_to_video(video_base,'outputs/base_videos/base_{}.mp4'.format(num_countour))
	

		video = 'outputs/base_videos/base_{}.mp4'.format(num_countour)
		image = "inputs/caracters/{}".format(caracter)
		movingPngIntoVideo(image,video,num_countour)

print("Done Generating")		






# from moviepy.editor import ImageSequenceClip

# # List of image file paths
# image_files = ['inputs/1.jpg', 'inputs/1.jpg', 'inputs/1.jpg']

# # Create a video clip
# clip = ImageSequenceClip(image_files, fps=25)  # fps=1 means each image will be displayed for 1 second

# # Write the clip to a file (output_video.mp4)
# clip.write_videofile("outputs/output_video.mp4")


# #a function to get the inputs

# #a function to ajust two photos

# #a function to get the contour of a png photo

# #a function to rotate a png on a jpg

# from moviepy.editor import ImageSequenceClip, ImageClip
# import numpy as np

# print("import the lib")

# image_files = ['inputs/1.jpg', 'inputs/1.jpg', 'inputs/1.jpg']
# size = (1920, 1080)

# # Create a list of Numpy arrays from resized ImageClips
# clips = [ImageClip(img).resize(newsize=size).to_ImageClip_array() for img in image_files]
# video = ImageSequenceClip(clips, fps=2)  # 'fps' is frames per second

# print("clip created")
# video.write_videofile("outputs/output_video.mp4")

# print("video created")

# try:
#     from moviepy.editor import ImageSequenceClip, ImageClip

#     print("import the lib")

#     image_files = ['inputs/1.jpg', 'inputs/2.jpg', 'inputs/3.jpg']

#     size = (1920, 1080)


#     clips = [ImageClip(img).resize(newsize=size) for img in image_files]
#     video = ImageSequenceClip(clips, fps=2)  # 'fps' is frames per second

#     print("clip created")
#     video.write_videofile("outputs/output_video.mp4")

#     print("video created")
# except Exception as e:
#     print(f"An error occurred: {e}")







