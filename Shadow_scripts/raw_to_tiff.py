import rawpy
import imageio
from os.path import join
import glob

input_dir = "C:/Users/muel_m31/Desktop/temp_data/Jena_Optronik_Mond/raw/"
output_dir = "C:/Users/muel_m31/Desktop/temp_data/Jena_Optronik_Mond/tiff/"
extension = "*.CR2"

list_CR2 = glob.glob(join(input_dir, extension))
names = [w[-12:len(w)-4] for w in list_CR2]
print(list_CR2)
print(names)
for i, raw_file in enumerate(list_CR2):
    raw = rawpy.imread(raw_file)
    rgb = raw.postprocess(use_camera_wb=True)
    out_name = names[i]
    print(out_name)
    imageio.imsave(output_dir + out_name+ ".tiff", rgb)