#!/usr/bin/env python3
import os
import sys
import numpy as np
import importlib
import tensorflow as tf

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'datasets'))


class Worker:
    def __init__(self):
        trainscript = 'train_network_tf.py'
        weights_path = 'pretrained_model_weights.h5'
        module_name = os.path.splitext(os.path.basename(trainscript))[0]
        sys.path.append('.')
        trainscript_module = importlib.import_module(module_name)

        # init the network
        model = trainscript_module.create_model()
        model.init()
        model.load_weights(weights_path, by_name=True)
        self.model = model

    def __call__(self, *args, **kwargs):
        position, velocity, phase, predictedPos, moveDirection, numParticles = \
            args[0], args[1], args[2], args[3], args[4], args[5]
        fluid_mask = (phase == 1)
        solid_mask = tf.logical_not(phase != 1)
        pos = position[fluid_mask]
        vel = velocity[fluid_mask]
        box = position[solid_mask]
        box_normals = moveDirection[solid_mask]
        pos_pred = self.step(pos, vel, box, box_normals)
        position[fluid_mask] = pos_pred
        return position

    def step(self, pos, vel, box, box_normals):
        inputs = (pos, vel, None, box, box_normals)
        pos, vel = self.model(inputs)
        return pos
