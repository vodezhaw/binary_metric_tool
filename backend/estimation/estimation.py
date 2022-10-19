
from dataclasses import dataclass

import jax.numpy as jnp
import jax.random
import numpyro
import numpyro.distributions as dist
import numpyro.infer as infer
from scipy import stats


@dataclass(frozen=True)
class BinomialOutcome:
    n_pos: int
    n_total: int


@dataclass(frozen=True)
class Experiment:
    rho: BinomialOutcome
    eta: BinomialOutcome
    oracle: BinomialOutcome
    metric: BinomialOutcome


def sample_posterior(
    experiment: Experiment,
) -> jnp.array:

    def model_fn():
        rho = numpyro.sample(
            "rho",
            dist.Beta(
                experiment.rho.n_pos + 1,
                experiment.rho.n_total - experiment.rho.n_pos + 1,
            ),
        )
        eta = numpyro.sample(
            "eta",
            dist.Beta(
                experiment.eta.n_pos + 1,
                experiment.eta.n_total - experiment.eta.n_pos + 1,
            ),
        )
        alpha = numpyro.sample(
            "alpha",
            dist.Beta(
                experiment.oracle.n_pos + 1,
                experiment.oracle.n_total - experiment.oracle.n_pos + 1,
            )
        )

        alpha_observed = numpyro.deterministic(
            "alpha_observed",
            alpha * (rho + eta - 1.) + (1. - eta),
        )

        with numpyro.plate("data", 1):
            numpyro.sample(
                "n_pos",
                dist.Binomial(
                    total_count=experiment.metric.n_total,
                    probs=alpha_observed,
                ),
                obs=experiment.metric.n_pos,
            )

    sampler = infer.MCMC(
        infer.NUTS(model_fn),
        num_warmup=2000,
        num_samples=10000,
        num_chains=5,
        progress_bar=False,
    )

    random_seed = 0xdeadbeef
    sampler.run(jax.random.PRNGKey(random_seed))

    samples = sampler.get_samples(group_by_chain=False)

    return samples['alpha']


def simulated_experiment(
    n_human: int,
    n_rho_eta: int,
    n_metric: int,
    rho_true: float,
    eta_true: float,
    alpha_true: float,
) -> Experiment:

    observed_alpha = (alpha_true * (rho_true + eta_true - 1.)) + (1. - eta_true)
    rho_samples = int(round(alpha_true * n_rho_eta))
    eta_samples = n_rho_eta - rho_samples

    return Experiment(
        rho=BinomialOutcome(
            n_pos=int(round(rho_true * rho_samples)),
            n_total=rho_samples,
        ),
        eta=BinomialOutcome(
            n_pos=int(round(eta_true * eta_samples)),
            n_total=eta_samples,
        ),
        oracle=BinomialOutcome(
            n_pos=int(round(alpha_true * n_human)),
            n_total=n_human,
        ),
        metric=BinomialOutcome(
            n_pos=int(round(observed_alpha * n_metric)),
            n_total=n_metric,
        ),
    )


def estimate_epsilon(
    n_human: int,
    n_rho_eta: int,
    n_metric: int,
    rho: float,
    eta: float,
    alpha: float,
) -> float:

    if n_human == 0 and n_metric == 0:
        return 1.

    experiment = simulated_experiment(
        n_human=n_human,
        n_rho_eta=n_rho_eta,
        n_metric=n_metric,
        rho_true=rho,
        eta_true=eta,
        alpha_true=alpha,
    )

    samples = sample_posterior(experiment=experiment)

    variance = samples.var()

    _, eps = stats.norm.interval(0.95, loc=0., scale=jnp.sqrt(2*variance))

    return eps
