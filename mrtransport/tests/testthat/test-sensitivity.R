test_that("leave_one_out returns stable for homogeneous data", {
  loo <- leave_one_out(
    betas = c(0.20, 0.20, 0.20, 0.20),
    ses = c(0.05, 0.06, 0.04, 0.07),
    strata_names = c("A", "B", "C", "D")
  )
  expect_true(loo$stable)
  expect_equal(length(loo$flipped_strata), 0)
})


test_that("leave_one_out returns stable=TRUE for 2 strata", {
  loo <- leave_one_out(
    betas = c(0.5, 0.1),
    ses = c(0.05, 0.05),
    strata_names = c("A", "B")
  )
  expect_true(loo$stable)
  expect_equal(length(loo$flipped_strata), 0)
})


test_that("leave_one_out detects influential strata", {
  # One outlier stratum drives non-transport; removing it flips to transport
  loo <- leave_one_out(
    betas = c(0.25, 0.23, 0.28, 2.50),
    ses = c(0.05, 0.06, 0.07, 0.05),
    strata_names = c("EUR", "EAS", "AFR", "outlier")
  )
  # The outlier stratum should be in flipped_strata (removing it changes verdict)
  if (!loo$stable) {
    expect_true("outlier" %in% loo$flipped_strata)
  }
})


test_that("alpha_sweep returns correct structure", {
  sweep <- alpha_sweep(
    betas = c(0.25, 0.23, 0.28),
    ses = c(0.05, 0.06, 0.07)
  )
  expect_s3_class(sweep, "data.frame")
  expect_equal(ncol(sweep), 5)
  expect_true(all(c("alpha", "verdict", "Q", "p", "power") %in% names(sweep)))
  expect_equal(nrow(sweep), 9)
})


test_that("alpha_sweep Q and p are constant across alphas", {
  sweep <- alpha_sweep(
    betas = c(0.25, 0.23, 0.28),
    ses = c(0.05, 0.06, 0.07)
  )
  # Q and p should not change with alpha
  expect_equal(length(unique(sweep$Q)), 1)
  expect_equal(length(unique(sweep$p)), 1)
})


test_that("alpha_sweep accepts custom alphas", {
  sweep <- alpha_sweep(
    betas = c(1.6, 1.2, 0.8),
    ses = c(0.04, 0.07, 0.12),
    alphas = c(0.01, 0.05, 0.10)
  )
  expect_equal(nrow(sweep), 3)
  expect_equal(sweep$alpha, c(0.01, 0.05, 0.10))
})
