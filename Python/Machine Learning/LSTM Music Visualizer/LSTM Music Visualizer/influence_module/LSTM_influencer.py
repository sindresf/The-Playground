from influence_module.Influencer import NetworkInfluencer
from influence_module.input_output_influence_function_mapping import *
from keras.models import Sequential
from keras.layers import Dense, Activation
from keras.layers import LSTM
from keras.optimizers import RMSprop

class LSTM_influencer(NetworkInfluencer):
    def __init__(self,conf):
        #required settings
        self.structure = conf.structure
        self.input_size = conf.input_size
        self.layers = conf.layer_count
        self.multilayer = self.layers > 1
        self.layer_types = conf.layer_types
        self.layer_sizes = conf.layer_sizes
        self.layer_activations = conf.layer_activations
        self.output_size = conf.output_size
        #class settings
        self.first_layer = True
        self.last_layer = False
        self.__get_input_output_size_based_function()
        #optional settings
        opt = conf.opt
        if conf.training_enabled:
            self.training_enabled = conf.training_enabled
            self.optimizer = opt.optimizer
            self.loss_func = opt.loss_func
            self.learning_rate = opt.learning_rate

    def __get_input_output_size_based_function(self):
        i,o = self.input_size - 1, self.output_size - 1
        print("getting function at " + str(i) + "," + str(o))
        self.influence_function = i2o_func_matrix[i][o]
        print(self.influence_function)

    def __set_base_network_structure(self):
        if self.structure == "sequential":
            self.network = Sequential()
        #elif self.structure == "recurrent":
        #    self.network = Reccurent()
        #elif self.structure == "convolutional":
        #    self.network = Convolutional()
        else:
            print("no structure, going for basic Sequential")
            self.network = Sequential()

    def __get_layer(self,layer_num):
        layer_size = self.layer_sizes[layer_num]
        layer = None
        lstm = self.layer_types[layer_num] == "lstm"

        if lstm:
            if self.first_layer:
                self.first_layer = False
                if self.multilayer:
                    layer = LSTM(layer_size, return_sequences = True, input_shape=(1, self.input_size, 1))
                else:
                    layer = LSTM(layer_size, input_shape=(1,self.input_size))
            elif not self.last_layer:
                self.last_layer == (layer_num + 1) == self.layers
                layer = LSTM(layer_size, return_sequences = True)
        else:
            print("no layer match.")

        return layer


    def __get_layer_activation(self,layer_num):
        return Activation(self.layer_activations[layer_num])

    def __get_optimizer(self):
        if self.optimizer == "rmsprop":
            return RMSprop(lr=self.learning_rate)
        else:
            print("no optimizer match, RMSprop by default")
            return RMSprop(lr=self.learning_rate)

    def build(self,particle_count):
        self.particle_count = particle_count
        self.__set_base_network_structure()
        if self.multilayer:
            for l in range(self.layers):
                layer = self.__get_layer(l)
                self.network.add(layer)
                activation = self.__get_layer_activation(l)
                self.network.add(activation)
        else:
            layer = self.__get_layer(0)
            self.network.add(layer)
            activation = self.__get_layer_activation(0)
            self.network.add(activation)


        if self.training_enabled:
            self.network.compile(loss=self.loss_func, optimizer=self.__get_optimizer())
        else:
            self.network.compile()

    def shift_train(self,shift_func):
        self.train = shift_func

    def influence(self, visual_objects):
        ops,ocs = [],[]
        ips,ics = visual_objects
        for ip,ic in zip(ips,ics):
            op,oc = self.influence_function(self.network,ip,ic)
            ops.append(op)
            ocs.append(oc)
        return ops,ocs

    def influencer_info(self):
        return "LSTM. {info}"