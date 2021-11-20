import argparse
import tempfile
from diagram_generator import generate_diagram, send_image_to_drive
from brocolib_utils.settings import get_project_settings


# Create the parser
my_parser = argparse.ArgumentParser(description='Generate diagrams for a DWH spec')

# Add the arguments
my_parser.add_argument('sheet_url',
                       metavar='sheet_url',
                       type=str,
                       help='Google Sheets URl'
                       )


# Execute the parse_args() method
args = my_parser.parse_args()

sheet_url = args.sheet_url
dirpath = tempfile.mkdtemp()
project_settings_dict = get_project_settings(sheet_url)
_, file_path = generate_diagram(
    sheet_url=sheet_url,
    directory=dirpath
)
send_image_to_drive(
    project_drive_folder_id=project_settings_dict["project_folder_id"],
    file_path=file_path
)

print('Image saved in Google Drive')



