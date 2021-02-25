from simulator import *
from policies import *
import pytest


def test_year():
    s = Simulator()
    assert s.year == 0
    s.advance_year()
    assert s.year == 1


def test_reduce_pollution():
    # bad < 150 and worst < 80
    sim_1 = Simulator()
    sim_1.current_bad = 50
    sim_1.current_worst = 40
    sim_1.reduce_pollution()
    assert sim_1.current_bad == 50
    assert sim_1.current_worst == 40

    # bad < 150 and worst < 80
    sim_2 = Simulator()
    sim_2.current_bad = 149
    sim_2.current_worst = 79
    sim_2.reduce_pollution()
    assert sim_2.current_bad == 149
    assert sim_2.current_worst == 79

    # bad > 150 and worst > 80
    sim_3 = Simulator()
    sim_3.current_bad = 151
    sim_3.current_worst = 81
    sim_3.reduce_pollution()
    assert sim_3.current_bad == 150
    assert sim_3.current_worst == 71

    # bad > 150 and worst > 80
    sim_4 = Simulator()
    sim_4.current_bad = 170
    sim_4.current_worst = 97
    sim_4.reduce_pollution()
    assert sim_4.current_bad == 169
    assert sim_4.current_worst == 87

    # bad < 0 and worst < 0
    sim_5 = Simulator()
    sim_5.current_bad = -100
    sim_5.current_worst = -600
    sim_5.reduce_pollution()
    assert sim_5.current_bad == -100
    assert sim_5.current_worst == -600

    # bad = 150 and worst = 80
    sim_6 = Simulator()
    sim_6.current_bad = 150
    sim_6.current_worst = 80
    sim_6.reduce_pollution()
    assert sim_6.current_bad == 150
    assert sim_6.current_worst == 80



def test_add_country():
    # No countries - empty strings
    no_country = Simulator()
    assert no_country.country_names == []
    assert no_country.temperatures == {}
    assert no_country.worst_emissions == {}
    assert no_country.bad_emissions == {}

    # Only 1 country
    country_1 = Simulator()
    country_1.add_country("Peru", Reducing(50, 60, 10, 5))
    assert country_1.country_names == ["Peru"]
    assert country_1.temperatures == {"Peru": 0}
    assert country_1.worst_emissions == {"Peru": 0}
    assert country_1.bad_emissions == {"Peru": 0}

    # Two countries
    two_countries = Simulator()
    two_countries.add_country("Peru", Reducing(50, 60, 10, 5))
    two_countries.add_country("Italy", Reducing(60, 29, 10, 3))
    assert two_countries.country_names == ["Peru", "Italy"]
    assert two_countries.temperatures == {"Peru": 0, "Italy": 0}
    assert two_countries.bad_emissions == {"Peru": 0, "Italy": 0}
    assert two_countries.worst_emissions == {"Peru": 0, "Italy": 0}

    # Four countries
    four_countries = Simulator()
    four_countries.add_country("Peru", Reducing(50, 90, 10, 7))
    four_countries.add_country("Italy", Reducing(60, 29, 10, 3))
    four_countries.add_country("Germany", Reducing(70, 87, 15, 14))
    four_countries.add_country("USA", Reducing(100, 50, 5, 13))
    assert four_countries.country_names == \
           ["Peru", "Italy", "Germany", "USA"]
    assert four_countries.temperatures == {"Peru": 0,
                                           "Italy": 0,
                                           "Germany": 0,
                                           "USA": 0}
    assert four_countries.bad_emissions == {"Peru": 0,
                                            "Italy": 0,
                                            "Germany": 0,
                                            "USA": 0}
    assert four_countries.worst_emissions == {"Peru": 0,
                                              "Italy": 0,
                                              "Germany": 0,
                                              "USA": 0}


# Test for update_emission and neighbor_average
def test_update_emission_neighbors_average():
    # empty case
    emissions_empty = Simulator()
    emissions_empty.update_emission(emissions_empty.bad_emissions)
    emissions_empty.update_emission(emissions_empty.worst_emissions)
    assert emissions_empty.bad_emissions == {}
    assert emissions_empty.worst_emissions == {}
    assert emissions_empty.current_bad == 150
    assert emissions_empty.current_worst == 0
    with pytest.raises(IndexError, match="list index out of range"):
        emissions_empty.neighbors_average(emissions_empty.bad_emissions)
    with pytest.raises(IndexError, match="list index out of range"):
        emissions_empty.neighbors_average(emissions_empty.worst_emissions)

    # bad and worst emissions > 0, only one country
    positive_emissions_one = Simulator()
    positive_emissions_one.add_country("Peru", Reducing(50, 60, 10, 5))
    positive_emissions_one.update_emission(
        positive_emissions_one.bad_emissions)
    positive_emissions_one.update_emission(
        positive_emissions_one.worst_emissions)
    assert positive_emissions_one.bad_emissions == {"Peru": 40}
    assert positive_emissions_one.worst_emissions == {"Peru": 55}
    assert positive_emissions_one.current_bad == 190
    assert positive_emissions_one.current_worst == 55
    assert positive_emissions_one.neighbors_average(
        positive_emissions_one.bad_emissions) == 0
    assert positive_emissions_one.neighbors_average(
        positive_emissions_one.worst_emissions) == 0

    # bad and worst emissions > 0, multiple countries
    positive_emissions_multiple = Simulator()
    positive_emissions_multiple.add_country(
        "Peru", Reducing(50, 90, 10, 7))
    positive_emissions_multiple.add_country(
        "Italy", Reducing(60, 29, 10, 3))
    positive_emissions_multiple.add_country(
        "Germany", Reducing(70, 87, 15, 14))
    positive_emissions_multiple.add_country(
        "USA", Reducing(100, 50, 5, 13))
    positive_bad_emissions = positive_emissions_multiple.bad_emissions
    positive_worst_emissions = positive_emissions_multiple.worst_emissions
    positive_emissions_multiple.update_emission(positive_bad_emissions)
    positive_emissions_multiple.update_emission(positive_worst_emissions)
    assert positive_emissions_multiple.bad_emissions == {
        "Germany": 55, "Italy": 50, "Peru": 40, "USA": 95}
    assert positive_emissions_multiple.worst_emissions == {
        "Germany": 73, "Italy": 26, "Peru": 83, "USA": 37}
    assert positive_emissions_multiple.current_bad == 390
    assert positive_emissions_multiple.current_worst == 219
    # bad
    assert positive_emissions_multiple.neighbors_average(
        positive_bad_emissions, 0) == 50
    assert positive_emissions_multiple.neighbors_average(
        positive_bad_emissions, 1) == 47.5
    assert positive_emissions_multiple.neighbors_average(
        positive_bad_emissions, 2) == 72.5
    assert positive_emissions_multiple.neighbors_average(
        positive_bad_emissions, 3) == 55
    # worst
    assert positive_emissions_multiple.neighbors_average(
        positive_worst_emissions, 0) == 26
    assert positive_emissions_multiple.neighbors_average(
        positive_worst_emissions, 1) == 78
    assert positive_emissions_multiple.neighbors_average(
        positive_worst_emissions, 2) == 31.5
    assert positive_emissions_multiple.neighbors_average(
        positive_worst_emissions, 3) == 73

    # bad and worst emissions = 0
    zero_emissions = Simulator()
    zero_emissions.add_country("Peru", Reducing(50, 80, 0, 0))
    zero_emissions.update_emission(zero_emissions.bad_emissions)
    zero_emissions.update_emission(zero_emissions.worst_emissions)
    assert zero_emissions.bad_emissions == {"Peru": 50}
    assert zero_emissions.current_bad == 200
    assert zero_emissions.neighbors_average(
        zero_emissions.bad_emissions, True) == 0
    assert zero_emissions.neighbors_average(
        zero_emissions.worst_emissions, True) == 0
    assert zero_emissions.worst_emissions == {"Peru": 80}
    assert zero_emissions.current_worst == 80
    assert zero_emissions.neighbors_average(
        zero_emissions.bad_emissions, False) == 0
    assert zero_emissions.neighbors_average(
        zero_emissions.worst_emissions, False) == 0


    # bad and worst emissions < 0 (Less than last years emission, negative)
    negative_emissions = Simulator()
    negative_emissions.add_country("Peru",
                                   Reducing(50, 60, -10, -20))
    negative_emissions.update_emission(
        negative_emissions.bad_emissions)
    negative_emissions.update_emission(
        negative_emissions.worst_emissions)
    assert negative_emissions.bad_emissions == {"Peru": 60}
    assert negative_emissions.current_bad == 210
    assert negative_emissions.worst_emissions == {"Peru": 80}
    assert negative_emissions.current_worst == 80
    assert negative_emissions.neighbors_average(
        negative_emissions.bad_emissions, True) == 0
    assert negative_emissions.neighbors_average(
        negative_emissions.worst_emissions, False) == 0


#Test for update_temperature and max_temp_reached
def test_update_temperature_max():
    # temperature < max.temperature, empty country
    empty_temperature = Simulator()
    empty_temperature.update_temperature()
    assert empty_temperature.temperatures == {}

    # temperature < max.temperature, one country
    one_temperature = Simulator()
    one_temperature.add_country("Peru", Reducing(50, 70, 10, 5))
    one_temperature.update_temperature()
    assert one_temperature.temperatures == {"Peru": 30.0}

    # temperature < max.temperature, multiple countries
    multiple_temperature = Simulator()
    multiple_temperature.add_country("Peru", Reducing(50, 90, 10, 7))
    multiple_temperature.add_country("Italy", Reducing(60, 29, 10, 3))
    multiple_temperature.add_country("Germany", Reducing(70, 87, 15, 14))
    multiple_temperature.add_country("USA", Reducing(100, 50, 5, 13))
    multiple_temperature.update_temperature()
    assert multiple_temperature.temperatures == {
        "Peru": 30, "Italy": 35 , "Germany": 40, "USA": 45}

    # temperature = max.temperature
    same_temperature = Simulator()
    same_temperature.current_bad = 475
    same_temperature.current_worst = 600
    same_temperature.add_country("Peru",
                                 Reducing(50, 90, 10, 7))
    same_temperature.add_country("Italy",
                                 Reducing(60, 29, 10, 3))
    same_temperature.update_temperature()
    assert same_temperature.temperatures == {
        "Peru": 155, "Italy": 160}
    assert same_temperature.max_temp_reached() == True

    # temperature > max.temperature
    max_temperature = Simulator()
    max_temperature.current_bad = 495
    same_temperature.current_worst = 614
    max_temperature.add_country("Peru", Reducing(50, 90, 10, 7))
    max_temperature.add_country("Italy", Reducing(60, 29, 10, 3))
    max_temperature.update_temperature()
    assert max_temperature.temperatures == {
        "Peru": 99.0, "Italy": 104.0}
    assert max_temperature.max_temp_reached() == True


def test_advance_year():
    year_1 = Simulator()

    # Incrementing the current year
    year_1.advance_year()
    assert year_1.year == 1

    # Reduce pollution
    year_1.current_bad = 151
    year_1.current_worst = 89
    year_1.reduce_pollution()
    assert year_1.current_bad == 150
    assert year_1.current_worst == 79


    # Updating Emissions
    year_1.add_country("Peru", Reducing(50, 90, 10, 7))
    year_1.add_country("Italy", Reducing(60, 29, 10, 3))
    year_1.add_country("Germany", Reducing(70, 87, 15, 14))
    year_1.add_country("USA", Reducing(100, 50, 5, 13))
    year_1.update_emission(year_1.bad_emissions)
    year_1.update_emission(year_1.worst_emissions)
    assert year_1.bad_emissions == {
        "Germany": 55, "Italy": 50, "Peru": 40, "USA": 95}
    assert year_1.worst_emissions == {
        'Germany': 73, 'Italy': 26, 'Peru': 83, 'USA': 37}

    # Verify that current_bad and current_worst are updated correctly
    assert year_1.current_bad == 390
    assert year_1.current_worst == 298

    # Updating Temperatures and check max temperature reached
    year_1.update_temperature()
    assert year_1.temperatures == {
        'Germany': 154.3, 'Italy': 125.8, 'Peru': 149.3, 'USA': 141.3}
    assert year_1.max_temp_reached() == True



def test_report():
    # Empty list, no country
    empty_report = Simulator()
    empty_report.update_emission(empty_report.worst_emissions)
    empty_report.update_emission(empty_report.bad_emissions)
    empty_report.update_temperature()
    assert empty_report.report() == []

    # Only one country
    only_report = Simulator()
    only_report.add_country("Peru", Reducing(50, 90, 10, 7))
    only_report.update_emission(only_report.worst_emissions)
    only_report.update_emission(only_report.bad_emissions)
    only_report.update_temperature()
    assert only_report.report() == [
        {'name': 'Peru', 'temperature': 44.0}]

    # Multiple Countries
    multiple_report = Simulator()
    multiple_report.add_country("Peru", Reducing(50, 90, 10, 7))
    multiple_report.add_country("Italy", Reducing(60, 29, 10, 3))
    multiple_report.update_emission(multiple_report.bad_emissions)
    multiple_report.update_emission(multiple_report.worst_emissions)
    multiple_report.update_temperature()
    assert multiple_report.report() == [
        {'name': 'Peru', 'temperature': 100.4},
        {'name': 'Italy', 'temperature': 76.9}]

