
# Saz2Json

[![MIT License](https://img.shields.io/badge/License-MIT-yellow.svg)](https://choosealicense.com/licenses/mit/)
[![Python Version](https://img.shields.io/badge/Python-3.x-blue.svg)](https://www.python.org/downloads/)

The "Saz2Json" project is a specialized Python tool tailored for network research purposes. Its primary objective is to facilitate the conversion of Fiddler SAZ files into the JSON format, optimizing the extraction and analysis of captured network traffic data. Designed with a focus on network research, Saz2Json retains crucial request and response information, enabling researchers, developers, and analysts to delve into in-depth network behavior analysis. By bridging the gap between SAZ and JSON, this lightweight and user-friendly tool empowers network researchers to efficiently explore, dissect, and draw insights from network interactions, ultimately enhancing the efficacy of network research endeavors.

## Features

- Converts SAZ files to a folder contains JSON format files.
- Retains request and response details.
- Lightweight and easy-to-use.

## Usage

```bash
python Saz2Json.py <saz_file_path> <output_folder> [<list of domains>]
```

- <`saz_file_path`> is the path to the .saz file that you wish to convert.
- <`output_folder`> is the name of the target folder that will contain the JSON files (file per session).
- <`list of domains`> _(optional)_ is a white list of domains that you want the script to digest. Make sure that you enters it as one argument - e.g. "['www.google.com', 'www.domain.com']".

## License

This project is licensed under the MIT License - see the [LICENSE](https://choosealicense.com/licenses/mit/) file for details.

## Contributing

Contributions are welcome! If you find any issues or have suggestions for improvements, feel free to open an issue or submit a pull request.

## Authors

- [@RoyElia](https://www.linkedin.com/in/roy-elia/)

