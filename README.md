## A Systematic Literature Review on Virtual Machine Consolidation

This repository contains all the input data and scripts used to create the tables and charts of the paper _"A Systematic Literature Review on Virtual Machine Consolidation"_. The goal of this repository is to provide to researchers a way to easily reproduce the results obtained in our paper. It also allows them to modify the scripts to provide new insights based on the same data.

### Paper abstract

Virtual machine consolidation has been a widely explored topic in recent years due to Cloud Data Centers' effect on global energy consumption. Thus, academia and companies made efforts to achieve green computing, reducing energy consumption to minimize environmental impact. By consolidating Virtual Machines into a fewer number of Physical Machines, resource provisioning mechanisms can shutdown idle Physical Machines to reduce energy consumption and improve resource utilization. However, there is a trade-off between reducing energy consumption while assuring the Quality of Service established on the Service Level Agreement. This work introduces a Systematic Literature Review of one year of advances in virtual machine consolidation. It provides a discussion on methods used in each step of the virtual machine consolidation, a classification of papers according to their contribution, and a quantitative and qualitative analysis of datasets, scenarios, and metrics.


### Repository structure

This repository is structured as follows:
-	The ```data``` folder contains all the input data needed to run the scripts. It provides: 
	- The images used as masks to create the wordcloud.
	- The data collected using the quality assessment and data extraction forms.
	- The paper's BibTeX that was used to create some tables for the paper.
	- The primary selection sheets. These sheets include the reason, for each paper in the time range of the study, the reason why it was included or excluded from our study based on the abstract, keywords and title. It also mentions which papers were not included due to the limitations of our university subscription.
	- The raw CSVs exported from the digital libraries and the filtered CSVs after using the PreProcessing.ipynb (which applies year filtering and duplicate removal).
-	The ```notebook``` folder stores all the scripts, which are basically several Jupyter Notebooks and a Python module (called ```utils.py```).
-	All the charts, tables and the wordcloud are saved in the ```output``` folder.

### Results

The results can be seen either by the Jupyter Notebooks inside the ```notebook``` or directly by the files inside the ```output``` folder. Following is a brief summary of the results per notebook:
-	[Quality Assessment Form](https://github.com/alexandredias3d/slr-vmc/blob/master/notebook/QualityAssesment.ipynb): provides the percentage of answers per question and the final scores of the papers.
-	[Synthesis](https://github.com/alexandredias3d/slr-vmc/blob/master/notebook/SynthesisTable.ipynb): contains a table that shows the methods used per stage of the VMC.
-	[Venn diagram](https://github.com/alexandredias3d/slr-vmc/blob/master/notebook/Venn.ipynb): provides a Venn diagram that depicts in which stages of the VMC, the proposed methods contribute to.
-	[Wordcloud](https://github.com/alexandredias3d/slr-vmc/blob/master/notebook/Wordcloud.ipynb): shows a wordcloud based of the keywords extracted from papers.
-	[Research Question 1](https://github.com/alexandredias3d/slr-vmc/blob/master/notebook/ResearchQuestion1.ipynb): shows methods and criteria used during the Physical Machine Classification (PMC).
-	[Research Question 2](https://github.com/alexandredias3d/slr-vmc/blob/master/notebook/ResearchQuestion2.ipynb): shows methods, criteria and the amount of VMs selected during the Virtual Machine Selection (VMS).
-	[Research Question 3](https://github.com/alexandredias3d/slr-vmc/blob/master/notebook/ResearchQuestion3.ipynb): shows methods and criteria used during the Virtual Machine Placement (VMP).
-	[Research Question 4](https://github.com/alexandredias3d/slr-vmc/blob/master/notebook/ResearchQuestion4.ipynb): provides insights about the type of experiment performed (analytical, simulation, real) and the platform.
-	[Research Question 5](https://github.com/alexandredias3d/slr-vmc/blob/master/notebook/ResearchQuestion5.ipynb): depicts the scenarios used to evaluate the VMC solutions such as the trace used, PM and VM configurations.
-	[Research Question 6](https://github.com/alexandredias3d/slr-vmc/blob/master/notebook/ResearchQuestion6.ipynb): shows the metrics used to assess the VMC solutions.


### How to reproduce

To run the notebooks, you will need to install Python >= 3.9 on your operating system. Pipenv is used as the packaging tool. Therefore, if it is not installed in your system run the following:
```
pip install pipenv
```

Then, clone this repository:
```
git clone https://www.github.com/alexandredias3d/slr-vmc
```

After cloning the repository, enter in the repository folder and install the dependencies with the following commands:
```
cd slr-vmc
pipenv install
```

Finally, start the Jupyter Lab server (you can also use Jupyter Notebook in this step):
```
pipenv shell
jupyter lab
```

Now you are able to open the Jupyter Notebooks to run and modify them at your will.
