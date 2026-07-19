#!/usr/bin/env bash

current_notes="a22-2.csv"
current_folder="/home/laotze/Downloads/A2.2/03. Unit 2 - Auf dem Flohmarkt (At the flea market)"
current_lesson="/home/laotze/notes/german/a22-2.csv"

cd "$current_folder" || echo "Folder does not exist" >&2

nohup thunar . &
nohup mpv "$current_lesson" &

alacritty -e nvim ~/notes/german/$current_notes
