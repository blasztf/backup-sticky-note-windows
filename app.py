import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox

from cmds import *

def main():

    def button_action_backup():
        src = get_sticky_note_appdata_path()
        dst = get_sticky_note_backup_path()
        if src is not None:
            result = messagebox.askyesno(message="This will replace last notes backup, if any.\nAre you sure?")
            if result:
                if backup(src, dst):
                    messagebox.showinfo(message="Your sticky notes has been backed up.")
                    string_last_version.set(last_backup_version())
                else:
                    messagebox.showerror(message="Error has been occurred!")

    def button_action_restore():
        src = get_sticky_note_appdata_path()
        dst = get_sticky_note_backup_path()
        if src is not None:
            result = messagebox.askyesno(message="This will replace current notes. Please make sure you already backup your notes.\nAre you sure?")
            if result:
                if restore(dst, src):
                    messagebox.showinfo(message="Your sticky notes has been restored.")
                else:
                    messagebox.showerror(message="Error has been occurred!")

    def button_action_migrate():
        title = "Migration Helper"
        result = messagebox.askyesno(
            title=title,
            message="Hi, we will help you to migrate your sticky notes from one account to another. Please follow the steps carefully.\n Do you want to continue?"
        )

        if result:
            messagebox.showinfo(
                title=title,
                message="First, we will backup your sticky notes. Please make sure you have already sync your sticky notes by go to the 'Settings' (click gear icon in the top-right) and then click 'Sync Now' button (available when signed in) before we backup your sticky notes in local."
            )
            button_action_backup()
            result = messagebox.askyesno(
                title=title,
                message="Is the backup process completed successfully?"
            )

            if result:
                messagebox.showinfo(
                    title=title,
                    message="Next, you must sign out the sticky notes app from your account. After that, click 'Ok' to continue."
                )
                messagebox.showinfo(
                    title=title,
                    message="Now, we will restore your sticky notes."
                )
                button_action_restore()
                result = messagebox.askyesno(
                    title=title,
                    message="Is the restore process completed successfully?"
                )

                if result:
                    messagebox.showinfo(
                        title=title,
                        message="For the last step, you can sign in to your new account and then sync your sticky notes by go to the 'Settings' (click gear icon in the top-right) and then click 'Sync Now' button (available when signed in)."
                    )
                    messagebox.showinfo(
                        title=title,
                        message="Done.\nCongratulation, you have migrate your sticky notes from old account to your new account. Please make sure again if everything is ok."
                    )
                else:
                    messagebox.showerror(
                        title=title,
                        message="Error has been occurred!"
                    )
            else:
                messagebox.showerror(
                    title=title,
                    message="Error has been occurred!"
                )

    title = "Backup Sticky Notes (from Microsoft)"

    window = tk.Tk()
    window.resizable(False, False)

    frame = ttk.Frame(window, padding=10)
    frame.grid()
    frame.winfo_toplevel().title("BSN")

    row = 0

    label_title = ttk.Label(
        master=frame,
        text=title
    )
    label_title.grid(column=0, row=row, columnspan=2)

    row = 1

    label_last_backup = ttk.Label(
        master=frame,
        text="Last backup"
    )
    label_last_backup.grid(column=0, row=row, sticky='W')

    last_version = last_backup_version()
    string_last_version = tk.StringVar()
    if last_version is not None:
        string_last_version.set(last_version)
    label_last_version = ttk.Label(
        master=frame,
        textvariable=string_last_version
    )
    label_last_version.grid(column=1, row=row, sticky='E')

    row = 2

    button_backup = ttk.Button(
        master=frame,
        text="Backup",
        command=button_action_backup
    )
    button_backup.grid(column=0, row=row, sticky='W')

    button_restore = ttk.Button(
        master=frame,
        text="Restore",
        command=button_action_restore
    )
    button_restore.grid(column=1, row=row, sticky='E')

    row = 3

    button_migrate = ttk.Button(
        master=frame,
        text="Sticky Notes Migration",
        command=button_action_migrate
    )
    button_migrate.grid(column=0, row=row, columnspan=2)

    window.mainloop()

if __name__ == '__main__':
    main()