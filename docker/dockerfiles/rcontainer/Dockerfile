FROM ghcr.io/rocker-org/verse:4.5.1

ENV TZ=Europe
ENV DEBIAN_FRONTEND=noninteractive

WORKDIR /tmp
COPY /scripts/apt_get_essential.sh .
RUN bash apt_get_essential.sh && \
    rm apt_get_essential.sh

# R packages.
# Install in order, if CRAN packages exist, install them first, and so forth in downstream order.
# CRAN packages:
WORKDIR /tmp/
RUN R -e "install.packages('devtools', repos='https://packagemanager.posit.co/cran/__linux__/noble/2025-08-01', dependencies=c('Depends', 'Imports', 'LinkingTo'))"
COPY /scripts/R/cran.R .
RUN Rscript cran.R

# Bioconductor distributed packages:
COPY /scripts/R/bioconductor.R .
RUN Rscript bioconductor.R

# GitHub distributed packages:
COPY /scripts/R/github.R .
RUN --mount=type=secret,id=github_pat \
    github_pat=$(cat /run/secrets/github_pat) \
    Rscript github.R

# Misc. packages
COPY /scripts/R/source.R .
RUN Rscript source.R && \
    rm -rf /tmp/*

WORKDIR /home
