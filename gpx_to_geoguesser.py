import gpxpy
import json
import sys

def gpx_to_json(gpx_file_path):
    """
    Reads a GPX file and returns a JSON array (list in Python)
    of objects with the specified format.
    """
    with open(gpx_file_path, 'r', encoding='utf-8') as gpx_file:
        gpx = gpxpy.parse(gpx_file)

    # Customize these fixed fields as needed
    default_heading = 0
    default_pitch = 0
    default_zoom = 1
    default_pano_id = None
    default_country_code = None
    default_state_code = None

    results = []
    # Traverse tracks, segments, and points in the GPX
    for track in gpx.tracks:
        for segment in track.segments:
            for point in segment.points:
                entry = {
                    "heading": default_heading,
                    "pitch": default_pitch,
                    "zoom": default_zoom,
                    "panoId": default_pano_id,
                    "countryCode": default_country_code,
                    "stateCode": default_state_code,
                    "lat": point.latitude,
                    "lng": point.longitude
                }
                results.append(entry)

    return results

if __name__ == "__main__":
    # getting GPX file path from command line arguments
    gpx_file_path = sys.argv[1]
    json_data = gpx_to_json(gpx_file_path)
    # Print the JSON array to stdout
    print(json.dumps(json_data, indent=2))
