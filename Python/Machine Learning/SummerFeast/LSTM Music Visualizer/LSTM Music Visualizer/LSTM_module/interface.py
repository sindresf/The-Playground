import numpy as np
class ILSTM(object):
    """description of class
    
        a wrapper for the LSTM network,
        an interface version "built by the builder",
        based on the config,
        having just public functions for "shift training", and
        get output(input)
        ...and maybe stuff, if I can think of stuff
    """
    def __init__(self, network, config): #get the entire model from the builder
        self.layers = config.layers
        self.network = network

    def get_output(self, input):
        feature_input = self.__input_pixels_to_features([input])
        return self.__output_features_to_pixels([self.network.predict(feature_input)])

    def get_all_outputs(self,all_inputs):
        outputs = np.zeros_like(self.__input_pixels_to_features(all_inputs))
        for index, input in enumerate(all_inputs):
            outputs[index] = self.network.predict(input)
        return self.__output_features_to_pixels(outputs)

    def shift_train(self,all_inputs,shift_max_amount = 0.2): #shift given as percentage (??), should be config based
        init_output = self.get_all_outputs(all_inputs)
        shift_output = np.full_like(init_output,None,dtype=np.object)
        for index, output in enumerate(init_output):
            shift_output[index] = output.shift_by_amount(shift_max_amount)
        self.network.train(all_inputs,shift_output) #something like this is what I desire!
        #and then you just call the predict again to get the shift influenced new output

    def __input_pixels_to_features(self,inputs):
        feature_array = np.array()
        for input in inputs:
            feature_array.append(input.to_features,config.point,config.color)
        return feature_array

    def __output_features_to_pixels(self,outputs):
        pixels = np.array()
        for output in outputs:
            pixels.append(Pixel(output)) #gonna need a [0,...] conversion to what is what, based on config
        return pixels