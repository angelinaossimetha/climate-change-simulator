class Simulator:
    """Simulates the climate of Branlex"""
    def __init__(self):
        self.year = 0
        self.max_temperature = 100
        self.current_bad = 150
        self.worst_threshold = 80
        self.bad_threshold = 150
        self.current_worst = 0
        self.country_names = []
        self.policies = {}
        self.temperatures = {}
        self.bad_emissions = {}
        self.worst_emissions = {}

    def add_country(self, name: str, policy):
        """Adds a country its policy along with populating the
        hashtables -temperatures and emissions- to the simulation"""
        self.country_names.append(name)
        self.policies[name] = policy
        self.temperatures[name] = 0
        self.bad_emissions[name] = 0
        self.worst_emissions[name] = 0

    def reduce_pollution(self):
        """Reduces current bad based on its value"""
        if self.current_bad > self.bad_threshold:
            self.current_bad -= 1
        if self.current_worst > self.worst_threshold:
            self.current_worst -= 10

    def neighbors_average(self, emissions: dict, index=0) -> float:
        """Return average emissions of a given country's
        neighbors of non-empty list"""
        if len(emissions) == 1:
            return 0
        elif index == 0:
            return emissions[self.country_names[index + 1]]
        elif index == (len(self.country_names) - 1):
            return emissions[self.country_names[index - 1]]
        return (emissions[self.country_names[index - 1]] +
                emissions[self.country_names[index + 1]]) / 2

    def update_emission(self, emissions: dict, index=0):
        """Updates each country's emissions based on
        the country's policy"""
        if index < len(emissions):
            boolean = self.bad_emissions == emissions
            index = 0
            while index < len(self.country_names):
                country = self.country_names[index]
                emission = self.policies[country].emit(
                    self.temperatures[country],
                    self.neighbors_average(emissions, index),
                    boolean)
                if boolean:
                    self.bad_emissions[country] = emission
                    self.current_bad += emission
                else:
                    self.worst_emissions[country] = emission
                    self.current_worst += emission
                index += 1

    def update_temperature(self, index=0):
        """Updates each country's temperature based on the
        country's index in country_name"""
        if index < len(self.temperatures):
            current_country = self.country_names[index]
            self.temperatures[current_country] = \
                (self.current_bad / 5) + \
                        (self.worst_emissions[current_country] / 2) + \
                        (self.current_worst / 10) + (5 * index)
            self.update_temperature(index + 1)

    def max_temp_reached(self):
        """Return if at least one country has
        reached the max temperature"""
        for country in self.temperatures:
            if self.temperatures[country] >= self.max_temperature:
                return True
        return False

    def advance_year(self):
        """Advances the current year, updating country
        and global emissions and temperatures"""
        if not self.max_temp_reached():
            self.year += 1
            self.update_emission(self.bad_emissions)
            self.update_emission(self.worst_emissions)
            self.reduce_pollution()
            self.update_temperature()
            #print(self.current_worst)
            #print(self.current_bad)

    def report(self):
        """Generates a report for use in the display"""
        return [{'name': name, 'temperature': self.temperatures[name]}
                for name in self.country_names]