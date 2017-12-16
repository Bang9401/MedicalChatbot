# -*- coding: utf-8 -*-
"""
Basic agent class that other complicated agent, e.g., rule-based agent, DQN-based agent.
"""

import numpy as np
import copy
import random
import json
import sys, os
sys.path.append(os.getcwd().replace("src/dialogue_system/agent",""))

from src.dialogue_system import dialogue_configuration


class Agent(object):
    def __init__(self, action_set, slot_set, disease_symptom, parameter):
        self.action_set = action_set
        self.slot_set = slot_set
        self.disease_symptom = disease_symptom
        self.parameter = parameter
        self.candidate_disease_list = []
        self.candidate_symptom_list = []
        self.agent_action = {
            "turn":1,
            "action":None,
            "request_slots":{},
            "inform_slots":{},
            "explicit_inform_slots":{},
            "implicit_inform_slots":{},
            "speaker":"agent"
        }

    def initialize(self):
        self.candidate_disease_list = []
        self.candidate_symptom_list = []
        self.agent_action = {
            "turn":None,
            "action":None,
            "request_slots":{},
            "inform_slots":{},
            "explicit_inform_slots":{},
            "implicit_inform_slots":{},
            "speaker":"agent"
        }

    def next(self, state, turn):
        # Take action based on different methods, e.g., DQN in AgentDQN, rule in AgentRule
        return self.agent_action

    def _state_to_representation(self, state):
        # TODO (Qianlong): mapping state to representation using one-hot. Including state["history"] and
        # TODO (Qianlong): state["current_slots"] of each turn.
        # （1）考虑生成一个sequence，每一个元素包含（action_rep, request_slots_rep,inform_slots_rep, explicit_inform_slots_rep,
        # implicit_slots_rep, turn_rep, current_slots_rep )
        # （2）与定电影票相同，并不考虑state中的history，只用user_action, agent_action, current_slots, 数据库查询结果，turn来
        # 生成当前的state_rep.
        # 现在使用的方法是生成一个sequence，但是sequence需要进一步处理，如LSTM， 然后再提供给。

        ###########################################################################################
        # One-hot representation for the current state using state["history"].
        ############################################################################################
        history = state["history"]
        state_rep = []
        for index in range(0, len(history), 1):
            temp_action = history[index]
            # Action rep.
            action_rep = np.zeros(len(self.action_set.keys()))
            action_rep[self.action_set[temp_action["action"]]] = 1.0

            # Request slots rep.
            request_rep = np.zeros(len(self.slot_set.keys()))
            for slot in temp_action["request_slots"].keys():
                request_rep[self.slot_set[slot]] = 1.0

            # Inform slots rep.
            inform_slots_rep = np.zeros(len(self.slot_set.keys()))
            for slot in temp_action["inform_slots"].keys():
                inform_slots_rep[self.slot_set[slot]] = 1.0

            # Explicit_inform_slots rep.
            explicit_inform_slots_rep = np.zeros(len(self.slot_set.keys()))
            for slot in temp_action["explicit_inform_slots"].keys():
                explicit_inform_slots_rep[self.slot_set[slot]] = 1.0

            # Implicit_inform_slots rep.
            implicit_inform_slots_rep= np.zeros(len(self.slot_set.keys()))
            for slot in temp_action["implicit_inform_slots"].keys():
                implicit_inform_slots_rep[self.slot_set[slot]] = 1.0

            # Turn rep.
            turn_rep = np.zeros(self.parameter["max_turn"])
            turn_rep[temp_action["turn"]-1] = 1.0

            # Current_slots rep.
            current_slots = copy.deepcopy(temp_action["current_slots"]["inform_slots"])
            current_slots.update(temp_action["current_slots"]["explicit_inform_slots"])
            current_slots.update(temp_action["current_slots"]["implicit_inform_slots"])
            current_slots.update(temp_action["current_slots"]["proposed_slots"])
            current_slots_rep = np.zeros(len(self.slot_set.keys()))
            for slot in current_slots.keys():
                current_slots_rep[self.slot_set[slot]] = 1.0

            state_rep.append(np.hstack((action_rep, request_rep, inform_slots_rep, explicit_inform_slots_rep, implicit_inform_slots_rep, turn_rep, current_slots_rep)).tolist())
        return state_rep