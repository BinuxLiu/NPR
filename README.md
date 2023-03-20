# NPR: Nocturnal Place Recognition in Street

This is the official implementation of the ICCV 2023 paper "NPR: Nocturnal Place Recognition in Street".

```shell
git clone https://github.com/BinuxLiu/npr.git
```

## Reproduce our results

1. Generate NightStreet and VPR datasets
    * First, run the following command:
        ```shell
        # Initialize the folders of datasets
        python format_datasets.py --datasets_folder /path/to/datasets
        ```
    * Then, you need to download AachenDN (v1, v1.1), Tokyo247 (v2, v3, and database), Pittsburgh, SF-XL-small dataset to the 'datasets/raw' folder.
      The download links of above datasets are written in the comments of `format_datasets.py`.
      In datasets/raw/pittsburgh there should be the following folders: 000, 001, 002, 003, 004, 005, 006, queries_real, index. (index is a folder that contains files such as pitts30k_train.mat).
      Except for the Pittsburgh and Tokyo 247 dataset, none of the other datasets require you to manually decompress them.
    * Run the following command:
        ```shell
        python format_datasets.py --datasets_folder /path/to/datasets/ --datasets aachen_tokyo_pitts_sfxl
        ```
    * If you are using our pre-generated NightStreet dataset, you can skip the above step. You can download the NightStreet dataset directly from here and merge it with the `./datasets/nightstreet` folder after extracting it.

2. Train NEG-CUT on NightStreet dataset
    * To train NEG-CUT on the NightStreet dataset, run the following command in the terminal:
        ```shell
        # terminal_1
        python -m visdom.server
        ```
        ```shell
        # terminal_2
        cd ./third_party/NEGCUT
        python train.py --dataroot ../../datasets/nightstreet --checkpoints_dir ../../checkpoints --name nightstreet --NEGCUT_mode negcut --model negcut --load_size 512 --crop_size 512 --preprocess scale_shortside_and_crop
        ```
    * If you are using our pre-trained NEG-CUT model, you can skip this step.

3. Generate VPR-Night datasets by processing VPR datasets
    * To generate the VPR-Night dataset by processing the VPR dataset, run the following command in the terminal:

        ```shell
        python test.py --dataroot ../../datasets/nightstreet --name nightstreet --NEGCUT_mode negcut --model negcut
        ```
    * If you are using our pre-generated VPR-Night dataset, you can skip this step.

4. Train or fine-tuning VPR methods on VPR-Night datasets
    * Training CosPlace on sf_xl_small_N:
        ```shell
        python train.py
        ```
    * Training DVG on pitts30k_N:
        ```shell
        python train.py
        ```

5. Eval NPR on the Tokyo247 and AachenDN datasets

## Issues

If you have any questions regarding our code or datasets, feel free to open an issue or send an e-mail to binuxliu@gmail.com

## Cite




