"""Executes the SNN with NEST"""

import nest
import numpy as np
import pylab

import parameters as params

class SpikingNeuralNetwork():
    """Includes everything necessary to execute a SNN with NEST."""
    def __init__(self):
        """Inits class SpikingNeuralNetwork with parameters from parameter.py."""
        # NEST options
        np.set_printoptions(precision=1)
        nest.set_verbosity('M_WARNING')
        nest.ResetKernel()
        nest.SetKernelStatus({"local_num_threads" : 1,
                              "resolution" : params.time_resolution})
        # Create input Poisson neurons
        # (are made of a Poisson generator and parrot neurons)
        self.spike_generators = nest.Create("poisson_generator",
                                            params.resolution[0]*params.resolution[1],
                                            params=params.poisson_params)
        self.neuron_pre = nest.Create("parrot_neuron",
                                      params.resolution[0]*params.resolution[1])
        # Create motor IAF neurons
        self.neuron_post = nest.Create("iaf_psc_alpha",
                                       2,
                                       params=params.iaf_params)
        # Create Output spike detector
        self.spike_detector = nest.Create("spike_detector",
                                          2,
                                          params={"withtime": True})
        # Create R-STDP synapses
        self.syn_dict = {"model": "stdp_dopamine_synapse",
                        "weight": {"distribution": "uniform",
                                   "low": params.w0_min,
                                   "high": params.w0_max}}
        self.vt = nest.Create("volume_transmitter")
        nest.SetDefaults("stdp_dopamine_synapse",
                         {"vt": self.vt[0],
                          "tau_c": params.tau_c,
                          "tau_n": params.tau_n,
                          "Wmin": params.w_min,
                          "Wmax": params.w_max,
                          "A_plus": params.A_plus,
                          "A_minus": params.A_minus})
        # Connect neurons in an all-to-all fashion
        nest.Connect(self.spike_generators,
                     self.neuron_pre,
                     "one_to_one")
        nest.Connect(self.neuron_pre,
                     self.neuron_post,
                     "all_to_all",
                     syn_spec=self.syn_dict)
        nest.Connect(self.neuron_post,
                     self.spike_detector,
                     "one_to_one")
        # Create connection handles for left and right motor neuron
        self.conn_l = nest.GetConnections(target=[self.neuron_post[0]])
        self.conn_r = nest.GetConnections(target=[self.neuron_post[1]])

    def simulate(self, dvs_data, reward):
        """Simulate the SNN (use this for training as weights are changed)."""
        # Set reward signal for left and right network
        nest.SetStatus(self.conn_l,
                       {"n": -reward})
        nest.SetStatus(self.conn_r,
                       {"n": reward})
        # Set poisson neuron firing time span
        time = nest.GetKernelStatus("time")
        nest.SetStatus(self.spike_generators,
                       {"origin": time})
        nest.SetStatus(self.spike_generators,
                       {"stop": params.sim_time})
        # Set poisson neuron firing frequency
        dvs_data = dvs_data.reshape(dvs_data.size)
        for i in range(dvs_data.size):
            rate = dvs_data[i]/params.max_spikes
            rate = np.clip(rate,0,1)*params.max_poisson_freq
            nest.SetStatus([self.spike_generators[i]], {"rate": rate})
        # Simulate network in NEST
        nest.Simulate(params.sim_time)
        # Get left and right output spikes
        n_l = nest.GetStatus(self.spike_detector,
                             keys="n_events")[0]
        n_r = nest.GetStatus(self.spike_detector,
                             keys="n_events")[1]
        # Reset output spike detector
        nest.SetStatus(self.spike_detector,
                       {"n_events": 0})
        # Get network weights
        weights_l = np.array(nest.GetStatus(self.conn_l,
                                            keys="weight")).reshape(params.resolution)
        weights_r = np.array(nest.GetStatus(self.conn_r,
                                            keys="weight")).reshape(params.resolution)
        return n_l, n_r, [weights_l, weights_r]

    def run(self, dvs_data):
        """Run the SNN (use this for testing as weights are not changed)."""
        # Set poisson neuron firing time span
        time = nest.GetKernelStatus("time")
        nest.SetStatus(self.spike_generators,
                       {"origin": time})
        nest.SetStatus(self.spike_generators,
                       {"stop": params.sim_time})
        # Set poisson neuron firing frequency
        dvs_data = dvs_data.reshape(dvs_data.size)
        for i in range(dvs_data.size):
            rate = dvs_data[i]/params.max_spikes
            rate = np.clip(rate,0,1)*params.max_poisson_freq
            nest.SetStatus([self.spike_generators[i]], {"rate": rate})
        # Run network in NEST
        nest.Prepare()
        nest.Run(params.sim_time)
        nest.Cleanup()
        # Get left and right output spikes
        n_l = nest.GetStatus(self.spike_detector,
                             keys="n_events")[0]
        n_r = nest.GetStatus(self.spike_detector,
                             keys="n_events")[1]
        # Reset output spike detector
        nest.SetStatus(self.spike_detector,
                       {"n_events": 0})
        return n_l, n_r

    def set_weights(self, weights_l, weights_r):
        """Set weights of a pretrained SNN."""
        # Translate weights into dictionary format
        w_l = []
        for w in weights_l.reshape(weights_l.size):
            w_l.append({'weight': w})
        w_r = []
        for w in weights_r.reshape(weights_r.size):
            w_r.append({'weight': w})
        # Set left and right network weights
        nest.SetStatus(self.conn_l, w_l)
        nest.SetStatus(self.conn_r, w_r)
        return
