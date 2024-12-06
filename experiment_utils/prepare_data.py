from d4rl import qlearning_dataset
import numpy as np
import os
from experiment_utils.utils import load_dataset
import gym


def load_hdf5(env, replay_buffer, args=None):
    # filename = os.path.split(env.dataset_url)[-1]
    # h5path = os.path.join(D4RL_DIR, filename)

    refined_dataset = qlearning_dataset(env)

    observations = refined_dataset['observations']
    next_obs = refined_dataset['next_observations']
    actions = refined_dataset['actions']
    rewards = np.expand_dims(np.squeeze(refined_dataset['rewards']), 1)
    terminals = np.expand_dims(np.squeeze(refined_dataset['terminals']), 1)

    # if_mix = False
    # mix_rate = 0.5
    # if if_mix:
    #     env_name = env.spec.id.split('-')[0] + '-random-v2'
    #     rand_env = gym.make(env_name).unwrapped
    #     rand_dataset = qlearning_dataset(rand_env)
    #     size = max(len(rand_dataset['observations']), len(observations))
    #     size = len(rand_dataset['observations'])
    #     rand_obs = rand_dataset['observations'][: int(mix_rate * size)]
    #     rand_next_obs = rand_dataset['next_observations'][: int(mix_rate * size)]
    #     rand_actions = rand_dataset['actions'][: int(mix_rate * size)]
    #     rand_rewards = np.expand_dims(np.squeeze(rand_dataset['rewards']), 1)[: int(mix_rate * size)]
    #     rand_terminals = np.expand_dims(np.squeeze(rand_dataset['terminals']), 1)
    #
    #     observations = observations[:int((1 - mix_rate) * size)]
    #     next_obs = next_obs[:int((1 - mix_rate) * size)]
    #     actions = actions[:int((1 - mix_rate) * size)]
    #     rewards = rewards[:int((1 - mix_rate) * size)]
    #     terminals = terminals[:int((1 - mix_rate) * size)]
    #
    #     observations = np.concatenate([observations, rand_obs], axis=0)
    #     next_obs = np.concatenate([next_obs, rand_next_obs], axis=0)
    #     actions = np.concatenate([actions, rand_actions], axis=0)
    #     rewards = np.concatenate([rewards, rand_rewards], axis=0)
    #     terminals = np.concatenate([terminals, rand_terminals], axis=0)

        # for i in range(9):
        #     observations = np.concatenate([observations, rand_obs], axis=0)
        #     next_obs = np.concatenate([next_obs, rand_next_obs], axis=0)
        #     actions = np.concatenate([actions, rand_actions], axis=0)
        #     rewards = np.concatenate([rewards, rand_rewards], axis=0)
        #     terminals = np.concatenate([terminals, rand_terminals], axis=0)
        #
        # print(observations.mean(axis=0))
        # print(observations.std(axis=0))


    normalize_mean = True if args and args.get('reward_mean') else False
    normalize_std = True if args and args.get('reward_std') else False
    normalize = True if args and args.get('reward_norm') else False
    shift_reward_minzero = True if args and args.get('shift_reward_minzero') else False

    print("\nRewards stats before preprocessing")
    print('mean: {:.4f}'.format(rewards.mean()))
    print('std: {:.4f}'.format(rewards.std()))
    print('max: {:.4f}'.format(rewards.max()))
    print('min: {:.4f}'.format(rewards.min()))


    if shift_reward_minzero:
        rewards = rewards - rewards.min()

    if normalize_mean:
        rewards -= rewards.mean()

    if normalize_std:
        rewards_mean = rewards.mean()
        rewards = (rewards - rewards_mean) / rewards.std() + rewards_mean

    if normalize:
        rewards = (rewards - rewards.mean()) / rewards.std()

    print("\nRewards stats after preprocessing")
    print('mean: {:.4f}'.format(rewards.mean()))
    print('std: {:.4f}'.format(rewards.std()))
    print('max: {:.4f}'.format(rewards.max()))
    print('min: {:.4f}'.format(rewards.min()))

    dataset_size = observations.shape[0]
    
    replay_buffer._observations = observations
    replay_buffer._next_obs = next_obs
    replay_buffer._actions = actions
    replay_buffer._rewards = rewards
    replay_buffer._terminals = terminals

    replay_buffer._size = dataset_size
    replay_buffer.total_entries = dataset_size
    replay_buffer._top = replay_buffer._size

    # Work for state observations
    obs_dim = observations.shape[-1]
    low = np.array(obs_dim * [replay_buffer._ob_space.low[0]])
    high = np.array(obs_dim * [replay_buffer._ob_space.high[0]])
    replay_buffer._ob_space = gym.spaces.Box(low, high)
    replay_buffer._ob_shape = replay_buffer._ob_space.shape
    replay_buffer._observation_dim = obs_dim

    print(f'\nReplay buffer size : {replay_buffer._size}')
    print(f"obs dim            : ", observations.shape)
    print(f"action dim         : ", actions.shape)
    print(f'# terminals: {replay_buffer._terminals.sum()}')
    print(f'Mean rewards       : {replay_buffer._rewards.mean():.2f}')
    replay_buffer._top = replay_buffer._size

    # print('Number of terminals on: ', replay_buffer._terminals.sum())
