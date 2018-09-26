from skimage import io
from skimage.transform import resize
from glob import glob

path = sorted(glob('./imagenes/B*.png'))

im = io.imread('./imagenes/B_1_iniciom.png')

im = resize(im, [128, 128], anti_aliasing=True)

io.imsave('./imagenes/B_1_inicio.png', im)
