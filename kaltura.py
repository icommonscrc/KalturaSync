# Created by Kyle Goetke

import pysftp
import shutil
import os
import sys
import time


def files_in_directory(PATH):
    onlyfiles = [f for f in os.listdir(PATH) if os.path.isfile(os.path.join(PATH, f))]
    return onlyfiles


def compare_lists(original_list, new_list):
    list_of_diff = [x for x in new_list if x not in original_list]  # Only detects created/moved files, not deleted files
    return list_of_diff


def main():
    # define constant variables
    HOST = ""  # sftp host
    USERNAME = ""  # sftp username
    PASSWORD = ""  # sftp password
    PATH = ""  # path to OBS save location for recordings
    CNOPTS = pysftp.CnOpts()
    CNOPTS.hostkeys = None
    USER_ID = ""  # add your abc123

    while True:
        prev_file_list = files_in_directory(PATH)
        print("> CURRENT FILES:", prev_file_list, end="\r")
        time.sleep(10)  # 10 seconds
        # time.sleep(86400)  # 24 hours
        new_file_list = files_in_directory(PATH)
        files_diff = compare_lists(prev_file_list, new_file_list)
        prev_file_list = new_file_list
        if len(files_diff) == 0:  # if no new files are detected
            continue
        print("> CURRENT FILES:", new_file_list)

        for filename in files_diff:
            print(f"\n> NEW FILE - {filename}")
            name = filename
            description = filename[:-4]  # full filename, minus the file extension
            new_xml_file = "XML/" + description + ".xml"
            shutil.copyfile("XML/template.xml", new_xml_file)
            print("> XML TEMPLATE COPIED")

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
                print("SFTP:", SFTP.listdir())
                SFTP.put(f"{PATH}{filename}")
                SFTP.put(new_xml_file)
                print("SFTP:", SFTP.listdir())
                print("> FILES PUSHED")

        print("ALL FILES PROCESSED")


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
