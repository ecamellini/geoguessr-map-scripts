import os
import glob
import exifread
import json
import sys

def dms_to_decimal(dms, ref):
    """
    Convert DMS (Degrees, Minutes, Seconds) to decimal degrees.
    dms is a list of exifread Ratio objects, e.g. [34, 12, 30/1].
    ref is a character 'N', 'S', 'E', or 'W'.
    """
    # Each dms element may be of type exifread.utils.Ratio or int.
    # For safety, convert them to float explicitly.
    degrees = float(dms[0].num) / float(dms[0].den)
    minutes = float(dms[1].num) / float(dms[1].den)
    seconds = float(dms[2].num) / float(dms[2].den)

    decimal = degrees + minutes / 60.0 + seconds / 3600.0
    if ref in ['S', 'W']:
        decimal = -decimal
    return decimal

def get_gps_data_from_exif(img_path):
    """
    Read EXIF data from an image and extract GPS latitude/longitude if present.
    Returns (lat, lng) in decimal degrees if found, otherwise None.
    """
    with open(img_path, 'rb') as f:
        tags = exifread.process_file(f, details=False)

    # exifread typically stores the GPS data under keys like 'GPS GPSLatitude',
    # 'GPS GPSLatitudeRef', 'GPS GPSLongitude', 'GPS GPSLongitudeRef'.
    gps_lat = tags.get('GPS GPSLatitude')
    gps_lat_ref = tags.get('GPS GPSLatitudeRef')
    gps_lng = tags.get('GPS GPSLongitude')
    gps_lng_ref = tags.get('GPS GPSLongitudeRef')

    if gps_lat and gps_lat_ref and gps_lng and gps_lng_ref:
        lat = dms_to_decimal(gps_lat.values, gps_lat_ref.values)
        lng = dms_to_decimal(gps_lng.values, gps_lng_ref.values)
        return lat, lng

    return None

def images_to_json(folder_path):
    """
    Reads all JPG images in the folder, extracts GPS coordinates from each,
    and returns a JSON array (Python list) of objects with the specified format.
    """
    # Customize these fixed fields as needed
    default_heading = 0
    default_pitch = 0
    default_zoom = 1
    default_pano_id = None
    default_country_code = None
    default_state_code = None

    results = []

    # Change the pattern if you want to include other image extensions
    image_files = glob.glob(os.path.join(folder_path, "*.jpg"))

    for img_path in image_files:
        gps_coords = get_gps_data_from_exif(img_path)
        if gps_coords is not None:
            lat, lng = gps_coords
            entry = {
                "heading": default_heading,
                "pitch": default_pitch,
                "zoom": default_zoom,
                "panoId": default_pano_id,
                "countryCode": default_country_code,
                "stateCode": default_state_code,
                "lat": lat,
                "lng": lng
            }
            results.append(entry)
        else:
            # If no GPS data is present, you can decide to skip
            # or create an entry with null coordinates, etc.
            pass

    return results

if __name__ == "__main__":
    # Getting pictures folder path from command line arguments
    folder_path = sys.argv[1]
    json_data = images_to_json(folder_path)
    # Print the JSON array to stdout
    print(json.dumps(json_data, indent=2))
