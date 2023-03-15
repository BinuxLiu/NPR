import argparse

def parse_arguments():
    parser = argparse.ArgumentParser(description="Nocturnal Place Recognition",
                                formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    # Initialization parameters
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--datasets_folder", type=str, default="./datasets")
    
    args = parser.parse_args()
    
    return args