import numpy as np

from .probability_space import ProbabilitySpace

## Discrete Distributions

class Bernoulli(ProbabilitySpace):
    """Defines a probability space for a Bernoulli
         distribution.

    Attributes:
      p (float): probability (number between 0 and 1)
        of a "success" (i.e., 1)
    """

    def __init__(self, p):
        if 0 <= p <= 1:
            self.p = p
        else:
            # TODO: implement error handling
            pass

    def draw(self):
        return np.random.binomial(n=1, p=self.p)

class Binomial(ProbabilitySpace):
    """Defines a probability space for a binomial
         distribution.

    Attributes:
      n (int): number of trials
      p (float): probability (number between 0 and 1)
        that each trial results in a "success" (i.e., 1)
    """

    def __init__(self, n, p):
        self.n = n
        self.p = p

    def draw(self):
        return np.random.binomial(n=self.n, p=self.p)

class Hypergeometric(ProbabilitySpace):
    """Defines a probability space for a hypergeometric
         distribution (which represents the number of
         ones in n draws without replacement from a box
         containing zeros and ones.

    Attributes:
      n (int): number of draws (without replacement)
        from the box
      N0 (int): number of 0s in the box
      N1 (int): number of 1s in the box
    """

    def __init__(self, n, N0, N1):
        self.n = n
        self.N0 = N0
        self.N1 = N1

    def draw(self):
        return np.random.hypergeometric(ngood=self.N1, nbad=self.N0, nsample=self.n)

class Geometric(ProbabilitySpace):
    """Defines a probability space for a geometric
         distribution (which represents the number
         of trials until the first success), including
         the success.

    Attributes:
      p (float): probability (number between 0 and 1)
        that each trial results in a "success" (i.e., 1)
    """

    def __init__(self, p):
        self.p = p

    def draw(self):
        return np.random.geometric(p=self.p)

class NegativeBinomial(ProbabilitySpace):
    """Defines a probability space for a negative
         binomial distribution (which represents the 
         number of trials until r successes), including
         the r successes.

    Attributes:
      r (int): desired number of successes
      p (float): probability (number between 0 and 1)
        that each trial results in a "success" (i.e., 1)
    """

    def __init__(self, r, p):
        self.r = r
        self.p = p

    def draw(self):
        # Numpy's negative binomial returns numbers in [0, inf),
        # but we want numbers in [r, inf).
        return self.r + np.random.negative_binomial(n=self.r, p=self.p)

class Pascal(NegativeBinomial):
    """Defines a probability space for a Pascal
         distribution (which represents the number
         of trials until r successes), not including
         the r successes.

    Attributes:
      r (int): desired number of successes
      p (float): probability (number between 0 and 1)
        that each trial results in a "success" (i.e., 1)
    """
    def draw(self):
        # Numpy's negative binomial returns numbers in [0, inf).
        return np.random.negative_binomial(n=self.r, p=self.p)

class Poisson(ProbabilitySpace):
    """Defines a probability space for a Poisson distribution.

    Attributes:
      lam (float): rate parameter for the Poisson distribution
    """

    def __init__(self, lam):
        self.lam = lam

    def draw(self):
        return np.random.poisson(lam=self.lam)


## Continuous Distributions

class Uniform(ProbabilitySpace):
    """Defines a probability space for a uniform distribution.

    Attributes:
      a (float): lower bound for possible values
      b (float): upper bound for possible values
    """

    def __init__(self, a=0.0, b=1.0):
        self.a = a
        self.b = b

    def draw(self):
        return np.random.uniform(low=self.a, high=self.b)

class Normal(ProbabilitySpace):
    """Defines a probability space for a normal distribution.

    Attributes:
      mean (float): mean parameter of the normal distribution
      var (float): variance parameter of the normal distribution
      sd (float): standard deviation parameter of the normal 
        distribution (if specified, var parameter will be ignored)
    """

    def __init__(self, mean=0.0, var=1.0, sd=None):
        self.mean = mean
        if sd is None:
            self.scale = np.sqrt(var)
        else:
            self.scale = sd
    
    def draw(self):
        return np.random.normal(loc=self.mean, scale=self.scale)

class Exponential(ProbabilitySpace):
    """Defines a probability space for an exponential distribution.
       Only one of scale or rate should be set. (The scale is the
       inverse of the rate.)

    Attributes:
      scale (float): scale parameter for gamma distribution
        (often symbolized beta = 1 / lambda)
      rate (float): rate parameter for gamma distribution
        (often symbolized lambda)
    """

    def __init__(self, rate=1.0, scale=None):
        self.scale = scale
        self.rate = rate

    def draw(self):
        if self.scale is None:
            return np.random.exponential(scale=1. / self.rate)
        else:
            return np.random.exponential(scale=self.scale)

class Gamma(ProbabilitySpace):
    """Defines a probability space for a gamma distribution.
       Only one of scale or rate should be set. (The scale is the
       inverse of the rate.)

    Attributes:
      shape (float): shape parameter for gamma distribution
        (often symbolized alpha)
      scale (float): scale parameter for gamma distribution
        (often symbolized beta = 1 / lambda)
      rate (float): rate parameter for gamma distribution
        (often symbolized lambda)
    """

    def __init__(self, shape, rate=1.0, scale=None):
        self.shape = shape
        self.scale = scale
        self.rate = rate
    
    def draw(self):
        if self.scale is None:
            return np.random.gamma(self.shape, 1. / self.rate)
        else:
            return np.random.gamma(self.shape, self.scale)

class Beta(ProbabilitySpace):
    """Defines a probability space for a beta distribution.

    Attributes:
      a (float): alpha parameter for beta distribution
      b (float): beta parameter for beta distribution
    """

    def __init__(self, a, b, scale=None):
        self.a = a
        self.b = b
    
    def draw(self):
        return np.random.beta(self.a, self.b)


## Multivariate Distributions

class MultivariateNormal(ProbabilitySpace):
    """Defines a probability space for a multivariate normal 
       distribution.

    Attributes:
      mean (1-D array_like, of length n): mean vector
      cov (2-D array_like, of shape (n, n)): covariance matrix
    """

    def __init__(self, mean, cov):
        if len(mean) != len(cov):
            raise Exception("The dimension of the mean vector" +
                            "is not compatible with the dimensions" +
                            "of the covariance matrix.")
        self.mean = mean
        self.cov = cov

    def draw(self):
        return tuple(np.random.multivariate_normal(self.mean, self.cov))

class BivariateNormal(MultivariateNormal):
    """Defines a probability space for a bivariate normal 
       distribution.

    Attributes:
      mean1 (float): mean parameter of X
      mean2 (float): mean parameter of Y
      sd1 (float): standard deviation parameter of X
      sd2 (float): standard deviation parameter of Y
      corr (float): correlation between X and Y
      var1 (float): variance parameter of X
        (if specified, sd1 will be ignored)
      var2 (float): variance parameter of Y
        (if specified, sd2 will be ignored)
      cov (float): covariance between X and Y
        (if specified, corr parameter will be ignored)
    """

    def __init__(self,
                 mean1=0.0, mean2=0.0,
                 sd1=1.0, sd2=1.0, corr=0.0,
                 var1=None, var2=None, cov=None):

        if corr is not None and not (-1 <= corr < 1):
            raise Exception("Correlation must be "
                            "between -1 and 1.")

        self.mean = [mean1, mean2]

        if var1 is None:
            var1 = sd1 ** 2
        if var2 is None:
            var2 = sd2 ** 2
        if cov is None:
            cov = corr * np.sqrt(var1 * var2)
        self.cov = [[var1, cov], [cov, var2]]
        
