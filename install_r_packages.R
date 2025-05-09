# Install remotes and BiocManager if not already installed
required <- c("remotes", "BiocManager")

for (pkg in required) {
  if (!require(pkg, character.only = TRUE)) {
    install.packages(pkg, repos = "https://cloud.r-project.org/") # automatically selects geographically closest CRAN mirror
  }
}

# Install dnaMethyAge from GitHub
remotes::install_github("yiluyucheng/dnaMethyAge")