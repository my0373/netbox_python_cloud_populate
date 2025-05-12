import pynetbox
import os, sys
import yaml
import csv


def connect_netbox(hostname, token):
    """
    Connect to the NetBox API.
    """

    nb = pynetbox.api(hostname, token=token)
    nb.status()
    print("Connected successfully to NetBox.")
    return nb
    
def get_region(nb, region_name):
    """
    Get a region by name.
    """
    
    return nb.dcim.regions.get(name=region_name)
        

def load_config(config_file):
    """
    Load the configuration file.
    """
    with open(config_file, 'r') as file:
        reader = csv.reader(file)

        config = tuple(tuple(row) for row in reader)
        return config



    return config

def create_region(nb, region_name, parent=None):
    """
    Create a region in NetBox.
    """
    try:
        region = nb.dcim.regions.create(
            name=region_name,
            slug=region_name.lower().replace(" ", "-"),
            description=f"This is the {region_name} region",
            parent=parent,
            status=1,
        )
        print(f"Created region: {region.name}")
    except pynetbox.RequestError as e:
        print(f"Error creating region {region_name}: {e}")
        
def create_regions(nb, config):
    """
    Create regions in NetBox recursively.
    """
    # for line in config:
    #     print(config)

    for parent, region in config:
        if parent:
            # Why is this not getting the parent ID
            parent_id = nb.dcim.regions.get(name=parent).id

            print(f"Creating region {region} with parent {parent}: {parent_id}")

        else:
            print(f"Creating region {region}")
            parent_id = None

        # Create the parent
        create_region(nb,region, parent=parent_id)


    # for region, parent in config:
    #     if parent:
    #         parent = nb.dcim.regions.get(name=parent)
    #     else: parent = None
    #
    #     print(f"region: {region} Parent region: {parent}")


if __name__ == "__main__":

    # Get the NetBox API token and hostname from environment variables
    api_token = os.getenv('NB_TOKEN')
    api_hostname = os.getenv('NB_HOSTNAME')
    api_url = f"https://{api_hostname}"
    
    # Display the API token and hostname
    print(f"API Token: {api_token}")
    print(f"API Hostname: {api_hostname}")
    print(f"API URL: {api_url}") 
    
    
    # Load the configuration file
    config_file = 'regions.csv'
    regions_dict = load_config(config_file)
    print(f"Using configuration file: {config_file}") 

    
    

    # Connect to NetBox
    nb = connect_netbox(api_url, api_token)

    # print("#" * 50)
    # print(regions_dict)
    # print("#" * 50)
    
    get_region = nb.dcim.regions.get(name="UK")
    
    #print(get_region.id)
    create_regions(nb, regions_dict) 