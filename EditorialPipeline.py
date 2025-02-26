import re

edl_file_path = "D:/HecberryStuff/PAINANI STUDIOS/1_Proyectos/Active/1_Animaorquesta/PipeTest/EDL_Test_v002.edl"
fps = 24

#def export_edl(edl_file):
    # Export an edl and send the information into Kitsu or a json file so it can be accessed.
    # Recollect the metadata from shots and store it in variables that will be added into Kitsu.
#    """Cut video using FFmpeg based on an EDL file."""

#def export_shots():
    # Export each shot separately and publish it into kitsu, this should version up.

#def export_cut():
    # Export a full cut and publish it into kitsu, this should version up and publish a new version of the full cut.

#def get_shots_info():
    #Get the shots info from the edl or kitsu as a result of the export_edl function

def timecode_to_seconds(timecode, fps=24):
    hh, mm, ss, ff = map(int, timecode.split(":"))
    total_seconds = hh * 3600 + mm * 60 + ss + (ff / fps)
    return total_seconds



def get_shots_from_edl(edl_file, fps=24):
    regex_pattern = r"(\d{2}:\d{2}:\d{2}:\d{2})\s(\d{2}:\d{2}:\d{2}:\d{2})\s(\d{2}:\d{2}:\d{2}:\d{2})\s(\d{2}:\d{2}:\d{2}:\d{2})"
    shots = {}
    with open(edl_file, "r") as file:

        for line in file:
            match = re.search(r"(\d{3})\s", line)
            if match:
                shot_number = match.group(1)

            timecodes = re.findall(regex_pattern, line)

            if timecodes:
                for timeSource in timecodes:
                    #print(timeSource)
                    source_in = timecode_to_seconds(timeSource[0], fps)
                    source_out = timecode_to_seconds(timeSource[1], fps)
                    record_in = timecode_to_seconds(timeSource[2], fps)
                    record_out = timecode_to_seconds(timeSource[3], fps)
                    #print(f"This is the cut in : {source_in}, this is the cut out {source_out}")


                    shots[shot_number] = {
                        "source_in": source_in,
                        "source_out": source_out,
                        "record_in": record_in,
                        "record_out": record_out
                    }
    #print(shots)
    return shots



shots = get_shots_from_edl(edl_file_path)

for shot, data in shots.items():
    print(f"Shot {shot}:")
    print(f"  Source In: {data['source_in']} sec")

