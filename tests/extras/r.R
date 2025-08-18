# test script checking that all installed libraries are present

# Load the testthat package
library(testthat)

# List of libraries to check - comma delimited
libraries_to_check <- c(
    "GenomicSEM"
)

# Define a test
test_that("Required libraries are installed", {
  missing_libraries <- setdiff(libraries_to_check, installed.packages()[, "Package"])
  expect_true(length(missing_libraries) == 0, 
              sprintf("Missing libraries: %s", paste(missing_libraries, collapse = ", ")))
})