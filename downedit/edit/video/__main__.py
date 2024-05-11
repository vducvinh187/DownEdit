import os
import multiprocessing

from colorama import Fore

from ...utils.common import tool_selector
from ...utils.file_utils import FileUtil
from ._process import VideoProcess
from ...__config__ import (
    DE_VERSION,
    Extensions
)


def get_speed_factor(tool):
    if tool in ["Custom Speed", "Flip + Speed", "Speed + Music", "Flip + Speed + Music"]:
        return eval(input(f"{Fore.WHITE}[{Fore.MAGENTA}?{Fore.WHITE}] {Fore.YELLOW}Select Speed:{Fore.WHITE} "))
    return 1.0

def get_music_path(tool):
    if tool in ["Add Music", "Speed + Music", "Flip + Speed + Music"]:
        return input(f"{Fore.YELLOW}Enter Music:{Fore.WHITE} ")
    return tool

def start_process(
    tool: str,
    video_speed: float,
    music_path: str,
    video_preset: str,
    cpu_threads: int,
    input_folder: str
):
    input_folder = FileUtil.get_file_list(
        directory=input_folder,
        extensions=Extensions.VIDEO
    )
    output_folder = FileUtil.create_folder(
        folder_type="EDITED_VIDEO"
    )
    FileUtil.folder_path(output_folder, tool)

    video_process = VideoProcess(
        tool,
        video_speed,
        music_path,
        video_preset,
        cpu_threads,
        input_folder,
        output_folder
    )
    video_process.process()

    
def display_banner():
    banner_display = f"""{Fore.MAGENTA}
███████╗██████╗░██╗████████╗  ██╗░░░██╗██╗██████╗░███████╗░█████╗░
██╔════╝██╔══██╗██║╚══██╔══╝  ██║░░░██║██║██╔══██╗██╔════╝██╔══██╗
█████╗░░██║░░██║██║░░░██║░░░  ╚██╗░██╔╝██║██║░░██║█████╗░░██║░░██║
██╔══╝░░██║░░██║██║░░░██║░░░  ░╚████╔╝░██║██║░░██║██╔══╝░░██║░░██║
███████╗██████╔╝██║░░░██║░░░  ░░╚██╔╝░░██║██████╔╝███████╗╚█████╔╝
╚══════╝╚═════╝░╚═╝░░░╚═╝░░░  ░░░╚═╝░░░╚═╝╚═════╝░╚══════╝░╚════╝░
                Created by HengSok - v{DE_VERSION}
    """
    banner_msg = r"Example: C:\Users\Name\Desktop\Folder\Video"
    return banner_display, banner_msg


def main():
    max_cpu_cores = multiprocessing.cpu_count()
    banner_display, banner_msg = display_banner()
    tool_selector.display_banner(banner_display, banner_msg)
    available_tools = { 
        " Flip Horizontal": lambda: None,
        " Custom Speed": lambda: None,
        " Loop Video": lambda: None,
        " Flip + Speed": lambda: None,
        " Add Music": lambda: None,
        " Speed + Music": lambda: None,
        " Flip + Speed + Music": lambda: None,
        " Adjust Color": lambda: None,
    }
    video_presets = {
        " Ultrafast": "ultrafast",
        " Superfast": "superfast",
        " Veryfast": "veryfast",
        " Faster": "faster",
        " Fast": "fast",
        " Medium": "medium",
        " Slow": "slow",
    }
    cpu_cores_choices = [
        str(i) for i in range(
            1,
            max_cpu_cores + 1
        )
    ]
    user_folder = FileUtil.validate_folder(
        folder_path=input(f"{Fore.YELLOW}Enter folder:{Fore.WHITE} ")
    )
    selected_tool = tool_selector.select_menu(
        message=f"{Fore.YELLOW}Choose Tools{Fore.WHITE}", 
        choices=available_tools
    )
    video_speed = get_speed_factor(
        selected_tool
    )
    music_path = get_music_path(
        selected_tool
    )
    selected_presets = tool_selector.select_menu(
        message=f"{Fore.YELLOW}Video Preset{Fore.WHITE}",
        choices=video_presets
    )
    selected_threads = tool_selector.select_menu(
        message=f"{Fore.YELLOW}CPU Threads (Max: {max_cpu_cores}){Fore.WHITE}", 
        choices=cpu_cores_choices
    )
    start_process(
        selected_tool,
        video_speed,
        music_path,
        selected_presets,
        selected_threads,
        user_folder
    )


if __name__ == "__main__":
    main()
