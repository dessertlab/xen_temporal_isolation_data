## Assessing temporal isolation in Xen

This repository contains raw data about experimental analysis on Xen and Zynq Ultrascale+ ZCU104. The results are in the paper entitled "_Temporal isolation assessment in virtualized safety-critical mixed-criticality systems: A case study on Xen hypervisor_".

Please, cite the paper if you use our results and findings for your research:

```
@article{cinque2024temporal,
	title = {Temporal isolation assessment in virtualized safety-critical mixed-criticality systems: A case study on Xen hypervisor},
	journal = {Journal of Systems and Software},
	pages = {112147},
	year = {2024},
	doi = {https://doi.org/10.1016/j.jss.2024.112147},
	author = {Marcello Cinque and Luigi {De Simone} and Daniele Ottaviano}
}
```

Follow these passages to run the tests: 

1) Run Dom0-Xen on ZCU104 board (we provided all files to be flashed on an SD card [here](https://dessert.unina.it:5551/sharing/eo0Bgxxah))

2) Setup the bridge configuration (modifying the IP if necessary)

3) Run two virtual machines as replicas (using the example configuration)

4) Configure the VM network and SSH using script_DomU (using for replica A the IP: 192.168.100.66, and for replica B the IP: 192.168.100.67)

5) Delete known hosts if needed sed -i '$ d' /home/root/.ssh/known_hosts

6) Run the script in Dom0 to start the test (input: name/number of experiments)
 
7) Save the results in your machine and analyze them 
