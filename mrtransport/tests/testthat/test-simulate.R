test_that("simulate_pair returns correct structure", {
  pair <- simulate_pair(k = 4, seed = 42)
  expect_equal(length(pair$betas), 4)
  expect_equal(length(pair$ses), 4)
  expect_equal(length(pair$strata_names), 4)
  expect_equal(pair$ground_truth, "transport")
  expect_equal(pair$params$k, 4)
})


test_that("simulate_pair with tau > 0 is non-transport", {
  pair <- simulate_pair(k = 4, tau = 0.3, seed = 42)
  expect_equal(pair$ground_truth, "non-transport")
})


test_that("simulate_pair seed is reproducible", {
  p1 <- simulate_pair(k = 3, seed = 123)
  p2 <- simulate_pair(k = 3, seed = 123)
  expect_equal(p1$betas, p2$betas)
  expect_equal(p1$ses, p2$ses)
})


test_that("simulate_catalog returns correct counts", {
  catalog <- simulate_catalog(n_transport = 5, n_nontransport = 3, seed = 42)
  expect_equal(length(catalog), 8)

  n_transport <- sum(vapply(catalog, function(p) p$ground_truth == "transport", logical(1)))
  n_nontransport <- sum(vapply(catalog, function(p) p$ground_truth == "non-transport", logical(1)))
  expect_equal(n_transport, 5)
  expect_equal(n_nontransport, 3)
})


test_that("simulate_catalog seed is reproducible", {
  c1 <- simulate_catalog(n_transport = 3, n_nontransport = 2, seed = 99)
  c2 <- simulate_catalog(n_transport = 3, n_nontransport = 2, seed = 99)
  for (i in seq_along(c1)) {
    expect_equal(c1[[i]]$betas, c2[[i]]$betas)
  }
})


test_that("simulate_catalog pairs have valid structure", {
  catalog <- simulate_catalog(n_transport = 3, n_nontransport = 2, seed = 42)
  for (pair in catalog) {
    expect_true(length(pair$betas) >= 3)
    expect_true(length(pair$betas) <= 6)
    expect_equal(length(pair$betas), length(pair$ses))
    expect_equal(length(pair$betas), length(pair$strata_names))
    expect_true(!is.null(pair$id))
    expect_true(pair$ground_truth %in% c("transport", "non-transport"))
  }
})
