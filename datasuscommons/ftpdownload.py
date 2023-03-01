import os
import ftplib
from ftplib import FTP
from pathlib import Path

def ftp_download_file(ftp_connection, source_file, target_dir):
    #ftp_reply = ftp_connection.retrlines(f'NLST {source_file}')
    #ftp_reply = ftp_connection.retrlines(f'NLST {source_file}')
    ftp_reply = ftp_connection.retrlines(f'LIST {source_file}')
    print(f"FTP List {ftp_reply}")
    target_file_path = os.path.join(target_dir, source_file)

    print(f"Downloading at: {target_file_path}")
    #os.listdir(f"listing: {target_dir}")
    with open(target_file_path, 'wb') as file_output:
        ftp_reply = ftp_connection.retrbinary(f"RETR {source_file}", file_output.write)
        print(f"Downloaded: {ftp_reply}")
    return os.path.exists(target_file_path)
 


def ftp_download_files(ftp_connection, ftp_base_path, files, key_target_path = None, login = None) -> tuple:
    try:
        ftp_reply2 = ftp_connection.cwd(ftp_base_path)
        #print(f"FTP Connection state: {ftp_reply2}")
        key_target_path = key_target_path if key_target_path else ftp_base_path.replace('/','')[:28]
        target_dir = os.path.join(Path.home(), key_target_path)
        Path(target_dir).mkdir(parents=True, exist_ok=True)
        ok_processed_files = []
        failed_processed_files = []
        for source_file in files:
            try:
                ftp_download_file(ftp_connection, source_file, target_dir)
                ok_processed_files.append(source_file)
            except Exception  as e:
                print(repr(e))
                ftp_download_file(ftp_connection, source_file, target_dir)
        os.chdir(target_dir)
        print(os.getcwd())
        return (ok_processed_files, failed_processed_files)      
    except Exception  as ex:
        print(repr(ex))
        if 'ok_processed_files' in locals() and 'failed_processed_files' in locals():
            return (ok_processed_files, failed_processed_files)
        else:
            None
 

def ftp_connect_download_files(ftp_host, ftp_base_path, files, key_target_path = None, login = None):
    try:
        ftp = FTP(ftp_host)
        ftp_reply1 = ftp.login()
        return ftp_download_files(ftp, ftp_base_path, files, key_target_path, login)
    except Exception  as ex:
        print(repr(ex))
        return None  
    finally:
        if 'ftp' in locals():
            ftp.close()


