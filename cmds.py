import os
import sys
import shutil
import sqlite3
import time

def get_sticky_note_backup_path():
    return os.path.expandvars("%TMP%\\plum.sqlite")

def get_sticky_note_appdata_path():
    sticky_note_dir_cache = os.path.expandvars("%TMP%\\sndir.cache")

    src_path = os.path.expandvars("%USERPROFILE%\\AppData\\Local\\Packages")

    dirname = None
    if os.path.exists(sticky_note_dir_cache):
        with open(sticky_note_dir_cache, mode='r') as fhandle:
            dirname = fhandle.readline()
    else:
        for dire in os.listdir(src_path):
            if "Microsoft.MicrosoftStickyNotes" in dire:
                with open(sticky_note_dir_cache, mode='w') as fhandle:
                    fhandle.write(dire)
                    dirname = dire
                break

    return f"{src_path}\\{dirname}\\LocalState\\plum.sqlite" if dirname is not None else None

def log(err):
    if err == -1:
        print("[Error] Sticky Note (from Microsoft) is not installed!")
    elif err == -2:
        print("[Error] Sticky Note (from Microsoft) data can not be found!")
        print("Please make sure if you have notes in the app.")
    elif err == -3:
        print("[Error] Sticky Note (from Microsoft) backup data can not be found!")
        print("Please make sure if you have backup data at least once.")

def backup(src, dst):
    result = True
    try:
        shutil.copyfile(src, dst)
        shutil.copyfile(src + "-shm", dst + "-shm")
        shutil.copyfile(src + "-wal", dst + "-wal")
    except FileNotFoundError as e:
        result = False
    finally:
        if result:
            with sqlite3.connect(dst) as plum_conn:
                plum_cur = plum_conn.cursor()
                plum_cur.execute("UPDATE Note SET RemoteId = ?, ChangeKey = ?, LastServerVersion = ?, RemoteSchemaVersion = ?, IsRemoteDataInvalid = ?, PendingInsightsScan = ?, Type = ?", (None, None, None, None, None, None, None))
                #plum_cur.execute("UPDATE Note SET WindowPosition = ? WHERE RemoteId = ?", ("ManagedPosition=", None))
    return result

def restore(src, dst):
    result = True

    if os.path.exists(src):
        shutil.copyfile(src, dst)
        # shutil.move(dst + "-shm", dst + "-shm.bak")
        # shutil.move(dst + "-wal", dst + "-wal.bak")
    else:
        result = False
    
    return result

def last_backup_version():
    dst = get_sticky_note_backup_path()
    return time.ctime(os.path.getmtime(dst)) if os.path.exists(dst) else None

def cmds(mode):
    err_code = 0

    sqlite_src = get_sticky_note_appdata_path()
    sqlite_dst = get_sticky_note_backup_path()

    if sqlite_src is None:
        err_code = -1
    else:
        if mode == 'backup':
            if backup(sqlite_src, sqlite_dst):
                print(f"Your sticky note is backed up at \"{sqlite_dst}\"\n")
                print(f"To restore your sticky note, place the backed up file in:\n\"{sqlite_src}\"\n\nafter you sign out from sticky note")
            else:
                err_code = -2
        elif mode == 'restore':
            if restore(sqlite_dst, sqlite_src):
                print("Your sticky notes has been restored")
            else:
                err_code = -3
        else:
            print("Mode not recognized! Available mode: 'backup' or 'restore'")

    log(err_code)
    return err_code

if __name__ == '__main__':
    if len(sys.argv) > 2:
        cmds(sys.argv[1])
    
    
