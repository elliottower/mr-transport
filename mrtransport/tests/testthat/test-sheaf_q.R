test_that("d=1 vector Q equals scalar Cochran's Q", {
  betas <- c(0.30, 0.25, 0.15)
  ses <- c(0.05, 0.06, 0.08)

  scalar <- scalar_cochran_q(betas, ses)
  vec <- vector_sheaf_q_diagonal(
    matrix(betas, ncol = 1),
    matrix(ses, ncol = 1)
  )

  expect_equal(vec$Q_V, scalar$Q, tolerance = 1e-10)
  expect_equal(vec$p, scalar$p, tolerance = 1e-10)
  expect_equal(vec$df, scalar$df)
})


test_that("diagonal covariance: Q_V equals sum of scalar Q", {
  beta <- matrix(
    c(0.30, 0.10,
      0.10, 0.30,
      0.20, 0.20),
    nrow = 3, byrow = TRUE
  )
  se <- matrix(0.04, nrow = 3, ncol = 2)

  result <- vector_sheaf_q_diagonal(beta, se)

  expect_equal(result$Q_V, result$sum_scalar_Q, tolerance = 1e-10)
})


test_that("correlated traits: Q_V diverges from sum of scalar Q", {
  beta <- matrix(
    c(0.30, 0.10,
      0.10, 0.30,
      0.20, 0.20),
    nrow = 3, byrow = TRUE
  )
  se <- matrix(0.04, nrow = 3, ncol = 2)
  rho <- matrix(c(1, 0.6, 0.6, 1), nrow = 2)

  result <- vector_sheaf_q_correlated(beta, se, rho)

  expect_true(result$Q_V > result$sum_scalar_Q)
  expect_true(result$Q_V / result$sum_scalar_Q > 1.5)
})


test_that("vector_sheaf_q with full covariance matches diagonal shortcut", {
  beta <- matrix(
    c(0.30, 0.10,
      0.10, 0.30,
      0.20, 0.20),
    nrow = 3, byrow = TRUE
  )
  se <- matrix(0.04, nrow = 3, ncol = 2)

  K <- nrow(beta)
  d <- ncol(beta)
  cov_arr <- array(0, dim = c(K, d, d))
  for (k in seq_len(K)) {
    cov_arr[k, , ] <- diag(se[k, ]^2, nrow = d)
  }

  full <- vector_sheaf_q(beta, cov_arr)
  diag_result <- vector_sheaf_q_diagonal(beta, se)

  expect_equal(full$Q_V, diag_result$Q_V, tolerance = 1e-10)
})


test_that("scalar_cochran_q reproduces textbook example", {
  betas <- c(0.20, 0.20, 0.20)
  ses <- c(0.05, 0.06, 0.04)
  result <- scalar_cochran_q(betas, ses)
  expect_equal(result$Q, 0, tolerance = 1e-10)
  expect_equal(result$I2, 0)
})
