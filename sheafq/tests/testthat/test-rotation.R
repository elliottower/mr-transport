test_that("rotation_angle of orthogonal vectors is 90", {
  expect_equal(rotation_angle(c(1, 0), c(0, 1)), 90)
})


test_that("rotation_angle of identical vectors is 0", {
  expect_equal(rotation_angle(c(1, 0), c(1, 0)), 0)
})


test_that("rotation_angle of opposite vectors is 180", {
  expect_equal(rotation_angle(c(1, 0), c(-1, 0)), 180)
})


test_that("rotation_angle of zero vector is NaN", {
  expect_true(is.nan(rotation_angle(c(0, 0), c(1, 0))))
})


test_that("max_rotation finds the largest pairwise angle", {
  beta <- matrix(c(1, 0, 0, 1, 0.5, 0.5), nrow = 3, byrow = TRUE)
  result <- max_rotation(beta)
  expect_equal(result$theta_max, 90)
  expect_equal(sort(result$pair), c(1, 2))
})
