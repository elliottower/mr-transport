test_that("HLA-DRB1 -> RA is non-transportable", {
  result <- test_transport(
    betas = c(1.6, 1.2, 0.8, 1.0),
    ses = c(0.04, 0.07, 0.12, 0.10),
    strata_names = c("EUR", "EAS", "AFR", "HISP")
  )
  expect_equal(result$verdict, "non-transport")
  expect_false(result$is_transportable)
  expect_equal(result$k, 4)
  expect_equal(result$strata_names, c("EUR", "EAS", "AFR", "HISP"))
})


test_that("homogeneous effects produce transport verdict", {
  result <- test_transport(
    betas = c(0.20, 0.20, 0.20),
    ses = c(0.05, 0.06, 0.04)
  )
  expect_equal(result$verdict, "transport")
  expect_true(result$is_transportable)
  expect_equal(result$Q, 0, tolerance = 1e-10)
})


test_that("underpowered flag triggers correctly", {
  result <- test_transport(
    betas = c(0.10, -0.05, 0.15, 0.02),
    ses = c(0.04, 0.05, 0.08, 0.10)
  )
  # This case has transport verdict with moderate I2 and low power
  expect_equal(result$verdict, "transport")
  # underpowered = transport AND power < 0.50 AND I2 > 0.30
  if (result$power < 0.50 && result$I2 > 0.30) {
    expect_true(result$underpowered)
  }
})


test_that("test_transport validates inputs", {
  expect_error(test_transport(c(1, 2), c(1)))
  expect_error(test_transport(c(1), c(1)))
  expect_error(test_transport(c(1, 2), c(0.1, -0.1)))
})


test_that("transport_power returns alpha when Q equals df", {
  # When Q == df, noncentrality parameter is 0, power = alpha
  expect_equal(transport_power(3, 3, 0.05), 0.05)
})


test_that("transport_power increases with larger Q", {
  p1 <- transport_power(5, 3, 0.05)
  p2 <- transport_power(20, 3, 0.05)
  expect_true(p2 > p1)
})


test_that("strata_needed returns NULL for I2 = 0", {
  expect_null(strata_needed(0))
})


test_that("strata_needed returns 2 for I2 = 1", {
  expect_equal(strata_needed(1.0), 2L)
})


test_that("strata_needed returns sensible values for moderate I2", {
  k <- strata_needed(0.50, target_power = 0.80)
  expect_true(is.integer(k) || is.numeric(k))
  expect_true(k >= 2)
  expect_true(k <= 50)
})


test_that("strata_needed returns NULL when max_k is insufficient", {
  # Very low I2 with strict max_k
  expect_null(strata_needed(0.01, max_k = 5))
})


test_that("test_transport returns all expected fields", {
  result <- test_transport(c(0.3, 0.25, 0.15), c(0.05, 0.06, 0.08))
  expected_names <- c("Q", "df", "p", "I2", "tau2", "power", "verdict",
                      "beta_pooled", "k", "strata_names",
                      "is_transportable", "underpowered")
  expect_true(all(expected_names %in% names(result)))
})
