class Baseline:
    """Emits at a constant rate"""

    def __init__(self, bad_baseline: float, worst_baseline: float):
        self.bad_baseline = bad_baseline
        self.worst_baseline = worst_baseline

    def emit(self, temperature: float, avg_neighbors: float,
             boolean: bool) -> float:
        """"Returns a constant emission rate"""
        if boolean:
            return self.bad_baseline
        else:
            return self.worst_baseline


class Reducing:
    """Reduces emissions every year"""

    def __init__(self, bad_baseline: float, worst_baseline: float,
                 bad_increment: float, worst_increment: float):
        self.worst_increment = worst_increment
        self.bad_increment = bad_increment
        self.worst_baseline = worst_baseline
        self.bad_baseline = bad_baseline

    def helper(self, baseline: float, increment: float) -> float:
        """Adjusts baseline based on the policy, can differentiate
        between BaD emissions or WoRSe emissions"""
        if baseline > 0:
            baseline -= increment
        else:
            baseline = 0
        return baseline

    def emit(self, temperature: float, avg_neighbors: float,
             boolean: bool) -> float:
        """"Returns and modifies a reduced emission based on baseline """
        if boolean:
            self.bad_baseline = self.helper(self.bad_baseline,
                                            self.bad_increment)
            return self.bad_baseline
        else:
            self.worst_baseline = self.helper(self.worst_baseline,
                                              self.worst_increment)
            return self.worst_baseline




class TemperaturePanic:
    """Emits at a constant rate until a temp threshold is reached"""

    def __init__(self, bad_baseline: float, worst_baseline: float,
                 bad_increment: float, worst_increment: float,
                 bad_threshold: float, worst_threshold: float):
        self.bad_baseline = bad_baseline
        self.bad_threshold = bad_threshold
        self.bad_increment = bad_increment
        self.worst_baseline = worst_baseline
        self.worst_threshold = worst_threshold
        self.worst_increment = worst_increment

    def helper(self, temperature: float, threshold: float, baseline: float,
               increment: float) -> float:
        """Adjusts baseline based on the policy, can differentiate between
        BaD emissions or WoRSe emissions"""
        if temperature > threshold:
            baseline -= increment
            if baseline <= 0:
                baseline = 0
        return baseline

    def emit(self, temperature: float, avg_neighbors: float,
             boolean: bool) -> float:
        """"Returns and modifies emission based on country's temperature """
        if boolean:
            self.bad_baseline = self.helper(temperature, self.bad_threshold,
                                    self.bad_baseline, self.bad_increment)
            return self.bad_baseline
        else:
            self.worst_baseline = self.helper(temperature,
                                              self.worst_threshold,
                                self.worst_baseline, self.worst_increment)
            return self.worst_baseline


class NeighborAverage:
    """Adjusts emissions towards its neighbors' average"""

    def __init__(self, bad_baseline: float, worst_baseline: float,
                 bad_increment: float, worst_increment: float):
        self.bad_baseline = bad_baseline
        self.bad_increment = bad_increment
        self.worst_baseline = worst_baseline
        self.worst_increment = worst_increment

    def helper(self, avg_neighbors: float, baseline: float,
               increment: float):
        """Adjusts baseline based on the policy, can differentiate between
        BaD emissions or WoRSe emissions"""
        if avg_neighbors < baseline:
            baseline -= increment
        else:
            baseline += increment
        if baseline < 0:
            baseline = 0
        return baseline

    def emit(self, temperature: float, avg_neighbors: float,
             boolean: bool) -> float:
        """"Returns and modifies emission based on country's neighbors'
        average emission """
        if boolean:
            self.bad_baseline = self.helper(avg_neighbors,
                                        self.bad_baseline,
                                            self.bad_increment)
            return self.bad_baseline
        else:
            self.worst_baseline = self.helper(avg_neighbors,
                                    self.worst_baseline,
                                              self.worst_increment)
            return self.worst_baseline


class SocialDistancing:
    """When the country's temperature is at or above the
    upper threshold, the country cuts its emissions of both
    compounds to 0. When the country's temperature is below
    the lower threshold, the country increments both
    emissions upward. When the country's temperature
    is between the two thresholds,the country's emissions
    are constant."""

    def __init__(self, bad_baseline: float, worst_baseline: float,
                 bad_increment: float, worst_increment: float,
                 lower_threshold: float, upper_threshold: float):
        self.worst_increment = worst_increment
        self.bad_increment = bad_increment
        self.worst_baseline = worst_baseline
        self.bad_baseline = bad_baseline
        self.lower_threshold = lower_threshold
        self.upper_threshold = upper_threshold

    def helper(self, temperature: float, baseline: float,
               increment: float):
        """Adjusts baseline based on the policy, can differentiate
        between BaD emissions or WoRSe emissions"""
        if temperature >= self.upper_threshold:
            baseline = 0
        elif (temperature >= self.lower_threshold) and \
                (temperature < self.upper_threshold):
            baseline = baseline
        else:
            baseline += increment
        return baseline

    def emit(self, temperature: float, avg_neighbors: float,
             boolean: bool) -> float:
        """Returns and modifies emission based on country's lower and
        upper temperature thresholds"""
        if boolean:
            self.bad_baseline = self.helper(temperature, self.bad_baseline,
                                            self.bad_increment)
            return self.bad_baseline
        else:
            self.worst_baseline = self.helper(temperature,
                                    self.worst_baseline,
                                              self.worst_increment)
            return self.worst_baseline

