This is the official implementation of the paper "NPR: Nocturnal Place Recognition Using Nighttime Translation in Large-Scale Training Procedures".

```shell
git clone https://github.com/BinuxLiu/npr.git
git submodule init
git submodule update
```


## Reproduce our results

If you want to reproduce our experiment from start to finish, please perform each step below. 
(It takes a long time to train the night generation model and generate night data.) 
If you want to train the VPR model on the night data we generated, skip to step 4 after performing step 1. 
If you just want to test our model on a public dataset, skip to step 5 after step 1.

1. Generate and unzip the NightStreet, NightCity and VPR datasets.
    * First, run the following command:
        ```shell
        # Initialize the folders of datasets
        python format_datasets.py --datasets_folder /path/to/datasets
        ```
    * Then, you need to download AachenDN (v1, v1.1), Tokyo247 (v2, v3, and database), Pittsburgh, SF-XL-small dataset to the **/path/to/datasets/raw** folder.
      The download links of above datasets are written in the comments of `format_datasets.py`.
      In **/path/to/datasets/raw/pittsburgh** there should be the following folders: 000, 001, 002, 003, 004, 005, 006, queries_real, index. (index is a folder that contains files such as pitts30k_train.mat).
      Except for the Pittsburgh and Tokyo 247 dataset, none of the other datasets require you to manually decompress them.
    * Run the following command again:
        ```shell
        python format_datasets.py --datasets_folder /path/to/datasets/ --datasets aachen_tokyo_pitts_sfxl
        ```
    * If you are using our pre-generated nightstreet dataset, you can skip the above step. You can download the NightStreet dataset directly from here and merge it with the `./datasets/nightstreet` folder after extracting it.


2. Train NEG-CUT on NightCity(NightStreet) dataset 
    * To train NEG-CUT on the NightCity dataset, run the following command in the terminal:
        ```shell
        # terminal_1
        python -m visdom.server
        ```
        ```shell
        # terminal_2
        python train.py --dataroot ./datasets/nightstreet --name maps_cyclegan --model cycle_gan --load_size 512 --crop_size 512 --preprocess scale_shortside_and_crop
        cd ./third_party/NEGCUT
        # NightStreet
        python train.py --dataroot ../../datasets/nightstreet --checkpoints_dir ../../checkpoints --name nightstreet --NEGCUT_mode negcut --model negcut --load_size 512 --crop_size 512 --preprocess scale_shortside_and_crop
        # NightCity
        python train.py --dataroot ../../datasets/nightcity --checkpoints_dir ../../checkpoints --name nightcity --NEGCUT_mode negcut --model negcut --load_size 512 --crop_size 512 --preprocess scale_shortside_and_crop
        ```
    * If you are using our pre-trained night generator or pre-generated VPR-Night datasets, you can **skip this step**.

3. Generate VPR-Night datasets by processing VPR datasets
    * To generate the VPR-Night dataset by processing the VPR dataset, run the following command in the terminal:

        ```shell
        python test.py --dataroot ../../datasets/sf_xl/small/train --name nightcity --NEGCUT_mode negcut --model negcut --checkpoints_dir ../../checkpoints --load_size 512 --preprocess none --dataset_mode vpr
        ```
    * If you are using our pre-generated VPR-Night dataset, you can **skip this step**.

    Generate the features of VPR datasets for supervising the NPR model
    ```
    python eval.py --dataset_folder ../../datasets/sf_xl/small --backbone ResNet50 --fc_output_dim 2048 --resume_model ./logs/official/ResNet50_2048_cosplace.pth --use_kd --infer_batch_size 1
    ```

4. Train or fine-tuning VPR methods on VPR-Night datasets
    * Training CosPlace on sf_xl_small_n:
        ```shell
        python train.py --dataset_folder ../../datasets/sf_xl/small/ --backbone ResNet50 --fc_output_dim 2048 --resume_model ./logs/official/ResNet50_2048_eigenplaces.pth --groups_num 1 --fc_output_dim 512 --brightness=0 --contrast=0 --hue=0 --saturation=0 --use_kd
        ```
    * Training DVG on pitts30k_N:
        ```shell
        python train.py
        ```

5. Eval NPR on the Tokyo247 and AachenDN datasets

    ```
    python eval.py --dataset_folder ../../datasets/tokyo247/images/ --backbone ResNet50 --fc_output_dim 512 --resume_model ./logs/official/resnet50_512.pth 
    python eval.py --dataset_folder ../../datasets/sf_xl/small/ --backbone ResNet50 --fc_output_dim 512 --resume_model ./logs/official/resnet50_512.pth 
    ```

## Issues

If you have any questions regarding our code or datasets, feel free to open an issue or send an e-mail to liubx@pcl.ac.cn or binuxliu@gmail.com

## Cite

```
@article{liu2024npr,
  title={NPR: Nocturnal Place Recognition Using Nighttime Translation in Large-Scale Training Procedures},
  author={Liu, Bingxi and Fu, Yujie and Lu, Feng and Cui, Jinqiang and Wu, Yihong and Zhang, Hong},
  journal={IEEE Journal of Selected Topics in Signal Processing},
  year={2024},
  publisher={IEEE}
}
```



