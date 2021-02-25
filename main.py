from display import Display
from simulator import Simulator
import policies

if __name__ == '__main__':
    sim = Simulator()
    sim.add_country('Atlantis', policies.Baseline(0.1, 0.2))
    sim.add_country('Omelas', policies.Reducing(5, 1, 0.1, 0.05))
    sim.add_country('Vulcan', policies.NeighborAverage(2, 1, 1, 0.2))
    sim.add_country('Arcadia', policies.TemperaturePanic(2, 1, 1, 0.2, 60, 45))
    sim.add_country('Chalion', policies.Reducing(2, 1, 0.1, 0.2))
    sim.add_country('Xanadu', policies.SocialDistancing(2, 3, 0.1, 0.2, 45, 75))
    display = Display(sim)
    display.run()