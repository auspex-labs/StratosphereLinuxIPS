<h1 align="center"> 

Slips v0.8
</h1>

Slips is a behavioral-based Python intrusion prevention system that uses machine learning to detect malicious behaviors in the network traffic. Slips was designed to focus on targeted attacks, detection of command and control channels to provide good visualisation for the analyst.
Slips is a modular software.

<h3 align="center"> 
Behavioral based Intrusion Prevention System<br><br>

Slips documentation is [here](https://stratospherelinuxips.readthedocs.io/en/develop/) <br>

[Features](#features) — [Running Slips in a Docker](#installation) — [Authors](#people-involved) - [How to contribute](#how-to-contribute)
</h3>

## Features

Slips is a Python-based intrusion prevention system that uses machine learning to detect malicious behaviors in the network traffic. Slips was designed to focus on targeted attacks, to detect of command and control channels and to provide good visualisation for the analyst. Slips is able to analyze real live traffic from the device and the large network captures in the type of a pcap files, Suricata, Zeek/Bro and Argus flows. As a result, Slips highlights suspicious behaviour and connections that needs to be deeper analyzed. 

Slips is a modular software. Each module is designed to perform a specific detection in the network traffic. Current version of Slips contains following modules:

|   module  |   description | status |
| ---| --- | :-: |
| asn | loads and finds the ASN of each IP |✅|
| geoip | finds the country and geolocation information of each IP |✅|
| https | training&test of RandomForest to detect malicious https flows |⏳|
| port scan detector | detects Horizontal and Vertical port scans |✅|
| threat Intelligence | checks if each IP is in a list of malicious IPs  |✅|
| timeline |  creates a timeline of what happened in the network based on all the flows and type of data available  |✅|
| rnn-cc-detection | detects command and control channels using recurrent neural network and the stratosphere behavioral letters |✅|
| VirusTotal | module to lookup IP address on VirusTotal |✅|
| flowalerts | module to find malicious behaviour in each flow. Current measures are: long duration of the connection, successful ssh |✅|
| RDNS | module to get and store the reverse DNS info about IPs  |✅|
| ARPScanDetector | module to check for ARP scans in ARP traffic  |✅|
| ExportingAlerts | module to export alerts to slack, STIX or suricata format |✅|
| http_analyzer | module to analyze HTTP traffic |✅|
| blocking | module to block malicious IPs connecting to the device |✅|
| flowmldetection | module to detect malicious flows using ML pretrained models |✅|
| leak_detector | module to  detect leaks of data in the traffic using YARA rules |✅|



Slips has its own console graphical user interface called Kalipso. Kalipso summarizes the detections performed by Slips in colorful graphs and tables.

Complete documentation of Slips internal architecture and instructions how to implement a new module is available here: https://stratospherelinuxips.readthedocs.io/en/develop/

## Training of machine learning models from your data

Slips can also be used in _training_ mode with traffic from the user, so that the machine learning model can be **extended** with the users' traffic to improve detection.
To use this feature you need to modify the configuration file ```slips.conf``` to add in the ```[flowmldetection]``` section:

    mode = train

And also you need to specify the label of the traffic you are adding with:

    label = normal

After this, just run slips normally in your data (interface or any input file) and the machine learning model will be updated automatically.
To use the new model, just reconfigure slips in test mode

    mode = train

## Installation

The easiest way to run Slips is inside a docker. Current version of Slips docker can analyze network captures (pcap, Zeek flows, Argus flows, etc.), but it is not able to analyze real live traffic from inside the docker. If you need to analyze the traffic from your computer, use the native version.

## How to use Slips docker from DockerHub and share files between the host and the docker:

        mkdir ~/dataset
        cp <some-place>/myfile.pcap ~/dataset
        docker run -it --rm --net=host -v ~/dataset:/StratosphereLinuxIPS/dataset stratosphereips/slips:latest
        ./slips.py -c slips.conf -f dataset/myfile.pcap

## How to build Slips docker from Dockerfile:

        cd dockeri/ubuntu-image
        docker build --no-cache -t slips -f Dockerfile .
        docker run -it --rm --net=host -v $(pwd)/../../dataset:/StratosphereLinuxIPS/dataset slips
        ./slips.py -c slips.conf -f dataset/test3.binetflow

## If you want to allow Slips inside the docker to analyze and block the traffic in your Linux host, run docker with --cap-add=NET_ADMIN. And run with -p

        docker run -it --rm --net=host --cap-add=NET_ADMIN stratosphereips/slips:latest
        ./slips.py -c slips.conf -i eno1 -p


You can now put pcap files or other flow files in the ./dataset/ folder and analyze them

## People Involved

**Founder:** Sebastian Garcia. sebastian.garcia@agents.fel.cvut.cz, eldraco@gmail.com. 

**Main authors:** Sebastian Garcia, Kamila Babayeva, Ondrej Lukas, Alya Gomaa

**Contributors:**
- Veronica Valeros
- Frantisek Strasak
- Dita Hollmannova
- Elaheh Biglar Beigi
- Maria Rigaki 
- kartik88363
- arkamar

## How to contribute
All contributors are welcomed! How you can help?

- Run Slips and report bugs and needed features, and suggest ideas
- Pull requests with a solved GitHub issue and new feature
- Pull request with a new detection module. The instructions and a template for new detection module [here](https://stratospherelinuxips.readthedocs.io/en/develop/).

## Acknowledgments
Slips was funded by the following organizations.

- NlNet Foundation. https://nlnet.nl/
- AIC Group, Czech Technical University in Prague. https://www.aic.fel.cvut.cz/
- Avast Software. https://www.avast.com/
- CESNET. https://www.cesnet.cz/
