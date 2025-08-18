url <- "https://packagemanager.posit.co/cran/__linux__/noble/2025-08-01"
dependencies <- c('Depends', 'Imports', 'LinkingTo')
# upgrade <- 'default'
upgrade <- 'never'
auth_token <- Sys.getenv("github_pat")
cat("GitHub PAT length: ", nchar(auth_token), "\n")

# GitHub packages w. Git SHA - comma delimited
packages <- list(
    'GenomicSEM/GenomicSEM'='8e0ef594e95885b1f734f1dfcfe668b16ada2880'
)

# install package from GitHub and quit with error if installation fails
for (package in names(packages)) {
    ref <- packages[[package]]
    cat("Installing package ", package, " from GitHub with ref ", ref, "\n")
    tryCatch(
    {
        devtools::install_github(package, ref=ref, repos=url, dependencies=dependencies, upgrade=upgrade, auth_token=auth_token)
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
