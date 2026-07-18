test_that("rotation-only classification works for rotated effects", {
  beta <- matrix(
    c(0.30, 0.10,
      0.10, 0.30,
      0.20, 0.20),
    nrow = 3, byrow = TRUE
  )
  se <- matrix(0.04, nrow = 3, ncol = 2)

  result <- classify_locus(beta, se)

  expect_true(result$vector_result$p < 0.05)
  expect_true(result$category %in% c("concordant_significant", "rotation_only"))
})


test_that("concordant_null classification for homogeneous effects", {
  beta <- matrix(0.20, nrow = 4, ncol = 3)
  se <- matrix(0.10, nrow = 4, ncol = 3)

  result <- classify_locus(beta, se)
  expect_equal(result$category, "concordant_null")
})
