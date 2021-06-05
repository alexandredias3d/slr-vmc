import json
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import re
import seaborn as sns

from dataclasses import dataclass

OUTPUT_PATH = '../output'  

class Abbreviations:
    
    PMC = {
        'Clustering': 'C',
        'Dynamic Threshold': 'DT',
        'Not Available': 'NA',
        'Prediction Model': 'P',
        'Static Threshold': 'ST',
    }
    
    VMS = {
        'VMs are selected individually': 'I',
        'VMs are selected as a group': 'G',
        'Not Available': 'NA',
    }

    VMP = {
        'Exact': 'E',
        'Heuristic': 'H',
        'Metaheuristic': 'MH',
        'Multi-Criteria-Decision-Making': 'MCDM',
        'Not Available': 'NA',
        'Prediction Model': 'P',
        'Random': 'R',
    }
    
    CRITERIA = {
        'Energy Consumption' : 'EC',
        'Power Consumption': 'PC',
        'Bandwidth': 'BW',
        'Not Available': 'NA',
        'Migration Cost': 'MiC',
    }
    
    METRICS = {
        'Energy Consumption': 'EC',
        'Number of VM Migrations' : 'NVMM',
        'SLA Violation (SLAV)': 'SLAV',                       
        'SLA Violation Time per Active Host (SLATAH)': 'SLATAH',    
        'Performance Degradation due to Migration (PDM)': 'PDM',                   
    }

class Table:
    
    INDEX = 'index'
    AMOUNT = 'amount'
    
    def __init__(self, path):
        self.data = pd.read_csv(path)
        

class DataExtraction(Table):
    
    PATH = '../data/form/DataExtraction.csv'
    
    PAPER_NAME = 'paper_name'
    
    #paper_authors
    #source_name
    
    KEYWORDS = 'keywords'
    
    PMC_TECHNIQUE = 'pmc_technique'
    PMC_CRITERIA = 'pmc_criteria'
    
    VMS_TECHNIQUE = 'vms_technique'
    VMS_CRITERIA = 'vms_criteria'
    VMS_AMOUNT = 'vms_amount'
    
    VMP_TECHNIQUE = 'vmp_technique'
    VMP_CRITERIA = 'vmp_criteria'
    
    EXPERIMENT_TYPE = 'experiment_type'
    EXPERIMENT_PLATFORM = 'experiment_platform'
    
    SCENARIO_DATASET = 'scenario_dataset'
    SCENARIO_PMS = 'scenario_pms'
    SCENARIO_VMS = 'scenario_vms'
    
    CONTRIBUTION = 'contribution'
    
    REFERENCE = 'reference_number'
    
    METRICS = 'used_metrics'
    IMPROVED_METRICS = 'improved_metrics'
   
    def __init__(self):
        super().__init__(DataExtraction.PATH)
        
    def get_paper_synthesis_information(self):
        return self.data[[DataExtraction.PAPER_NAME,
                          DataExtraction.REFERENCE,
                          DataExtraction.PMC_TECHNIQUE,
                          DataExtraction.VMS_TECHNIQUE,
                          DataExtraction.VMP_TECHNIQUE,
                          DataExtraction.METRICS,
                          DataExtraction.IMPROVED_METRICS]]
        
        
    def get_keywords(self):
        return self.data[DataExtraction.KEYWORDS]

    def get_pm_classification(self):
        return self.data[[DataExtraction.PMC_TECHNIQUE, 
                          DataExtraction.PMC_CRITERIA]]
    
    def get_vm_selection(self):
        return self.data[[DataExtraction.VMS_TECHNIQUE, 
                          DataExtraction.VMS_CRITERIA,
                          DataExtraction.VMS_AMOUNT]]
    
    def get_vm_placement(self):
        return self.data[[DataExtraction.VMP_TECHNIQUE, 
                          DataExtraction.VMP_CRITERIA]]
    
    def get_metrics(self):
        return self.data[DataExtraction.METRICS]
    
    def get_experiment(self):
        return self.data[[DataExtraction.EXPERIMENT_TYPE,
                          DataExtraction.EXPERIMENT_PLATFORM]]
    
    def get_scenario(self):
        return self.data[[DataExtraction.SCENARIO_DATASET,
                          DataExtraction.SCENARIO_PMS,
                          DataExtraction.SCENARIO_VMS,
                          DataExtraction.REFERENCE]]
    
    def get_contribution_and_reference(self):
        pmc = set(self.data[self.data[DataExtraction.CONTRIBUTION].str.contains('PMC')][DataExtraction.REFERENCE])
        vms = set(self.data[self.data[DataExtraction.CONTRIBUTION].str.contains('VMS')][DataExtraction.REFERENCE])
        vmp = set(self.data[self.data[DataExtraction.CONTRIBUTION].str.contains('VMP')][DataExtraction.REFERENCE])
                
        return pmc, vms, vmp
    
class QualityAssessment(Table):

    PATH = '../data/form/QualityAssessment.csv'

    ANSWER = 'answer'
    COUNT = 'count'
    TITLE = 'title'
    SCORE = 'score'
    
    QUESTION = 'Question'

    YES = 'Yes'
    NO = 'No'
    PARTIALLY = 'Partially'
    SOME = 'Some level of'
    
    def __init__(self):
        super().__init__(QualityAssessment.PATH)
        self.data = self.data.set_index(QualityAssessment.TITLE)

@dataclass(frozen=True)
class Scenario:
    BINS = 'Bins'
    
    NOT_AVAILABLE = 'Not Available'
    NA = 'N/A'
    
    INDEX = 'index'
    OCCURRENCES = 'Number of Occurrences'
    HETEROGENEITY = 'Heterogeneity'
    HETEROGENEOUS = 'Heterogeneous'
    HOMOGENEOUS = 'Homogeneous'
        
@dataclass(frozen=True)
class PMScenario(Scenario):
    
    AMOUNT = "Number of PMs"
    TYPES = "Number of PM Types"
    DISTRIBUTION = "Distribution of PMs"
    CORES = "Number of CPU Cores"
    FREQUENCY = "Frequency of CPU (in MIPS)"
    RAM = "Amount of RAM (in GB)"
    STORAGE = "Amount of Storage (in GB)"
    BANDWIDTH = "Amount of Bandwidth (in Gbps)"

@dataclass(frozen=True)
class VMScenario(Scenario):
    
    AMOUNT = "Number of VMs"
    TYPES = "Number of VM Types"
    DISTRIBUTION = "Distribution of VMs"
    CORES = "Number of CPU Cores"
    FREQUENCY = "Frequency of CPU (in MIPS)"
    RAM = "Amount of RAM (in MB)"
    STORAGE = "Amount of Storage (in GB)"
    BANDWIDTH = "Amount of Bandwidth (in Mbps)"

    
def keep_abbreviations(string):
    match = re.findall(r'\((.*?)\)', string)
    return ' + '.join(match) if match else 'NA'
    
def count_method_occurrences(df, column_name, abbreviation=False):
    pattern = re.compile(r'\((\s*\w+\s*\+?)*\)')
    
    if abbreviation:
        data = df[column_name].apply(keep_abbreviations)
    else:
        data = df[column_name].str.replace(pattern, '')

    data = (data.str.split('+')
                .explode()
                .str.strip()
                .value_counts()
                .reset_index()
                .rename(columns={Table.INDEX: column_name, column_name: Table.AMOUNT}))   
    return data

def count_criteria_occurrences(df, column_name):
    return (df[column_name]
                        .str.split(',')
                        .explode()
                        .str.strip()
                        .value_counts()
                        .reset_index()
                        .rename(columns={Table.INDEX: column_name, column_name: Table.AMOUNT}))

def create_unified_dictionary(scenario_series):
    scenario = {}
    
    for entry in scenario_series.apply(json.loads):
        for key, value in entry.items():
            try:
                if isinstance(value, list):
                    scenario[key].extend(value)
                else:
                    scenario[key].append(value)
            except:
                if isinstance(value, list):
                    scenario[key] = value
                else:
                    scenario[key] = [value]
                    
    return scenario

def count_occurrences_in_bins(scenario_series, scenario, attribute, step, remove_unused=True):
    
    series = pd.Series(scenario[attribute]).replace(Scenario.NOT_AVAILABLE, -1)
    max_value = series[series > 0].max()

    lower_bound = -step
    upper_bound = max_value + step

    bins = np.arange(lower_bound, upper_bound + step, step) 
    
    occurrences = np.zeros(len(bins) - 1, dtype='int')
    
    for entry in scenario_series.apply(json.loads):
        histogram, bin_edges = np.histogram(entry[attribute], bins)
        minimum = np.minimum(histogram, 1)
        occurrences = np.add(occurrences, minimum)
    
    bin_edges = [f'[{i}, {i + step})' for i in range(lower_bound, upper_bound, step)]
    bin_edges[0] = Scenario.NA
    bin_edges[-1] = bin_edges[-1].replace(')', ']')
    
    df = pd.DataFrame({Scenario.BINS: bin_edges, Scenario.OCCURRENCES: occurrences})
    
    if remove_unused:
        df = df[df[Scenario.OCCURRENCES] > 0]
    
    return df

def count_heterogeneity_occurrences(scenario_df, scenario):
    types = pd.Series(scenario_df[scenario]).value_counts()
    
    index = types.index
    
    homogeneous = types[index == 1].sum()
    heterogeneous = types[index >= 2].sum()
    not_available = types[index == -1].sum()

    heterogeneity = {
        Scenario.HETEROGENEITY: [Scenario.HOMOGENEOUS, Scenario.HETEROGENEOUS, Scenario.NA],
        Scenario.OCCURRENCES: [homogeneous, heterogeneous, not_available],
    }
    
    return pd.DataFrame.from_dict(heterogeneity)
    

def plot_horizontal_bar_chart(data, x, y, xlim, total, filename, xlabel='', ylabel='', remove_decimals=False, offset=1):
    sns.set_style('dark')
    
    ax = sns.barplot(data=data, x=x, y=y)
    _ = ax.set_xlabel(xlabel)
    _ = ax.set_ylabel(ylabel)
    _ = ax.set_xlim((xlim))
    _ = ax.set_xticks([])
    
    if remove_decimals:
        _ = ax.set_yticklabels([x.get_text().replace('.0', '') for x in ax.get_yticklabels()])
    
    for p in ax.patches:
        ax.annotate(f'{int(p.get_width())} ({((p.get_width() / total) * 100):.2f}%)', 
                    (offset + p.get_x() + p.get_width(), p.get_y() + (p.get_height() / 2)),
                    va='center', fontsize=12)

    ax.get_figure().savefig(f'{OUTPUT_PATH}/{filename}', bbox_inches='tight')
    
    
def read_bibtex():
    reference = '../data/reference.bib'
    
    with open(reference) as file:
        bibtex = file.read()
    
    return bibtex

def format_string(string, n=3):
    string = re.sub(r'(\{|\}|\[|\])', '', string)
    string = re.sub(rf'((\d+,\s*){{{n}}})', r'\g<1>\n', string)
    
    return string

def convert_types_to_heterogeneity(value):
    if value == 1:
        return Scenario.HOMOGENEOUS
    else:
        if value > 1:
            return Scenario.HETEROGENEOUS
        else: 
            return Scenario.NA
        
def get_papers_per_heterogeneity(df, heterogeneity):
    count = df[df[Scenario.HETEROGENEITY] == heterogeneity][DataExtraction.REFERENCE].sort_values()
    return ', '.join(count.astype(str).values)

def get_title_map():
    bibtex = read_bibtex()
    pattern = re.compile(r'@\w+\{(\w+\d+\w+),[\s\S]*?\btitle\s*=\s*\{(.*)\},')
    title_map = {paper.lower(): key for key, paper in re.findall(pattern, bibtex)}
    
    return title_map

def plot_heterogeneity_pie_chart(scenario, references, scenario_type, filename, fontsize=15, figsize=(6, 6)):
    sns.set_style('dark')

    heterogeneity_per_paper = pd.DataFrame.from_dict({
        DataExtraction.REFERENCE: references,
        Scenario.HETEROGENEITY: scenario[scenario_type],
    })

    heterogeneity_per_paper[Scenario.HETEROGENEITY] = heterogeneity_per_paper[Scenario.HETEROGENEITY].apply(convert_types_to_heterogeneity)

    heterogeneity = count_heterogeneity_occurrences(scenario, scenario_type)
    heterogeneity = heterogeneity.set_index(Scenario.HETEROGENEITY)
    plot = heterogeneity.plot.pie(y=Scenario.OCCURRENCES, autopct="%.2f%%", figsize=figsize)

    plot.get_legend().remove()
    plot.set_ylabel('')

    for child in plot.get_children():
        if isinstance(child, plt.Text):
            text = child.get_text()
            position = child.get_position()

            new_position = (1.0 if position[0] > 0 else -1.0, 0 if position[1] > 0 else -0.55)
  
            format_child = False

            papers = papers = get_papers_per_heterogeneity(heterogeneity_per_paper, text)
            if text == Scenario.HETEROGENEOUS:
                text = f'{text}\n{format_string(papers, n=4)}'
                format_child = True
            elif text == Scenario.HOMOGENEOUS:
                text = f'{text}\n{format_string(papers, n=3)}'
                new_position = (1.0 if position[0] > 0 else -1.15, position[1]) 
                format_child = True
            elif text == Scenario.NA:
                text = f'{text}\n{format_string(papers, n=4)}'
                format_child = True

            child.set_text(text)
            child.set_fontsize(fontsize)
            
            if format_child:
                child.set_position(new_position)

    plot.get_figure().savefig(f'{OUTPUT_PATH}/{filename}', bbox_inches='tight')