Compute B-Spline

from PIL import Image, ImageOps

im = Image.open("/Users/laiglejm/Documents/Belmont/Code/simple-daisies/Issac.jpeg")
plt.imshow(im)
plt.show()
imagegray = ImageOps.grayscale(im)
image = np.array(imagegray).astype(np.float32)