import os
import json

def get_gpu_type(filename):
    lower_filename = filename.lower()
    if 'menu.' in lower_filename or 'player.' in lower_filename or 'playerhi.' in lower_filename:
        return 'all'
    if '.dxt.' in lower_filename:
        return 'dxt'
    elif '.etc.' in lower_filename:
        return 'etc'
    elif '.pvr.' in lower_filename:
        return 'pvr'
    elif '.unc.' in lower_filename:
        return 'unc'
    else:
        return 'all'

def generate_json(mode, output_filename, folder_path, base_url):
    files_list = []

    for root, dirs, files in os.walk(folder_path):
        if mode == 'all_except_samp':
            dirs[:] = [d for d in dirs if d.lower() != 'samp']
        elif mode == 'only_samp':
            if root == folder_path:
                dirs[:] = [d for d in dirs if d.lower() in ['samp', 'texdb']]
            elif os.path.basename(root).lower() == 'texdb':
                dirs[:] = [d for d in dirs if d.lower() == 'samp']
        for file in files:
            file_path = os.path.join(root, file)
            relative_path = os.path.relpath(file_path, folder_path)
            normalized_path = relative_path.replace('\\', '/').replace('//', '/')

            if mode == 'only_samp':
                if not (normalized_path.startswith(('SAMP/', 'samp/', 'texdb/samp')) or 
                        normalized_path in ['texdb/samp.img', 'texdb/SAMPCOL.img']):
                    continue
            elif mode == 'all_except_samp':
                if normalized_path.startswith(('SAMP/', 'samp/', 'texdb/samp')) or \
                   normalized_path in ['texdb/samp.img', 'texdb/SAMPCOL.img']:
                    continue

            gpu_type = get_gpu_type(file)
            files_list.append({
                "name": file,
                "size": str(os.path.getsize(file_path)),
                "path": normalized_path,
                "url": f"{base_url}{normalized_path}",
                "gpu": gpu_type
            })

    with open(output_filename, 'w') as f:
        json.dump({"files": files_list}, f, indent=4, ensure_ascii=False)
    print(f"Created {output_filename} ({mode} mode)")

# Paths and URLs
lite_folder = 'files'
full_folder = 'files'
lite_url = 'http://14.225.207.220/datamobile/files/'
full_url = 'http://14.225.207.220/datamobile/files/'

# Generate the JSON files
generate_json('all_except_samp', 'lite_list.json', lite_folder, lite_url)
generate_json('only_samp', 'samp_list.json', full_folder, full_url)
generate_json('all_except_samp', 'full_list.json', full_folder, full_url)
generate_json('all_except_samp', 'data-0393828380.json', full_folder, full_url)
