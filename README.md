# Transactive Energy Service System (TESS)

The Transactive Energy Service System (TESS) is a platform to design, deploy, and operate transactive energy systems in electric utility retail environments. TESS provides retail market clearing mechanisms for peer-to-peer trading of behind-the-meter distributed energy resources based on ramping, capacity, and storage prices.

## Introduction
As the share of renewable resources grows, the marginal cost of energy resources tends to zero, and the long term average cost of energy is increasingly dominated by cost of flexibility resources, and the cost of associated capacity.  Nearly all the existing work on Transactive Energy Systems is based on the retail analogy to wholesale energy markets, which are fundamentally designed around marginal cost pricing of energy resources (and constraints on associated capacity), not on the cost of other grid services.  The goal of the Transactive Energy Service System (TESS) project to design, develop, test, and validate retail-level Transactive Energy systems that are dominated by behind-the-meter renewable energy resources and energy storage resources.  

Some of the research questions the project seeks to address include the following:
1. Is it possible to use the current model of Transactive Energy systems when the marginal cost of energy is often zero?
2. How can a Transactive system design reflect ramping and capacity costs in real time?
3. How do alternative Transactive Energy market designs affect the stability, reliability and resilience of power systems?
4. How do Transactive Energy systems compare to and work with flat rate or subscription billing in retail settings?
5. What new outcomes, features, and benefits emerge for utilities and customers who subscribe to Transactive Energy tariffs?
6. What are the economic impacts, e.g., distributional outcomes, that arise from these market design choices?

### Code Organization
|Path          | Description                                                  |
---------------|---------------------------------------------------------------
|[/agents](../master/agents)         | agent code for participation in bidding|
|[/analysis](../master/analysis)     | 'add description here'            |
|[/api](../master/api)               | Service Application directory     |
|[/cloud](../master/cloud)           | Infrastructure and container orchestration deployments configurations and templates                   |
|[/control](../master/control)       | Control Room app                  |
|[/docs](../master/docs)             | User docs                         |
|[/mobile](../master/mobile)         | Member-facing mobile              |
|[/scripts](../master/scripts)       | Database scripts                  |
|[/simulation](../master/simulation) | Simulation models                 |
|[/vendor](../master/vendor)         | 3rd party dependencies            |

### Contributing

Please read [CONTRIBUTING.md](../docs/CONTRIBUTING.md) for details on our code of conduct, and the process for submitting pull requests to us.

### Versioning

We use [SemVer](https://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/slacgismo/TESS/tags).

### Authors
* Anna Peery - [Github](https://github.com/avpeery)
* David Chassin - [Github](https://github.com/dchassin)
* Gustavo Cezar - [Github](https://github.com/gcezar)
* Jonathan Goncalves - [Github](https://github.com/jongoncalves)
* Marie-Louise Arlt - [Github](https://github.com/mlamlamla)
* Mayank Malik - [Github](https://github.com/malikmayank)
* Wan-Lin Hu - [Github](https://github.com/honeymilktea)
* Derin Serbetcioglu - [GitHub](https://github.com/derins)

### Acknowledgements

TESS is funded by the U.S. Department of Energy Office of Electricity. For more information contact Chris Irwin at christopher.irwin@hq.doe.gov.

SLAC National Accelerator Laboratory is operated for the U.S. Department of Energy by Stanford University under Contract No. DE-AC02-76SF00515.

### References

* [TESS White Paper](https://s3.us-east-2.amazonaws.com/tess.slacgismo.org/Chassin+et+al%2C+TESS+White+Paper+(2019).pdf)
* [GridLAB-D Transactive Module](https://github.com/slacgismo/gridlabd/pull/430)
* [Transactive Orderbook Design](https://github.com/slacgismo/gridlabd/blob/transactive_orderbook/transactive/Transactive%20Orderbook.ipynb)
* [Raspberry Pi Info](https://github.com/slacgismo/TESS/tree/master/edge_devices/README.md)

## Publications

1. [Arlt ML, DP Chassin, LL Kiesling, "Opening Up Transactive Systems: Introducing TESS and Specification in a Field Deployment", *Energies* **2021**, 14(13), 3970](https://www.mdpi.com/1996-1073/14/13/3970). DOI: https://doi.org/10.3390/en14133970
1. Arlt ML, DP Chassin, C Rivetta, and J Sweeney (2020): "Willingness to Pay for HVAC Operations for Automated Dispatch by Smart Home Systems", presented at the Wirtschaftsinformatik 2021, Community Workshop "Energy Informatics and Electro Mobility ICT", online, March 8, 2021.
1. Arlt ML, DP Chassin, C Rivetta, and J Sweeney (2020): "Automated Bidding in and Welfare Effects of Local Electricity Markets", Working paper, March 5, 2021. URL: https://marielouisearlt.files.wordpress.com/2021/03/wp_lems_210305.pdf.

## License
