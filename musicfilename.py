import os
import tkinter as tk
from tkinter import filedialog, messagebox
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, TIT2, TALB, TPE1, TRCK
from mutagen.flac import FLAC

def get_audio_info(file_path):
    """
    获取音频文件的标签信息：曲号、歌曲名、艺术家等
    """
    try:
        if file_path.lower().endswith(".mp3"):
            audio = MP3(file_path, ID3=ID3)
            track_num = audio.tags.get("TRCK")
            title = audio.tags.get("TIT2")
            artist = audio.tags.get("TPE1")
            if track_num and title and artist:
                return track_num.text[0], title.text[0], artist.text[0]
        elif file_path.lower().endswith(".flac"):
            audio = FLAC(file_path)
            track_num = audio.get("tracknumber")
            title = audio.get("title")
            artist = audio.get("artist")
            if track_num and title and artist:
                return track_num[0], title[0], artist[0]
        else:
            return None
    except Exception as e:
        print(f"Error reading tags from {file_path}: {e}")
        return None

def rename_files_in_directory(directory, include_track, include_title, include_artist):
    """
    遍历目录中的音频文件，根据选中的选项重命名文件
    """
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        if os.path.isfile(file_path) and (filename.lower().endswith(".mp3") or filename.lower().endswith(".flac")):
            audio_info = get_audio_info(file_path)
            if audio_info:
                track_num, title, artist = audio_info

                # 根据用户选择的选项构建文件名
                new_filename = ""
                if include_track:
                    new_filename += f"{track_num.zfill(2)}"
                if include_title:
                    new_filename += f" - {title}"
                if include_artist:
                    new_filename += f" - {artist}"

                # 保留原文件扩展名
                new_filename += os.path.splitext(filename)[1]
                new_file_path = os.path.join(directory, new_filename)

                # 重命名文件
                try:
                    os.rename(file_path, new_file_path)
                    print(f"Renamed: {filename} -> {new_filename}")
                except Exception as e:
                    print(f"Error renaming {filename}: {e}")

def choose_directory(path_entry):
    """
    打开文件夹选择对话框，并更新路径文本框
    """
    folder_selected = filedialog.askdirectory()
    if folder_selected:
        path_entry.delete(0, tk.END)  # 清空文本框
        path_entry.insert(0, folder_selected)  # 插入新的路径

def start_conversion(directory, include_track, include_title, include_artist):
    """
    开始转换文件名
    """
    if directory:
        rename_files_in_directory(directory, include_track, include_title, include_artist)
        messagebox.showinfo("Done", "文件重命名完成！")
    else:
        messagebox.showwarning("WARNING", "请先选择一个文件夹。")

def create_gui():
    """
    创建带复选框和文本框的图形界面
    """
    root = tk.Tk()
    root.title("Music_Filename")

    label = tk.Label(root, text="选择文件夹与选择要添加到文件名的信息")
    label.pack(pady=10)

    # 创建复选框
    include_track = tk.BooleanVar()
    include_title = tk.BooleanVar()
    include_artist = tk.BooleanVar()

    track_checkbox = tk.Checkbutton(root, text="曲号", variable=include_track)
    track_checkbox.pack(anchor="w")

    title_checkbox = tk.Checkbutton(root, text="歌曲名", variable=include_title)
    title_checkbox.pack(anchor="w")

    artist_checkbox = tk.Checkbutton(root, text="艺术家", variable=include_artist)
    artist_checkbox.pack(anchor="w")

    # 路径显示文本框
    path_label = tk.Label(root, text="选中的文件夹路径：")
    path_label.pack(pady=5)

    path_entry = tk.Entry(root, width=40)
    path_entry.pack(pady=5)

    # 创建选择文件夹按钮
    choose_button = tk.Button(root, text="选择文件夹", command=lambda: choose_directory(path_entry))
    choose_button.pack(pady=10)

    # 创建开始转换按钮
    convert_button = tk.Button(root, text="开始转换", command=lambda: start_conversion(path_entry.get(), include_track.get(), include_title.get(), include_artist.get()))
    convert_button.pack(pady=10)

    root.geometry("400x300")
    root.mainloop()

if __name__ == "__main__":
    create_gui()
