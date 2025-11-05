#! /bin/bash

current_notes="a1-4.csv"
current_lesson="/home/laotze/Downloads/A1.1/[TutsNode.com] - Best Way to Learn German Language-Full Beginner Course-A1.1/6. Unit 5 - Mein Tag (My day)"
next_lesson="/home/laotze/Downloads/A1.1/[TutsNode.com] - Best Way to Learn German Language-Full Beginner Course-A1.1/7. Unit 6 - Hobbys und Freizeit (Hobbies and free time)"
last_lesson="21. 5.6 Wochentage (Days of the week).mp4"
  

cd "$current_lesson"

nohup thunar . &
nohup mpv "$last_lesson" &

cd

nvim "./notes/german/$current_notes"





