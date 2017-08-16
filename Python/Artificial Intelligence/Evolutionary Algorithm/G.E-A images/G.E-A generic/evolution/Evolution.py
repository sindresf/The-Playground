from evolution.crossovers import *
from evolution.fitness_functions import *
from evolution.parent_selections import *
from evolution.populations import *

class Evolution(object):
    def __init__(self,conf):
        #here goes all the "direct settings" like:
        self.population_size = conf.population_size
        self.population_type = conf.population_type
        self.generation_max_try = conf.generation_max_try
        self.no_improvement_early_end = conf.no_improvement_early_end
        self.parent_selection_method = conf.parent_selection_method
        self.morphology_function = conf.morphology_function
        self.crossover = conf.crossover
        #set optional configs
        self.__set_optional_configs(conf)
        #at the end:
        self.__config_build()

    def __set_optional_configs(self,conf):
        if "speciation" in self.population_type:
            self.init_species_count = conf.opt.init_species_count
            self.max_species_count = conf.opt.max_species_count
        if "fixed_size" not in self.population_size_fixed:
            self.population_size_generation_diff_max = conf.opt.population_size_generation_diff_max
        #so on

    def __config_build(self):
        #and here goes the "select function based on setting:___"
        #and such, like:
        self.population = self.__make_population_structure()

    def __make_population_structure(self):
        if self.speciation: return speciated_population(self.population_size,self.init_species_count)

    def __choose_fitness_function(self):
        self.fitness_function = None

    def __choose_parent_selection_method(self):
        self.parent_selection = None

    def __choose_crossover_method(self):
        self.crossover_method = None