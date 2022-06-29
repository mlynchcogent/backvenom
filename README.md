# backvenom
multi-purpose Red Team Assessment access and exploitation framework for exploitation C2, backdooring and defense mechanism evasion purposes on restricted enviroments

# Features
- **modular**: each malware is generated with a (simple) python3 module, similar to msfconsole, which in turn, contains the handler, where the connections of the received agents will automatically arrive.
- **Dockerized**: Easy to use! Deploy server/ in any VPS, access from any device or situation!
- **Elasticsearch + Kibana**: the output of the commands executed in broadcast will be stored in the database in order to be able to analyze them or to have a holistic view on the indexed agents due to kibana, in addition, backvenom will check at each restart if it has to execute any listener indexed in the BBDD
- **Multiple Listeners**: DNS, ICMP...
- **Multiple Clients**: API, CLI, GUI, Telegram...


# State
This project is at an early stage of development. Please feel free to contact me for collaboration.

# Malware Module structure
1. MalwareHandler(ABC)
  - Handle a client connection given socket writer/reader
2. MalwareGenerator(ABC)
  -  This class generate malware and returns binary w/ given options
        
 ![image](https://user-images.githubusercontent.com/41192980/176485365-699a4ba2-1877-4b8e-8bbd-c5ffdc43d160.png)
 
