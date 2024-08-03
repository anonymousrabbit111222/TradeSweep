# TradeSweep
TradeSweep is a research project aimed at preprocessing data in an efficient and effective manner.

## Table of Contents
- [Introduction](#introduction)
- [Installation](#installation)
- [Setup Code Library](#setup-code-library)
- [Usage](#usage)
- [Contributing](#contributing)

## Introduction
TradeSweep is a powerful LLM-driven tool that leverages RAG and LLM's code writing abilities to help users optimize their data preprocessing pipelines.

## Installation
To use TradeSweep in local environment::
1. Clone this repository
2. Install the required dependencies: `pip install -r requirements.txt`

## Setup Code Library
To set a code library on Qdrant:
1. If desired, add new functions to the `./code_library.py` file.
2. Run `sudo docker run -p 6333:6333 -p 6334:6334 -v $(pwd)/qdrant_storage:/qdrant/storage qdrant/qdrant:latest` to start the Qdrant server.
2. Run `./generate_embeddings.ipynb` to generate embeddings for the code library.

## Usage
0. Make sure your target data is included in the `./datasets` folder.
1. Run the main script: `python TradeSweep.py`
2. Follow the prompts to input your data.
3. TradeSweep will generate detailed reports and visualizations to help you fulfill your data preprocessing requests.

## Contributing
Contributions are welcome! If you have any ideas or suggestions, please open an issue or submit a pull request.
