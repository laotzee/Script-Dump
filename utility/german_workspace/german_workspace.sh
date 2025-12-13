#! /bin/bash

current_notes="a2-2.csv"
current_folder="/home/laotze/Downloads/A1.2/[TutsNode.com] - Best Way to Learn German Language - Beginner Level 2-A1.2/2. Unit 2 - Reisen (Traveling)"
last_lesson="6. 2.02 - Modalverben (Modal verbs).mp4"

cd "$current_folder"

nohup thunar . &
nohup mpv "$last_lesson" &

cd

alacritty -e nvim ./notes/german/$current_notes
