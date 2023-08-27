# Carla Torch Dataset
This repo provides tools for creating a dataset from the [Carla](https://carla.org/) autonomous driving simulator. It provides a docker compose file for running both a carla server and a jupyter server for connecting the carla client. It also provides a data collector interface and torch dataset. 

## Usage
A jupyter notebook for [data capture](https://github.com/OLeather/carla-torch-dataset/blob/master/examples/example_capture.ipynb) and [data loading](https://github.com/OLeather/carla-torch-dataset/blob/master/examples/example_load_torch.ipynb) in PyTorch are provided.

The docker containers will run the carla server and client for interfacing with the carla simulator. Simply run `docker compose build && docker compose up` to run the containers. The client container will expose a port (specified in the `docker-compose.yaml` file, `8888` by default) to connect to the jupyer server using `http://localhost:8888`. 

### Data Capture
```python
from carla_data_collector import CarlaDataCollector

# hostname is the hostname of the carla server, either localhost or the name of the docker container
# data_dir is the directory to store the data
data = CarlaDataCollector(hostname='carla_server', data_dir='/data')

data.add_ego_vehicle()

# sensor data will be output to /data_dir/label
data.add_rgb_camera(label='rgb')
data.add_depth_camera(label='depth')

data.set_ego_autopilot(True)

# will capture num_ticks datapoints from carla
data.start(num_ticks=1000)
data.stop()
```

### Data Load
```python
from carla_dataset import CarlaDataset

dataset = CarlaDataset('/data', transform=ToTensor())

imgs = next(iter(dataset))

rgb = imgs['rgb']
depth = imgs['depth']
```
