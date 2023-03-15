import npr_parser
import format_datasets

if __name__ == "__main__":
    args = npr_parser.parse_arguments()
    
    formater = format_datasets.Format_Datasets(args)
    formater.tokyo247_to_nightstreet()
    formater.aachenDN_to_nightstreet()