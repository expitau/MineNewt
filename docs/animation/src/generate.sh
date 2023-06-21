manim render -ql --media_dir ../media scene.py Stochastic Tanh
mkdir ../media/gifs
ffmpeg -i ../media/videos/scene/480p15/Stochastic.mp4 ../media/gifs/Stochastic.gif
ffmpeg -i ../media/videos/scene/480p15/Tanh.mp4 ../media/gifs/Tanh.gif
