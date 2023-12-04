from target.hdfs import HdfsDriver, HdfsTarget

DRIVERS = {}
TARGETS = {
    'HDFS': lambda driver, target: HdfsTarget(driver, target['path'])
}

def init_driver(driver_confs):
    for drive_conf_name, drive_conf in driver_confs:
        if drive_conf_name in DRIVERS:
            raise ValueError("Driver {} already initialized".format(drive_conf_name))
        
        if drive_conf_name == 'HDFS':
            DRIVERS[drive_conf_name] = HdfsDriver(drive_conf['url'])
        else:
            raise ValueError("Driver {} not supported".format(drive_conf_name))

def parse_target(target):
    target_type = target['type']
    if target_type not in TARGETS:
        raise ValueError("Target type {} not supported".format(target_type))
    return TARGETS[target_type](DRIVERS[target_type], target)