# Dispersive Flies Optimisation (DFO)

## Summary
![DFO Pseudocode](docs/DFO.gif)
<p align="center"><b>Swarm behaviour in Dispersive Flies Optimisation</b></p>

Dispersive flies optimisation (DFO) is a bare-bones swarm intelligence algorithm which is inspired by the swarming behaviour of flies hovering over food sources. DFO is a simple optimiser which works by iteratively trying to improve a candidate solution with regard to a numerical measure that is calculated by a fitness function. Each member of the population, a fly or an agent, holds a candidate solution whose suitability can be evaluated by their fitness value. Optimisation problems are often formulated as either minimisation or maximisation problems.

DFO was introduced with the intention of analysing a simplified swarm intelligence algorithm with the fewest tunable parameters and components. In the first work on DFO, this algorithm was compared against a few other existing swarm intelligence techniques using error, efficiency and diversity measures. It is shown that despite the simplicity of the algorithm, which only uses agents’ position vectors at time t to generate the position vectors for time t + 1, it exhibits a competitive performance. Since its inception, DFO has been used in a variety of applications including medical imaging and image analysis as well as data mining and machine learning.

## Algorithm

![DFO Pseudocode](docs/dfo_algo.png)

## Resources
1. [Wikipedia](https://en.wikipedia.org/wiki/Dispersive_flies_optimisation)

## Citations
1. Al-Rifaie, Mohammad Majid. "[Dispersive Flies Optimisation](https://research.gold.ac.uk/id/eprint/17262/1/2014_DFO.pdf)." In 2014 federated conference on computer science and information systems, pp. 529-538. IEEE, 2014.
    ```
    @inproceedings{al2014dispersive,
        title={Dispersive flies optimisation},
        author={Al-Rifaie, Mohammad Majid},
        booktitle={2014 federated conference on computer science and information systems},
        pages={529--538},
        year={2014},
        organization={IEEE}
    }
    ```

2. Aparajeya, Prashant, Frederic Fol Leymarie, and Mohammad Majid Al-Rifaie. "[Swarm-based identification of animation key points from 2d-medialness maps](https://gala.gre.ac.uk/id/eprint/23765/7/23765%20AL-RIFAIE_Swarm-Based_Identification_of_Animation_Key_Points_2019.pdf)." In Computational Intelligence in Music, Sound, Art and Design: 8th International Conference, EvoMUSART 2019, Held as Part of EvoStar 2019, Leipzig, Germany, April 24–26, 2019, Proceedings 8, pp. 69-83. Springer International Publishing, 2019.
    ```
    @inproceedings{aparajeya2019swarm,
        title={Swarm-based identification of animation key points from 2d-medialness maps},
        author={Aparajeya, Prashant and Leymarie, Frederic Fol and Al-Rifaie, Mohammad Majid},
        booktitle={Computational Intelligence in Music, Sound, Art and Design: 8th International Conference, EvoMUSART 2019, Held as Part of EvoStar 2019, Leipzig, Germany, April 24--26, 2019, Proceedings 8},
        pages={69--83},
        year={2019},
        organization={Springer}
    }
    ```
3. Hooman, Oroojeni MJ, Mohammad Majid Al-Rifaie, and Mihalis A. Nicolaou. "[Deep neuroevolution: Training deep neural networks for false alarm detection in intensive care units](https://research.gold.ac.uk/id/eprint/24107/1/Deep%20Neuroevolution%20Training%20Deep%20Neural%20Networks%20for%20False%20Alarm%20Detection%20in%20Intensive%20Care%20Units.pdf)." In 2018 26th European Signal Processing Conference (EUSIPCO), pp. 1157-1161. IEEE, 2018.
    ```
    @inproceedings{hooman2018deep,
        title={Deep neuroevolution: Training deep neural networks for false alarm detection in intensive care units},
        author={Hooman, Oroojeni MJ and Al-Rifaie, Mohammad Majid and Nicolaou, Mihalis A},
        booktitle={2018 26th European Signal Processing Conference (EUSIPCO)},
        pages={1157--1161},
        year={2018},
        organization={IEEE}
    }
    ```