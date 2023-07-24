import os
import re
import shutil
import utm
from glob import glob
from tqdm import tqdm
from scipy.io import loadmat

def format_coord(num, left=2, right=5):
    """Return the formatted number as a string with (left) int digits 
            (including sign '-' for negatives) and (right) float digits.
    >>> format_coord(1.1, 3, 3)
    '001.100'
    >>> format_coord(-0.123, 3, 3)
    '-00.123'
    """
    sign = "-" if float(num) < 0 else ""
    num = str(abs(float(num))) + "."
    integer, decimal = num.split(".")[:2]
    left -= len(sign)
    return f"{sign}{int(integer):0{left}d}.{decimal[:right]:<0{right}}"


def format_location_info(latitude, longitude):
    easting, northing, zone_number, zone_letter = utm.from_latlon(float(latitude), float(longitude))
    easting = format_coord(easting, 7, 2)
    northing = format_coord(northing, 7, 2)
    latitude = format_coord(latitude, 3, 5)
    longitude = format_coord(longitude, 4, 5)
    return easting, northing, zone_number, zone_letter, latitude, longitude


def format_image_name(latitude, longitude, pano_id=None, tile_num=None, heading=None,
                       pitch=None, roll=None, height=None, timestamp=None, note=None, extension=".jpg"):
    easting, northing, zone_number, zone_letter, latitude, longitude = format_location_info(latitude, longitude)
    tile_num  = f"{int(float(tile_num)):02d}" if tile_num  is not None else ""
    heading   = f"{int(float(heading)):03d}"  if heading   is not None else ""
    pitch     = f"{int(float(pitch)):03d}"    if pitch     is not None else ""
    timestamp = f"{timestamp}"                if timestamp is not None else ""
    note      = f"{note}"                     if note      is not None else ""
    # assert is_valid_timestamp(timestamp), f"{timestamp} is not in YYYYMMDD_hhmmss format"
    if roll is None: roll = ""
    else: raise NotImplementedError()
    if height is None: height = ""
    else: raise NotImplementedError()
    
    return f"@{easting}@{northing}@{zone_number:02d}@{zone_letter}@{latitude}@{longitude}" + \
        f"@{pano_id}@{tile_num}@{heading}@{pitch}@{roll}@{height}@{timestamp}@{note}@{extension}"


class Format_Datasets():

    def __init__(self, datasets_folder):

        self.datasets_folder = datasets_folder

        self.raw_dataset_path = os.path.join(self.datasets_folder, "raw")
        self.raw_pittsburgh_dataset_path = os.path.join(self.raw_dataset_path, "pittsburgh")
        self.raw_tokyo_dataset_path = os.path.join(self.raw_dataset_path, "tokyo")

        self.nightstreet_path = os.path.join(self.datasets_folder, "nightstreet")
        self.trainA_path = os.path.join(self.nightstreet_path, "trainA")
        self.trainB_path = os.path.join(self.nightstreet_path, "trainB")
        self.testA_path = os.path.join(self.nightstreet_path, "testA")
        self.testB_path = os.path.join(self.nightstreet_path, "testB")

        self.tokyo247_path = os.path.join(self.datasets_folder, "tokyo247")
        self.pitts30k_n_path = os.path.join(self.datasets_folder, "pitts30k")

        os.makedirs(self.raw_pittsburgh_dataset_path, exist_ok=True)
        os.makedirs(self.raw_tokyo_dataset_path, exist_ok=True)

        os.makedirs(self.tokyo247_path, exist_ok=True)
        os.makedirs(self.pitts30k_n_path, exist_ok=True) 

        os.makedirs(self.trainA_path, exist_ok=True)
        os.makedirs(self.trainB_path, exist_ok=True)
        os.makedirs(self.testA_path, exist_ok=True)
        os.makedirs(self.testB_path, exist_ok=True)
        

    def aachenDN_to_nightstreet(self):
        '''
        Build the NightStreet dataset from the Aachen Day/Night dataset (v1 and v1.1).
        Link addresses:
        https://data.ciirc.cvut.cz/public/projects/2020VisualLocalization/Aachen-Day-Night/images/database_and_query_images.zip
        https://data.ciirc.cvut.cz/public/projects/2020VisualLocalization/Aachen-Day-Night/aachen_v1_1.zip
        '''
        raw_aachenDNv11_path = os.path.join(self.raw_dataset_path, "aachen_v1_1")
        shutil.unpack_archive(os.path.join(self.raw_dataset_path, "aachen_v1_1.zip"), raw_aachenDNv11_path)
        images_paths = sorted(glob(os.path.join(raw_aachenDNv11_path, "images_upright/query/night/nexus5x_additional_night", "*.jpg")))
        for index, image_path in tqdm(enumerate(images_paths), desc = f"Copy data to {self.nightstreet_path}", ncols = 100):
            image_name = image_path.split("/")[-1]
            shutil.copy(image_path, os.path.join(self.trainB_path, image_name))

        raw_aachenDNv1_path = os.path.join(self.raw_dataset_path, "database_and_query_images")
        shutil.unpack_archive(os.path.join(self.raw_dataset_path, "database_and_query_images.zip"), 
                              raw_aachenDNv1_path)
        images_paths = sorted(glob(os.path.join(raw_aachenDNv1_path, "images_upright/query/night/nexus5x", "*.jpg")))
        for index, image_path in tqdm(enumerate(images_paths), desc = f"Copy data to {self.nightstreet_path}", ncols = 100):
            image_name = image_path.split("/")[-1]
            shutil.copy(image_path, os.path.join(self.trainB_path, image_name))

        images_paths = sorted(glob(os.path.join(raw_aachenDNv1_path, "images_upright/db", "*.jpg")))
        for index, image_path in tqdm(enumerate(images_paths), desc = f"Copy data to {self.nightstreet_path}", ncols = 100):
            if index%20 == 0:
                image_name = image_path.split("/")[-1]
                shutil.copy(image_path, os.path.join(self.trainA_path, image_name))


    def tokyo247_to_nightstreet(self):
        '''
        Build the NightStreet dataset from the Tokyo 24/7 dataset (v3).
        Link address:
        http://www.ok.ctrl.titech.ac.jp/~torii/project/247/download/247query_v3.zip
        '''
        shutil.unpack_archive(os.path.join(self.raw_dataset_path, "247query_v3.zip"), self.raw_dataset_path)
        raw_tokyo247_path = os.path.join(self.raw_dataset_path, "247query_v3")
        images_paths = sorted(glob(os.path.join(raw_tokyo247_path, "*.jpg")))
        for index, image_path in tqdm(enumerate(images_paths), desc = f"Copy data to {self.nightstreet_path}", ncols = 100):
            image_name = image_path.split("/")[-1]
            if index%3 == 0:
                shutil.copy(image_path, os.path.join(self.trainA_path, image_name))
            elif index%3 == 2:
                shutil.copy(image_path, os.path.join(self.trainB_path, image_name))

    def build_nightcity(self):
        shutil.unpack_archive(os.path.join(self.raw_dataset_path, "nightcity.zip"), self.datasets_folder)


    def build_sf_xl_small(self):
        shutil.unpack_archive(os.path.join(self.raw_dataset_path, "small.zip"), self.datasets_folder)
        os.rename(os.path.join(self.datasets_folder, 'small'), os.path.join(self.datasets_folder, "sf_xl_small_n"))


    def copy_pitts_images(self, target_folder, images_paths, utms):
        os.makedirs(target_folder, exist_ok=True)
        for image_path, (utm_east, utm_north) in zip(tqdm(images_paths, desc=f"Copy to {target_folder}", ncols=100), utms):
            image_name = os.path.basename(image_path)
            latitude, longitude = utm.to_latlon(utm_east, utm_north, 17, "T")
            pitch = int(re.findall('pitch(\d+)_', image_name)[0])-1
            yaw =   int(re.findall('yaw(\d+)\.', image_name)[0])-1
            note = re.findall('_(.+)\.jpg', image_name)[0]
            tile_num = pitch*24 + yaw
            save_image_name = format_image_name(latitude, longitude, pano_id=image_name.split("_")[0],
                                                tile_num=tile_num, note=note)
            source_path = os.path.join(self.raw_pittsburgh_dataset_path, image_path)
            target_path = os.path.join(target_folder, save_image_name)
            shutil.copy(source_path, target_path)


    def build_pitts30k(self):
        for dataset in ["train", "val", "test"]:
            matlab_struct_file_path = os.path.join(self.raw_pittsburgh_dataset_path, "index", f"pitts30k_{dataset}.mat")
            mat_struct = loadmat(matlab_struct_file_path)["dbStruct"].item()
            # Database
            g_images = [f[0].item() for f in mat_struct[1]]
            g_utms = mat_struct[2].T
            self.copy_pitts_images(os.path.join(self.pitts30k_n_path, dataset, 'database'), g_images, g_utms)
            # Queries
            q_images = [os.path.join("queries_real", f"{f[0].item()}") for f in mat_struct[3]]
            q_utms = mat_struct[4].T
            self.copy_pitts_images(os.path.join(self.pitts30k_n_path, dataset, 'queries'), q_images, q_utms)

    
    def build_tokyo247(self):
        pass


    def build_aachenDN(self):
        pass


if __name__ == "__main__":
    formater = Format_Datasets("./datasets")
    # formater.build_nightcity()
    # formater.tokyo247_to_nightstreet()
    # formater.aachenDN_to_nightstreet()
    formater.build_sf_xl_small()
    # formater.build_pitts30k()


