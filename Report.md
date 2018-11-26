# Introduction 
This repository attempts a continuous control problem by implementing DDPG algorithm.
Which is an actor-critic policy based methods to train Deep Reinforcement Agents. 

# Algorithm: [DDPG](https://arxiv.org/abs/1509.02971)
1. Randomly initialize critic network Q(s, a|θQ) and actor µ(s|θµ) 
with weights θQ and θµ.

2. Initialize target network Q' and µ' with weights: 
θQ' ← θQ, 
θµ' ← θµ

3. Initialize replay buffer R
4. for episode = 1, M do
    1. Initialize a random process N for action exploration
    2. Receive initial observation state s1
        1. for t = 1, T do
            1. Select action a(t) = µ(st|θµ) + Nt according to the current policy and 
                exploration noise
            2. Execute action at and observe reward rt and observe new state st+1
            3. Store transition (st, at, rt, st+1) in R
            4. Sample a random minibatch of N transitions (si, ai, ri, si+1) from R
            5. Update critic by minimizing the loss
            6. Update the actor policy using the sampled policy gradient
            7. Update the target networks
        2. end for
    3. end for


# Network architecture

## 1. Models

### 1.1 Actor Model (actor-target and actor-local have identical architecture)
```
Actor(
  (fc1): Linear(in_features=33, out_features=128, bias=True)
  (fc2): Linear(in_features=128, out_features=128, bias=True)
  (fc3): Linear(in_features=128, out_features=4, bias=True)
  (bn1): BatchNorm1d(128, eps=1e-05, momentum=0.1, affine=True, track_running_stats=True)
)
```

### 1.2 Critic Model (critic-target and critic-local have identical architecture)
```
Critic(
  (fcs1): Linear(in_features=33, out_features=128, bias=True)
  (fc2): Linear(in_features=132, out_features=128, bias=True)
  (fc3): Linear(in_features=128, out_features=1, bias=True)
  (bn1): BatchNorm1d(128, eps=1e-05, momentum=0.1, affine=True, track_running_stats=True)
)
```

## Hyper-parameters
```
1. BUFFER_SIZE      = int(1e5)  # replay buffer size
2. BATCH_SIZE       = 128       # minibatch size
3. GAMMA            = 0.99      # discount factor
4. TAU              = 1e-3      # for soft update of target parameters
5. ACTOR_LR         = 1e-4      # learning rate of the actor
6. CRITIC_LR        = 1e-4      # learning rate of the critic
8. FC1_UNITS        = 128       # Number of Neurons in the first hidden layer of both the actor and critic networks
9. FC2_UNITS        = 128       # Number of Neurons in the second hidden layer of both the actor and critic networks 
10. TIME_STEPS      = 10000     # Number of time-steps in an episode
```


# Reward plots
Environment solved in 387 episodes!	Average Score: 30.04


# Ideas for Future Work
DDPG Algorithms need a lot of episodes to solve environments
which means slow convergence of neural networks is a huge bottleneck.
The model trained in this example took ~3 hours to hit 30+ points 
over 300 episodes.

Previous attempts without batch-normalization had even poor 
convergence results with over 100s of episodes fed, a reward of 1 was 
hard to maintain for the network.

Gradient clipping also helped to keep the gradients from exploding as a
ReLU activation function was chosen.
