import os
from glob import glob
from tqdm import tqdm
from PIL import Image

class Format_Datasets():

    def __init__(self, datasets_folder):
        self.datasets_folder = datasets_folder
        self.raw_dataset_paths = os.path.join(self.datasets_folder, "raw")
        self.nightstreet_path = os.path.join(self.datasets_folder, "nightstreet")
        self.trainA_path = os.path.join(self.nightstreet_path, "trainA")
        self.trainB_path = os.path.join(self.nightstreet_path, "trainB")
        self.testA_path = os.path.join(self.nightstreet_path, "testA")
        self.testB_path = os.path.join(self.nightstreet_path, "testB")

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
        raw_aachenDNv11_path = os.path.join(self.raw_dataset_paths, "aachen_v1_1")
        images_paths = sorted(glob(os.path.join(raw_aachenDNv11_path, "images_upright/query/night/nexus5x_additional_night", "*.jpg")))
        for index, image_path in tqdm(enumerate(images_paths), desc = f"Copy data to {self.nightstreet_path}", ncols = 100):
            image_name = image_path.split("/")[-1]
            pil_img = Image.open(image_path)
            pil_img.save(os.path.join(self.trainB_path, image_name))

        raw_aachenDNv1_path = os.path.join(self.raw_dataset_paths, "database_and_query_images")
        images_paths = sorted(glob(os.path.join(raw_aachenDNv1_path, "images_upright/query/night/nexus5x", "*.jpg")))
        for index, image_path in tqdm(enumerate(images_paths), desc = f"Copy data to {self.nightstreet_path}", ncols = 100):
            image_name = image_path.split("/")[-1]
            pil_img = Image.open(image_path)
            pil_img.save(os.path.join(self.trainB_path, image_name))

        images_paths = sorted(glob(os.path.join(raw_aachenDNv1_path, "images_upright/db", "*.jpg")))
        for index, image_path in tqdm(enumerate(images_paths), desc = f"Copy data to {self.nightstreet_path}", ncols = 100):
            if index%20 == 0:
                image_name = image_path.split("/")[-1]
                pil_img = Image.open(image_path)
                pil_img.save(os.path.join(self.trainA_path, image_name))

    def tokyo247_to_nightstreet(self):
        '''
        Build the NightStreet dataset from the Tokyo 24/7 dataset (v3).
        Link address:
        http://www.ok.ctrl.titech.ac.jp/~torii/project/247/download/247query_v3.zip
        '''
        raw_tokyo247_path = os.path.join(self.raw_dataset_paths, "247query_v3")
        images_paths = sorted(glob(os.path.join(raw_tokyo247_path, "*.jpg")))
        for index, image_path in tqdm(enumerate(images_paths), desc = f"Copy data to {self.nightstreet_path}", ncols = 100):
            image_name = image_path.split("/")[-1]
            pil_img = Image.open(image_path)
            if index%3 == 0:
                pil_img.save(os.path.join(self.trainA_path, image_name))
            elif index%3 == 2:
                pil_img.save(os.path.join(self.trainB_path, image_name))
        
    def timelapse(self):
        """
        TODO: Build the NightScape dataset which is larger than the NightStreet dataset
        """
        pass


if __name__ == "__main__":
    
    formater = Format_Datasets("./datasets")
    formater.tokyo247_to_nightstreet()
    formater.aachenDN_to_nightstreet()

