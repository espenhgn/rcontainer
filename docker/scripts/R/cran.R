require(devtools)
url <- "https://packagemanager.posit.co/cran/__linux__/noble/2025-08-01"
dependencies <- c('Depends', 'Imports', 'LinkingTo')
upgrade <- 'default'

options(repos = c(CRAN = url))

# CRAN packages to install, comma delimited
packages <- list(
    'simsalapar',
    'matrixStats',
    'psych',
    'egg',
    'ggpubr',
    'ggrepel',
    'corrplot')

# install package from CRAN and quit with error if installation fails
for (package in packages) {
    tryCatch(
    {
        devtools::install_cran(package, dependencies=dependencies, upgrade=upgrade)
    },
    error = function(e) {
        cat("Error occurred during package installation:\n")
        print(e)
        quit(status=1, save='no')
    },
    finally = {
    }
    )
}
