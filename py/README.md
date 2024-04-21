# Dispersive Flies Optimisation - Python Version

## Installation

### Using Docker Container

First, navigate to the **py** folder by running the following command in your terminal:

```bash
cd py/
```

Make sure you have ```.env``` file in this folder. If not then create and insert these ```ENVIRONMENT VARIABLES``` (template ```.env-dev``` can be used for this purpose; but make sure this file content is copied into ```.env``` file and all ```changethis``` values are replaced appropriately.):

```bash
REDIS_PASSWORD=******************
REDIS_PORT=6379
REDIS_HTTP_PORT=8001
REDIS_SERVER=redis
REDIS_DB=0
REDIS_EXPIRY=-1

ENVIRONMENT=local

LOG_DIR=logs/
LOG_FILE=${ENVIRONMENT}_dfo.log
ISSUE_FILE=${ENVIRONMENT}_dfo_issues.log
LOG_INTERVAL=midnight
MODE_LOG=debug
BACKUP_COUNT=7
```

Make sure you replace the ```ENVIRONMENT VARIABLES``` above with your own values.

If you have [docker](https://docs.docker.com/engine/install/) and [docker-compose](https://docs.docker.com/compose/install/) already installed, then use the following command to run the code in the docker container:

```bash
docker-compose up -d
```

The cached DFO data can be accessed/viewed via Redis Cache at [http://localhost:8001](http://localhost:8001). The default database is set to '0'. If you wish to change this, modify the ```REDIS_DB``` value in the ```ENVIRONMENT VARIABLES```. Then, incorporate this change into the URL to view the content of the desired database.

- When ```REDIS_EXPIRY``` is set to negative value, the will become permanent. If you want to expire the data by certain time, adjust this value in seconds.


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