import os

def delete_file_with_name(folder_path, file_name):
    for root, dirs, files in os.walk(folder_path):
        for file_name in file_names:
            if file_name in files:
                os.remove(os.path.join(root, file_name))
                print(f"Deleted file: {os.path.join(root, file_name)}")

folder_path = "G:/Dataset/jqq/underwater/stuff_darkdark/images"
file_names = ['DSC04361raw1.JPG', 'DSC04380raw1.JPG', 'DSC04396raw1.JPG', 'DSC04408raw1.JPG', 'DSC04414raw1.JPG']
delete_file_with_name(folder_path, file_names)