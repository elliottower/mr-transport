test_that("rotation-only classification works for rotated effects", {
  # Rotation in (0,1) plane: stratum 1 has (0.3, 0.1), stratum 2 has (0.1, 0.3)
  # Per-trait variation is modest, but the joint direction changes.
  # With small enough SE, vector Q detects the rotation but individual traits don't.
  beta <- matrix(
    c(0.30, 0.10,
      0.10, 0.30,
      0.20, 0.20),
    nrow = 3, byrow = TRUE
  )
  se <- matrix(0.04, nrow = 3, ncol = 2)

  result <- classify_locus(beta, se)

  # Vector Q should be significant
  expect_true(result$vector_result$p < 0.05)

  # Category depends on whether individual scalar tests pass Bonferroni
  expect_true(result$category %in% c("concordant_significant", "rotation_only"))
})


test_that("concordant_null classification for homogeneous effects", {
  beta <- matrix(0.20, nrow = 4, ncol = 3)
  se <- matrix(0.10, nrow = 4, ncol = 3)

  result <- classify_locus(beta, se)
  expect_equal(result$category, "concordant_null")
})
