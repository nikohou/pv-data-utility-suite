# utils.py



__all__ = ['read_pv_specs']


import yaml

def read_pv_specs():
    with open("pv_system_specs.yml", "r") as stream:
        try:
            parsed_yaml = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print("Could not read yml file.")

    return parsed_yaml
