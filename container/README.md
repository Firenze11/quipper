# Quipper Docker Container

We use a Docker container to ensure a consistent environment across dev and prod. In particular, we are interested in ffmpeg and Python installations. ffmpeg in particular must be built with --enable-libass for subtitles rendering.

Helper scripts are provided in script/ for building and running the container.

## Future work

Right now this container is set up for development. I think it's actually kind of hard to use the same Docker image for both development and prod. In the future, we'll probably have both dev-container/ and prod-container/ directories, each with its own build.sh and run.sh.

The main difficulty is that in dev you want live code reloading, which means you can't include the source code in the image, and instead you must mount the source directory with -v. But in prod you want a self-contained image, so you must include the source code in the image.
