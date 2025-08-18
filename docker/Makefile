all: rcontainer.sif  # additional .sif files may be listed here for corresponding dockerfiles

%.sif: dockerfiles/%/Dockerfile
	docker build -t $* -f dockerfiles/$*/Dockerfile . && \
	scripts/convert_docker_image_to_singularity.sh $* && \
	scripts/move_singularity_file.sh $*

# Example commands executed by this make file
# 
# Running "make rcontainer.sif" will issue the following commands:
# docker build -t rcontainer -f dockerfiles/rcontainer/Dockerfile . && \  # build docker container
#     scripts/convert_docker_image_to_singularity.sh rcontainer && \         # produces rcontainer.sif
#     scripts/move_singularity_file.sh.sh rcontainer        # moves rcontainer.sif to ../singularity/.
#  
# Running "make all" will build all singularity containers in this project
