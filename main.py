import boto3
from datetime import *
from threading import Thread

instances = {}

class GetInstancesThread(Thread):
    '''A Thread class to get instances from all regions at the same time to improve speed'''

    def __init__(self, region, tag):
        '''Constructor takes a region to identify the region and a tag to identify the instances to select.'''
        Thread.__init__(self)
        self.region = region
        self.tag = tag

    def run(self):
        '''called from the external program implicitly and gets instances from the selected region'''
        region = self.region
        tag = self.tag
        ec2client = boto3.client("ec2", region)
        response = ec2client.describe_instances()
        reservations = response['Reservations']
        instances[region] = []
        if reservations:
            if tag == None:
                for eachreservation in reservations:
                    try:
                        instances[region].append({
                            'InstanceId': eachreservation['Instances'][0]['InstanceId'],
                            'AZ': eachreservation['Instances'][0]['Placement']['AvailabilityZone'],
                            'PublicIP': eachreservation['Instances'][0]['PublicIpAddress'],
                            'State': eachreservation['Instances'][0]['State']['Name'],
                            'InstanceType': eachreservation['Instances'][0]['InstanceType'],
                            'LaunchTime': eachreservation['Instances'][0]['LaunchTime'],
                            'WithinFreeTier': checkfreetiereligible(
                                eachreservation['Instances'][0]['LaunchTime'].replace(tzinfo=None),
                                eachreservation['Instances'][0]['InstanceType'])
                        })
                    except:
                        instances[region].append({
                            'InstanceId': eachreservation['Instances'][0]['InstanceId'],
                            'AZ': eachreservation['Instances'][0]['Placement']['AvailabilityZone'],
                            'State': eachreservation['Instances'][0]['State']['Name'],
                            'InstanceType': eachreservation['Instances'][0]['InstanceType'],
                            'LaunchTime': eachreservation['Instances'][0]['LaunchTime'],
                            'WithinFreeTier': checkfreetiereligible(
                                eachreservation['Instances'][0]['LaunchTime'].replace(tzinfo=None),
                                eachreservation['Instances'][0]['InstanceType'])
                        })
            else:
                for eachreservation in reservations:
                    try:
                        instancetaglist = eachreservation['Instances'][0]['Tags']
                    except:
                        instancetaglist = None

                    if instancetaglist:
                        for eachinstancetag in instancetaglist:
                            if eachinstancetag['Key'] == tag['Key'] and eachinstancetag['Value'] == tag['Value']:
                                try:
                                    instances[region].append({
                                        'InstanceId': eachreservation['Instances'][0]['InstanceId'],
                                        'AZ': eachreservation['Instances'][0]['Placement']['AvailabilityZone'],
                                        'PublicIP': eachreservation['Instances'][0]['PublicIpAddress'],
                                        'State': eachreservation['Instances'][0]['State']['Name'],
                                        'InstanceType': eachreservation['Instances'][0]['InstanceType'],
                                        'LaunchTime': eachreservation['Instances'][0]['LaunchTime'],
                                        'WithinFreeTier': checkfreetiereligible(
                                            eachreservation['Instances'][0]['LaunchTime'].replace(tzinfo=None),
                                            eachreservation['Instances'][0]['InstanceType'])
                                    })
                                except:
                                    instances[region].append({
                                        'InstanceId': eachreservation['Instances'][0]['InstanceId'],
                                        'AZ': eachreservation['Instances'][0]['Placement']['AvailabilityZone'],
                                        'State': eachreservation['Instances'][0]['State']['Name'],
                                        'InstanceType': eachreservation['Instances'][0]['InstanceType'],
                                        'LaunchTime': eachreservation['Instances'][0]['LaunchTime'],
                                        'WithinFreeTier': checkfreetiereligible(
                                            eachreservation['Instances'][0]['LaunchTime'].replace(tzinfo=None),
                                            eachreservation['Instances'][0]['InstanceType'])
                                    })


def checkfreetiereligible(instancestarttime, instancetype):
    '''Checks whether free tier is eligible or not'''
    timediff = datetime.utcnow() - instancestarttime
    freetiertimeinsec = 750 * 60 * 60
    timediffinsec = timediff.total_seconds()

    if instancetype == 't2.micro' and timediffinsec <= freetiertimeinsec:
        return True
    else:
        return False

def askchoice():
    '''Asks for user's input and whether instances of a specific tag should be displayed'''
    while True:
        choice = raw_input("Would you like to list instances selectively using tags? (Enter 'Y'|'N'): ")

        if choice.lower() == 'y':
            key = raw_input("Enter Tag key: ")
            value = raw_input("Enter Tag value: ")
            return {'Key' : key, 'Value' : value}
        elif choice.lower() == 'n':
            return None
        else:
            print "Invalid choice, try again"

def getinstancesinallregions(tag):
    '''Get instances in all regions and passes the specified tag and region when creating an object of GetInstancesThread'''

    ec2client = boto3.client("ec2")

    response = ec2client.describe_regions()

    regions = []
    for eachresponse in response['Regions']:
        regions.append(eachresponse['RegionName'])

    threads = []

    for eachregion in regions:
        currentthread = GetInstancesThread(region=eachregion,tag=tag)
        currentthread.start()
        threads.append(currentthread)

    for eachthread in threads:
        eachthread.join()

    return instances

def displaydata(data):
    '''Displays information in a readable form'''
    for eachregion in data:
        print eachregion
        for eachinstance in data[eachregion]:
            print eachinstance
        print '--------------------------------------'


#main program

#Ask user for tags
tag = askchoice()

#use tag to get instances in all regions
instancesinallregions = getinstancesinallregions(tag)

#display result to user
displaydata(instancesinallregions)