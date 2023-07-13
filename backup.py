import os
import shutil
import sqlite3

def main():
    sticky_note_dir_cache = os.path.expandvars("%TMP%\\sndir.cache")

    sqlite_src = os.path.expandvars("%USERPROFILE%\\AppData\\Local\\Packages")

    if os.path.exists(sticky_note_dir_cache):
        with open(sticky_note_dir_cache, mode='r') as fhandle:
            dir = fhandle.readline()
    else:
        for dir in os.listdir(sqlite_src):
            if "Microsoft.MicrosoftStickyNotes" in dir:
                with open(sticky_note_dir_cache, mode='w') as fhandle:
                    fhandle.write(dir)
                break
            
    sqlite_src += f"\\{dir}\\LocalState\\plum.sqlite"
    
    sqlite_dst = os.path.expandvars("%USERPROFILE%\\Desktop\\plum.sqlite")
    
    try:
        shutil.copyfile(sqlite_src, sqlite_dst)
        shutil.copyfile(sqlite_src + "-shm", sqlite_dst + "-shm")
        shutil.copyfile(sqlite_src + "-wal", sqlite_dst + "-wal")
    except FileNotFoundError as e:
        print("No sticky note data can be found!")
        return -1

    with sqlite3.connect(sqlite_dst) as plum_conn:
        plum_cur = plum_conn.cursor()
        plum_cur.execute("UPDATE Note SET RemoteId = ?, ChangeKey = ?, LastServerVersion = ?, RemoteSchemaVersion = ?, IsRemoteDataInvalid = ?, PendingInsightsScan = ?, Type = ?", (None, None, None, None, None, None, None))
        #plum_cur.execute("UPDATE Note SET WindowPosition = ? WHERE RemoteId = ?", ("ManagedPosition=", None))
        
    print(f"Your sticky note is backed up at \"{sqlite_dst}\"\n")
    print(f"To restore your sticky note, place the backed up file in:\n\"{sqlite_src}\"\n\nafter you sign out from sticky note")

    return 0

if __name__ == '__main__':
    main()
    
    
