import bpy
import pprint
import csv


#camName = ["Cam1", "Cam2", "Cam3", "Cam4", "Cam5"]
csv_path = r"D:\HecberryStuff\Dev\TestCsv.csv"
collection_name = "Cameras"


#This checks for the existance of a collection named cameras and if not there it creates a new collection, named Cameras 
def create_collection():
    collections = bpy.context.scene.collection.children
    #print(collections)
    for coll in collections:
        if coll.name == collection_name:
            print(f"Collection {collection_name} already exists")
            break
    else:
        new_collection = bpy.data.collections.new(collection_name)
        # Link the collection to the scene
        bpy.context.scene.collection.children.link(new_collection)
        print(f"Collection {collection_name} will be created")
        return new_collection



# This function reads through a CSV file looking for the column ShotName and stores the values in a list called shot_names for later use on camera creation
def parse_csv_file_to_dict(file_path):
    shots_dict = {}
    with open(file_path, 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            shot_name = row["ShotName"]
            start_frame = int(row["StartFrame"])
            end_frame = int(row["EndFrame"])
            shots_dict[shot_name] = {
                "shot_name": shot_name,
                "start_frame": start_frame,
                "end_frame": end_frame
            }
    return shots_dict

# This function sets the timeline start and end frame based on the smallest start frame and highest end frame from the csv.
def set_timeline(shots_dict):
    start_frames = [data["start_frame"] for data in shots_dict.values()]
    end_frames = [data["end_frame"] for data in shots_dict.values()]
    
    min_frame = min(start_frames)
    max_frame = max(end_frames)
    
    bpy.context.scene.frame_start = min_frame
    bpy.context.scene.frame_end = max_frame
    
    print(f"Timeline set from {min_frame} to {max_frame}")
        
        
def create_markers(shots_dict):
    for cam, data in shots_dict.items():
        existing_cam = bpy.context.scene.objects.get(cam)
        existing_marker = bpy.context.scene.timeline_markers.get(cam)
        start_frame = shots_dict[cam]['start_frame']
        if existing_marker:
            if existing_marker.frame==start_frame:
                print(f"Marker {cam} exists on frame {start_frame}")
            else:
                existing_marker.frame = start_frame
                print(f"Marker {cam} updated to {start_frame}")
            #print(f"Marker {cam} already exists")
        else:
            bpy.context.scene.timeline_markers.new(name=cam, frame=data["start_frame"])
            print(f"{cam} marker created succesfully at frame {start_frame}")

#This section the function creates cameras based on a list of names, and skips if the camera already exists in the scene as a camera.
def cam_creation(cameras, collection):
    #print(f"These are the cameras and their info {cameras}")
    for cam, data in cameras.items():
        existing_cam = bpy.context.scene.objects.get(cam)
        existing_marker = bpy.context.scene.timeline_markers.get(cam)
        if existing_cam and existing_cam.type == 'CAMERA':
            if existing_marker:
                existing_marker.camera = existing_cam
            print(f"{cam} is already in scene. Skipping...")
            continue
        else:
            camera_data = bpy.data.cameras.new(name=cam)
            camera_object = bpy.data.objects.new(name=cam, object_data=camera_data)
            if existing_marker:
                existing_marker.camera = camera_object
            collection.objects.link(camera_object)
            print(f"{cam} created succesfully!")
# We need to add a condition if the marker already exists do not create a new one, just update the frame based on the new information



new_collection = create_collection()
Shots = parse_csv_file_to_dict(csv_path)


set_timeline(Shots)
create_markers(Shots)

cam_creation(Shots, new_collection)


print("Current Timeline range: ",bpy.context.scene.frame_start,"-", bpy.context.scene.frame_end)







# If its 1 single scene then markers can be used, if its a scene per camera then timeline can change. 