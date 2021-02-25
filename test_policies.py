from policies import *

def test_baseline_emit():
    # positive baseline
    positive_rate = Baseline(50, 70)
    assert positive_rate.emit(150, 60, True) == 50
    assert positive_rate.emit(150, 60, False) == 70
    # negative baseline
    negative_rate = Baseline(-78, -60)
    assert negative_rate.emit(150, 60, True) == -78
    assert negative_rate.emit(150, 60, False) == -60
    # zero baseline
    no_rate = Baseline(0, 0)
    assert no_rate.emit(150, 60, True) == 0
    assert no_rate.emit(150, 60, False) == 0


def test_reducing_emit():
    # positive increment
    positive_increment = Reducing(50, 60, 10, 15)
    assert positive_increment.helper(
        positive_increment.bad_baseline,
        positive_increment.bad_increment) == 40
    assert positive_increment.helper(
        positive_increment.worst_baseline,
        positive_increment.worst_increment) == 45
    assert positive_increment.emit(150, 60, False) == 45
    assert positive_increment.emit(150, 60, True) == 40

    # negative increment
    negative_increment = Reducing(50, 60, -10, -15)
    assert negative_increment.helper(
        negative_increment.bad_baseline,
        negative_increment.bad_increment) == 60
    assert negative_increment.helper(
        negative_increment.worst_baseline,
        negative_increment.worst_increment) == 75
    assert negative_increment.emit(160, 70, False) == 75
    assert negative_increment.emit(160, 70, True) == 60

    # zero increment
    zero_increment = Reducing(50, 60, 0, 0)
    assert zero_increment.helper(
        zero_increment.bad_baseline,
        zero_increment.bad_increment) == 50
    assert zero_increment.helper(
        zero_increment.worst_baseline,
        zero_increment.worst_increment) == 60
    assert zero_increment.emit(150, 70, True) == 50
    assert zero_increment.emit(150, 70, False) == 60

    # positive baseline
    positive_baseline = Reducing(50, 60, 10,15)
    assert positive_baseline.helper(
        positive_baseline.bad_baseline,
        positive_baseline.bad_increment) == 40
    assert positive_baseline.helper(
        positive_baseline.worst_baseline,
        positive_baseline.worst_increment) == 45
    assert positive_baseline.emit(150, 60, True) == 40
    assert positive_baseline.emit(150, 60, False) == 45

    # negative baseline
    negative_baseline = Reducing(-50,-60, 10,15)
    assert negative_baseline.helper(
        negative_baseline.bad_baseline,
        negative_baseline.bad_increment) == 0
    assert negative_baseline.helper(
        negative_baseline.worst_baseline,
        negative_baseline.worst_increment) == 0
    assert negative_baseline.emit(160, 70, True) == 0
    assert negative_baseline.emit(160, 70, False) == 0

    # zero baseline
    zero_baseline = Reducing(0,0, 0,0)
    assert zero_baseline.helper(
        zero_baseline.bad_baseline,
        zero_baseline.bad_increment) == 0
    assert zero_baseline.helper(
        zero_baseline.worst_baseline,
        zero_baseline.worst_increment) == 0
    assert zero_baseline.emit(150, 70, True) == 0
    assert zero_baseline.emit(150, 70, False) == 0


def test_temperature_panic_emit():
    # temperature == threshold
    equal_threshold = TemperaturePanic(60,70,5,7,50, 40)
    assert equal_threshold.helper(50,
                                  equal_threshold.bad_threshold,
                                  equal_threshold.bad_baseline,
                                  equal_threshold.bad_increment) == 60
    assert equal_threshold.helper(40,
                                  equal_threshold.worst_threshold,
                                  equal_threshold.worst_baseline,
                                  equal_threshold.worst_increment) == 70
    assert equal_threshold.emit(50, 55, True) == 60
    assert equal_threshold.emit(40, 55, False) == 70

    # temperature > self.threshold
    greater_than_threshold = TemperaturePanic(60, 70, 5, 7,50, 40)
    assert greater_than_threshold.helper(150,
                        greater_than_threshold.bad_threshold,
                        greater_than_threshold.bad_baseline,
                        greater_than_threshold.bad_increment) == 55
    assert greater_than_threshold.helper(150,
                         greater_than_threshold.worst_threshold,
                        greater_than_threshold.worst_baseline,
                        greater_than_threshold.worst_increment) == 63
    assert greater_than_threshold.emit(150, 60, True) == 55
    assert greater_than_threshold.emit(150, 60, False) == 63


    # temperature > self.threshold and start baseline is less than zero
    greater_than_threshold1 = TemperaturePanic(-10, -20,5, 7, 50,40)
    assert greater_than_threshold1.helper(150,
                          greater_than_threshold1.bad_threshold,
                         greater_than_threshold1.bad_baseline,
                         greater_than_threshold1.bad_increment) == 0
    assert greater_than_threshold1.helper(150,
                        greater_than_threshold1.worst_threshold,
                         greater_than_threshold1.worst_baseline,
                        greater_than_threshold1.worst_increment) == 0
    assert greater_than_threshold1.emit(150, 60, True) == 0
    assert greater_than_threshold1.emit(150, 60, False) == 0

    # temperature > self.threshold and  baseline is less than zero case
    greater_than_threshold2 = TemperaturePanic(50, 70,55, 85, 50, 40)
    assert greater_than_threshold2.helper(150,
                            greater_than_threshold2.bad_threshold,
                             greater_than_threshold2.bad_baseline,
                         greater_than_threshold2.bad_increment) == 0
    assert greater_than_threshold2.helper(150,
                            greater_than_threshold2.worst_threshold,
                            greater_than_threshold2.worst_baseline,
                            greater_than_threshold2.worst_increment) == 0
    assert greater_than_threshold2.emit(150, 60, True) == 0
    assert greater_than_threshold2.emit(150, 60, False) == 0

    # temperature < self.threshold
    more_than_threshold = TemperaturePanic(60,80,5,7 ,50, 40)
    assert more_than_threshold.helper(30,
                        more_than_threshold.bad_threshold,
                        more_than_threshold.bad_baseline,
                        more_than_threshold.bad_increment) == 60
    assert more_than_threshold.helper(30,
                        more_than_threshold.worst_threshold,
                      more_than_threshold.worst_baseline,
                        more_than_threshold.worst_increment) == 80
    assert more_than_threshold.emit(30, 65, True) == 60
    assert more_than_threshold.emit(30, 65, False) == 80


    # positive baseline
    positive_baseline = TemperaturePanic(50,70,5,7, 50, 70)
    assert positive_baseline.helper(150,
                        positive_baseline.bad_threshold,
                     positive_baseline.bad_baseline,
                        positive_baseline.bad_increment) == 45
    assert positive_baseline.helper(150,
                        positive_baseline.worst_threshold,
                        positive_baseline.worst_baseline,
                        positive_baseline.worst_increment) == 63
    assert positive_baseline.emit(150, 55, True) == 45
    assert positive_baseline.emit(150, 55, False) == 63


    # negative baseline
    negative_baseline = TemperaturePanic(-50,-86,5,7 ,60, 80)
    assert negative_baseline.helper(60,
                        negative_baseline.bad_threshold,
                        negative_baseline.bad_baseline,
                        negative_baseline.bad_increment) == -50
    assert negative_baseline.helper(60,
                        negative_baseline.worst_threshold,
                         negative_baseline.worst_baseline,
                        negative_baseline.worst_increment) == -86
    assert negative_baseline.emit(60, 60, True) == -50
    assert negative_baseline.emit(60, 60, False) == -86

    # zero baseline
    zero_baseline = TemperaturePanic(0,0,5, 7, 40, 50)
    assert zero_baseline.helper(60,
                                zero_baseline.bad_threshold,
                                 zero_baseline.bad_baseline,
                                zero_baseline.bad_increment) == 0
    assert zero_baseline.helper(60,
                                zero_baseline.worst_threshold,
                                zero_baseline.worst_baseline,
                                zero_baseline.worst_increment) == 0
    assert zero_baseline.emit(60, 65, True) == 0
    assert zero_baseline.emit(60, 65, False) == 0


def test_neighbor_average_emit():
    # country = neighbors
    equal_neighbor = NeighborAverage(50, 60, 10,15)
    assert equal_neighbor.helper(50,
                                 equal_neighbor.bad_baseline,
                                 equal_neighbor.bad_increment) == 60
    assert equal_neighbor.helper(50,
                                 equal_neighbor.worst_baseline,
                                 equal_neighbor.worst_increment) == 45
    assert equal_neighbor.emit(50, 50, True) == 60
    assert equal_neighbor.emit(50, 50, False) == 45


    #  neighbors < baseline
    less_neighbor = NeighborAverage(50, 70, 10,15)
    assert less_neighbor.helper(30,
                                less_neighbor.bad_baseline,
                                less_neighbor.bad_increment) == 40
    assert less_neighbor.helper(28,
                                less_neighbor.worst_baseline,
                                less_neighbor.worst_increment) == 55
    assert less_neighbor.emit(30, 30, True) == 40
    assert less_neighbor.emit(28, 28, False) == 55


    #  neighbors > baseline
    more_neighbor = NeighborAverage(78, 30, 10,15)
    assert more_neighbor.helper(80,
                                more_neighbor.bad_baseline,
                                more_neighbor.bad_increment) == 88
    assert more_neighbor.helper(90,
                                more_neighbor.worst_baseline,
                                more_neighbor.worst_increment) == 45
    assert more_neighbor.emit(50, 80, True) == 88
    assert more_neighbor.emit(50, 90, False) == 45

    # baseline < 0
    baseline_below_zero = NeighborAverage(-70, -90, 10, 15)
    assert baseline_below_zero.helper(50,
                                baseline_below_zero.bad_baseline,
                                baseline_below_zero.bad_increment) == 0
    assert baseline_below_zero.helper(50,
                                baseline_below_zero.worst_baseline,
                                baseline_below_zero.worst_increment) == 0
    assert baseline_below_zero.emit(50, 40, True) == 0
    assert baseline_below_zero.emit(50, 40, False) == 0


def test_social_distancing_emit():
    # temperature > upper threshold
    social = SocialDistancing(50,70,5,7, 50, 70)
    assert social.helper(150,
                         social.bad_baseline,
                         social.bad_increment) == 0
    assert social.helper(189,
                         social.worst_baseline,
                         social.worst_increment) == 0
    assert social.emit(150, 80,  True) == 0
    assert social.emit(189, 80, False) == 0


    # temperature = upper threshold
    social1 = SocialDistancing(50, 70, 5, 7, 70, 98)
    assert social1.helper(98,
                          social1.bad_baseline,
                          social1.bad_increment) == 0
    assert social1.helper(98,
                          social1.worst_baseline,
                          social1.worst_increment) == 0
    assert social1.emit(98, 80, True) == 0
    assert social1.emit(98, 80, False) == 0

    # temperature is between lower and upper threshold
    social2 = SocialDistancing(50, 70, 5, 7, 70, 98)
    assert social2.helper(80,
                          social2.bad_baseline,
                          social2.bad_increment) == 50
    assert social2.helper(91,
                          social2.worst_baseline,
                          social2.worst_increment) == 70
    assert social2.emit(80, 80, True) == 50
    assert social2.emit(91, 80, False) == 70

    # temperature == lower threshold
    social3 = SocialDistancing(50, 70, 5, 7, 70, 98)
    assert social3.helper(70,
                          social3.bad_baseline,
                          social3.bad_increment) == 50
    assert social3.helper(70,
                          social3.worst_baseline,
                          social3.worst_increment) == 70
    assert social3.emit(70, 80, True) == 50
    assert social3.emit(70, 80, False) == 70

    # temperature < lower threshold
    social4 = SocialDistancing(50, 70, 5, 7, 70, 98)
    assert social4.helper(-60,
                          social4.bad_baseline,
                          social4.bad_increment) == 55
    assert social4.helper(3, social4.worst_baseline,
                          social4.worst_increment) == 77
    assert social4.emit(-60, 80, True) == 55
    assert social4.emit(3, 80, False) == 77