# NPR: Nocturnal Place Recognition in Street

This is the official implementation of the ICCV 2023 paper "NPR: Nocturnal Place Recognition in Street".

## Reproduce our results

1. Generate NightStreet dataset
    * First, you need to download AachenDN and Tokyo247 datasets to the `./datasets/raw` folder and unzip them.
    * Then, run the following command:
        ```shell
        python format_datasets.py
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
        cd ./third_party/negcut
        python train.py --dataroot ../../datasets/nightstreet --checkpoints_dir ../../checkpoints --name nightstreet --NEGCUT_mode negcut --model negcut --load_size 512 --crop_size 512 --preprocess scale_shortside_and_crop
        ```
    * If you are using our pre-trained NEG-CUT model, you can skip this step.

3. Generate VPR-Night dataset by processing VPR dataset
    * To generate the VPR-Night dataset by processing the VPR dataset, run the following command in the terminal:

        ```shell
        python test.py --dataroot ../../datasets/nightstreet --name nightstreet --NEGCUT_mode negcut --model negcut
        ```
    * If you are using our pre-generated VPR-Night dataset, you can skip this step.
