import datetime
import time
import torch
import numpy as np

from collections import deque
from constants import constants
from utils.initialize import initialize


def log(episode, scores_deque, episode_start, agent):
    print('\rEpisode {}\tAverage Score: {:.2f}\tTime: {}'.format(
        episode + 1,
        np.mean(scores_deque),
        time.time() - episode_start
    ), end='')
    torch.save(agent.actor_local.state_dict(), 'checkpoint_actor.pth')
    torch.save(agent.critic_local.state_dict(), 'checkpoint_critic.pth')


def is_training_complete(scores_deque, episode, agent):
    if np.mean(scores_deque) >= 30.0:
        print('\nEnvironment solved in {:d} episodes!\tAverage Score: {:.2f}'.format(
            episode + 1,
            np.mean(scores_deque))
        )
        torch.save(agent.actor_local.state_dict(), 'checkpoint_actor_{}.pth'.format(datetime.datetime.now()))
        torch.save(agent.critic_local.state_dict(), 'checkpoint_critic_{}.pth'.format(datetime.datetime.now()))
        return True
    return False


def train_agent(
    environment_path,
    episodes=100000,
    max_t=5000,
    qualify_window=100,
    seed=constants.SEED,
    gamma=constants.GAMMA,
    tau=constants.TAU,
    critic_lr=constants.CRITIC_LR,
    actor_lr=constants.ACTOR_LR,
    buffer_size=constants.BUFFER_SIZE,
    batch_size=constants.BATCH_SIZE,
    actor_layer_1_nodes=constants.FC1_UNITS,
    critic_layer_1_nodes=constants.FC2_UNITS,
    actor_layer_2_nodes=constants.FC1_UNITS,
    critic_layer_2_nodes=constants.FC2_UNITS,
    actor_model_path=None,
    critic_model_path=None
):
    """DDQN Algorithm
        n_episodes (int): maximum number of training episodes
        max_t (int): maximum number of timesteps per episode
        print_every (int): frequency of printing information throughout iteration """

    print('training for episodes: {} and time steps: {}'.format(episodes, max_t))

    reacherEnv, agent = initialize(
        environment_path,
        seed=seed,
        gamma=gamma,
        tau=tau,
        critic_lr=critic_lr,
        actor_lr=actor_lr,
        buffer_size=buffer_size,
        batch_size=batch_size,
        actor_layer_1_nodes=actor_layer_1_nodes,
        critic_layer_1_nodes=critic_layer_1_nodes,
        actor_layer_2_nodes=actor_layer_2_nodes,
        critic_layer_2_nodes=critic_layer_2_nodes,
        actor_model_path=actor_model_path,
        critic_model_path=critic_model_path
    )

    scores = []
    scores_deque = deque(maxlen=qualify_window)

    for episode in range(episodes):
        episode_start = time.time()
        agent.reset()
        state = reacherEnv \
            .reset_to_initial_state(train_mode=True) \
            .get_state_snapshot()
        score = 0

        for t in range(max_t):
            action = agent.act(state)

            next_state, reward, done = reacherEnv.step(action).reaction()
            agent.step(state, action, reward, next_state, done)

            score += reward
            state = next_state

            if done: break

        scores_deque.append(score)
        scores.append(score)

        log(episode, scores_deque, episode_start, agent)
        if (is_training_complete(scores_deque, episode, agent)): break
    return scores
