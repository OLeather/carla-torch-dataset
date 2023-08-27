import carla
import random
import os
 
class CarlaDataCollector():
    def __init__(self, hostname='localhost', data_dir='./data/'):
        client = carla.Client(hostname, 2000)
        self.world = client.get_world()
        
        # Set world to synchronus mode so sensor measurements are aligned in time
        settings = self.world.get_settings()
        settings.synchronous_mode = True
        settings.fixed_delta_seconds = 0.05
        self.world.apply_settings(settings)
        self.data_dir = data_dir

        self.spawn_points = self.world.get_map().get_spawn_points()
        self.vehicle_blueprints = self.world.get_blueprint_library().filter('*vehicle*')

        self.cameras = {}

    def add_ego_vehicle(self, vehicle_name='vehicle.tesla.model3', spawn_point = None):
        if spawn_point is None:
            spawn_point = random.choice(self.spawn_points)
        ego_bp = self.vehicle_blueprints.find(vehicle_name)
        ego_bp.set_attribute('role_name', 'hero')
        self.ego_vehicle = self.world.spawn_actor(ego_bp, spawn_point)
    
    def set_ego_autopilot(self, autopilot):
        self.ego_vehicle.set_autopilot(autopilot)

    def add_rgb_camera(self, transform=carla.Transform(carla.Location(x=1.5, z=1.5)), width=256, height=144, fov=60, sensor_tick=0.05, label=None, attach_to=None):
        self.add_camera(type='rgb', transform=transform, width=width, height=height, fov=fov, sensor_tick=sensor_tick, label=label, attach_to=attach_to)
        
    def add_depth_camera(self, transform=carla.Transform(carla.Location(x=1.5, z=1.5)), width=256, height=144, fov=60, sensor_tick=0.05, label=None, attach_to=None):
        self.add_camera(type='depth', transform=transform, width=width, height=height, fov=fov, sensor_tick=sensor_tick, label=label, attach_to=attach_to)

    def add_camera(self, type='rgb', transform=carla.Transform(carla.Location(x=1.5, z=1.5)), width=256, height=144, fov=60, sensor_tick=0.05, label=None, attach_to=None):
        if attach_to is None:
            attach_to = self.ego_vehicle
        if label is None:
            label = 'camera{0}'.format(len(self.cameras))
        camera_bp = self.world.get_blueprint_library().find('sensor.camera.{0}'.format(type))
        camera_bp.set_attribute('image_size_x', str(width))
        camera_bp.set_attribute('image_size_y', str(height))
        camera_bp.set_attribute('fov', str(fov))
        camera_bp.set_attribute('sensor_tick', str(sensor_tick))
        camera = self.world.spawn_actor(camera_bp, transform, attach_to=attach_to)
        self.cameras[label] = camera

    def _save_image(self, image, label):
        path = os.path.join(self.data_dir, label, '%06d.png' % image.frame)
        image.save_to_disk(path)

    def start(self, num_ticks = float('inf')):
        for label in self.cameras:
            camera = self.cameras[label]
            camera.listen(lambda image, label=label: self._save_image(image, label))
        
        for i in range(num_ticks):
            self.world.tick()

        self.stop()

    def stop(self):
        for label in self.cameras:
            camera = self.cameras[label]
            camera.stop()
