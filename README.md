# Deep Jupyter Portal

Easy setup and teardown for Jupyter notebooks on GPU enabled AWS spot instance for deep learning. 

Blog post: [link](https://sudhanshupassi.info/deep-learning-for-cheap-jupyter-aws-spot/)

## Installation

Use python 2.7 and install requirements.

```bash
pip install -r requirements.txt
```

## To use the AWS spot instances
```bash
portal open deep_gpu
portal info deep_gpu
portal ssh deep_gpu
portal close deep_gpu
```

## To start the jupyter notebook
```bash
python start_jupyter.py
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)
