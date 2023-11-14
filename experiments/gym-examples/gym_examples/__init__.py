from gymnasium.envs.registration import register

register(
     id="gym_examples/MultiGridWorld-v0",
     entry_point="gym_examples.envs:MultiGridWorldEnv",
     max_episode_steps=300,
)

register(
     id="gym_examples/GridWorld-v0",
     entry_point="gym_examples.envs:GridWorldEnv",
     max_episode_steps=300,
)

register(
     id="gym_examples/SpatialDesignWorld-v0",
     entry_point="gym_examples.envs:SpaDesWorldEnv",
     max_episode_steps=300,
)


