from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
# gauth = GoogleAuth()
# gauth.LocalWebserverAuth()


class DataManager:

    PRES_SVG = "Presentation SVG"
    PRES_DOWN = "Presentation Downloaded"
    PRES_SVG_ID = '1qXOo6WpAurjFkS13-g15u1APi_LfYhOF'
    PRES_DOWN_ID = '1jOIhkeRurmjmxhCBDx4iSujbaGA17Ugf'
    NOTES_ID = '1yMeitTiDVmz-23PbGRNg4x5HhUNVRUO_'
    NOTES = "Notes"


    def __init__(self):
        self.gauth = GoogleAuth()
        self.gdrive_init()

    def gdrive_init(self):
        self.gauth.LoadCredentialsFile("creds.txt")
        if self.gauth.credentials is None:
            # Authenticate if they're not there
            self.gauth.LocalWebserverAuth()
        elif self.gauth.access_token_expired:
            # Refresh them if expired
            self.gauth.Refresh()
        else:
            # Initialize the saved creds
            self.gauth.Authorize()
        # Save the current credentials to a file
        self.gauth.SaveCredentialsFile("creds.txt")
        self.drive = GoogleDrive(self.gauth)

    def get_folder_id(self, folderName, extended_parent=None):
        q = "title='" + folderName + "' and mimeType='application/vnd.google-apps.folder' and trashed=false"
        if extended_parent:
            q += " and '{}' in parents".format(extended_parent)
        folders = self.drive.ListFile({'q': q}).GetList()
        for folder in folders:
            if folder['title'] == folderName: return folder['id']

    def create_folder(self, parentFolderName, folderName, extended_parent=None):
        q = "title='" + parentFolderName + "' and mimeType='application/vnd.google-apps.folder' and trashed=false"
        if extended_parent:
            q += " and '{}' in parents".format(extended_parent)
        folders =  self.drive.ListFile({'q': q}).GetList()
        for folder in folders:
            if folder['title'] == parentFolderName:
                metadata = {'parents': [{'id': folder['id']}], 'title' : folderName, 'mimeType' : 'application/vnd.google-apps.folder'}
                file = self.drive.CreateFile(metadata)
                file.Upload()
                return file['id']

        raise Exception("No such a folder")

    def create_folder_by_id(self, parentFolderID, folderName):
        try:
            q_chck = "title='{}' and mimeType='application/vnd.google-apps.folder' and trashed=false and '{}' in parents".format(folderName, parentFolderID)
            folders = self.drive.ListFile({'q': q_chck}).GetList()
            print("check qry done")
            if len(folders) >= 1:
                print("repeated_folder")
                return folders[0]['id']
        except Exception as e:
            pass
        try:
            metadata = {'parents': [{'id': parentFolderID}], 'title': folderName,
                        'mimeType': 'application/vnd.google-apps.folder'}
            file = self.drive.CreateFile(metadata)
            file.Upload()
            return file['id']
        except Exception as e:
            raise Exception("No folder with id found") from e

    def create_folders(self, parentFolderName, path, ext_id=None):
        paths = path.split("\\")
        if len(paths) > 1:
            base_folder = paths[0]
            self.create_folder(parentFolderName, base_folder, ext_id)
            self.create_folders(base_folder, '\\'.join(paths[1:]))
        else:
            self.create_folder(parentFolderName, paths[0])

    def create_folders_by_id(self, parentFolderID, path):
        paths = path.split("\\")
        if len(paths) > 1:
            base_folder = paths[0]
            id = self.create_folder_by_id(parentFolderID, base_folder)
            print()
            return self.create_folders_by_id(id, '\\'.join(paths[1:]))
        else:
            return self.create_folder_by_id(parentFolderID, paths[0])

    def upload_to_folder(self, folderName,  filepath, extended_parent=None):
        q = "title='" + folderName + "' and mimeType='application/vnd.google-apps.folder' and trashed=false"
        if extended_parent:
            q += " and '{}' in parents".format(extended_parent)
        folders =  self.drive.ListFile({'q': q}).GetList()
        for folder in folders:
            if folder['title'] == folderName:
                file2 = self.drive.CreateFile({'parents': [{'id': folder['id']}]})
                file2.SetContentFile(filepath)
                file2.Upload()
                break

    def upload_to_folder_by_id(self, folderID,  filepath, ):
        print("folderID being upload:", folderID, "filepath:", filepath, "name:", filepath.split("\\")[-1])
        file2 = self.drive.CreateFile({'parents': [{'id': folderID}], 'title':filepath.split("\\")[-1]})
        file2.SetContentFile(filepath)
        file2.Upload()


    def upload_by_id(self, parentFolderID, path):
        path = path.replace("/","\\")
        last_folder_id = self.create_folders_by_id(parentFolderID, '\\'.join(path.split("\\")[1:-1]))
        self.upload_to_folder_by_id(last_folder_id, path)

    def upload(self, folderName, file):
        fid = self.get_folder_id(folderName)
        self.upload_by_id(fid, file)

    def upload_svg(self, file):
        self.upload_by_id(self.PRES_SVG_ID, file)

    def upload_down(self, file):
        self.upload_by_id(self.PRES_DOWN_ID, file)

    def upload_notes(self, file):
        self.upload_by_id(self.NOTES_ID, file)
# upload_to_folder("Presentation SVG", "trial1.txt")
