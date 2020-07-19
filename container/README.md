# Quipper Docker Container

We use a Docker container to ensure a consistent environment across dev and prod. In particular, we are interested in ffmpeg and Python installations. ffmpeg in particular must be built with --enable-libass for subtitles rendering.

Helper scripts are provided in script/ for building and running the container.
