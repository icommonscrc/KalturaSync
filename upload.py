# Created by Kyle Goetke

import pysftp
import shutil
import os
import sys


def files_in_directory(PATH):
    onlyfiles = [f for f in os.listdir(PATH) if os.path.isfile(os.path.join(PATH, f))]
    return(onlyfiles)


def main():
    # define constant variables
    HOST = ""  # sftp host
    USERNAME = ""  # sftp username
    PASSWORD = ""  # sftp password
    PATH = ""  # path to OBS save location for recordings
    CNOPTS = pysftp.CnOpts()
    CNOPTS.hostkeys = None
    USER_ID = ""  # add your abc123

    file_list = files_in_directory(PATH)
    for file in file_list:
        print(f"[{file_list.index(file)}] {file}")

    choice = int(input("\nWhich file would you like to upload?\n# "))
    if str(choice) == "-1":
        exit
    filename = file_list[choice]
    name = filename
    description = filename[:-4]  # full filename minus the file extension
    new_xml_file = "XML/" + description + ".xml"
    shutil.copyfile("XML/template.xml", new_xml_file)
    print("\n> XML TEMPLATE COPIED")

    with open(new_xml_file, "r") as file:
        data = file.readlines()
    data[6] = f"      <userId>{USER_ID}</userId>\n"
    data[7] = f"      <name>{name}</name>\n"
    data[8] = f"      <description>{description}</description>\n"
    data[19] = f'          <dropFolderFileContentResource filePath="{filename}">\n'
    with open(new_xml_file, "w") as file:
        file.writelines(data)
    print("> XML UPDATED")

    with pysftp.Connection(HOST, username=USERNAME, password=PASSWORD, cnopts=CNOPTS) as SFTP:
        print("\nSFTP:", SFTP.listdir())
        SFTP.put(f"{PATH}{filename}")
        SFTP.put(new_xml_file)
        print("SFTP:", SFTP.listdir())
        print("> FILES PUSHED")

    print("\nALL FILES PROCESSED")


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
