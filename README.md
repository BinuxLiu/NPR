# NPR: Nocturnal Place Recognition in Street

This is the official implementation of the ICCV 2023 paper "NPR: Nocturnal Place Recognition in Street".

## Reproduce our results
1. Generating NightStreet dataset:
* First, you need to download AachenDN and Tokyo247 datasets to the `./datasets/raw` folder and unzip them.
* Then, run the following command:
```shell
python format_datasets.py
```
* If you are using our pre-generated NightStreet dataset, you can skip the above step. You can download the NightStreet dataset directly from here and merge it with the `./datasets/nightstreet` folder after extracting it.