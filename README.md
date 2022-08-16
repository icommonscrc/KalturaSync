# KalturaSync

`kaltura.py` is designed to run (semi)continuously whereas `upload.py` is dessigned for one-off file uploads.

`template.xml` is a template that is automatically copied and has metadata required by Kaltura inserted.

Before using either script, be sure to add the appropriate information to the following variables:
- `HOST` - SFTP host address (drop folder)
- `USERNAME` - SFTP username
- `PASSWORD` - SFTP password
- `PATH` - path to OBS save location for recordings (e.g. `C:\Users\...` or `/home/<user name>/...`)
- `USER_ID` - Drexel abc123 of the user that will have access to the uploaded file in Kaltura
