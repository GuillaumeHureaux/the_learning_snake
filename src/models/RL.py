# %%
from snake_ground import Ground
import numpy as np

# %%
class CustomEnvironment(Ground):

    def __init__(self, x_max, y_max):
        super().__init__(x_max, y_max)

    def states(self):
        # return {'ground': dict(type="float", shape=(25, 25)),
        #         'face': dict(type="int", shape=4,)
        # }
        return dict(type='float', shape=(25,25))

    def actions(self):
        return dict(type='int', num_values=4)

    # Optional: should only be defined if environment has a natural fixed
    # maximum episode length; otherwise specify maximum number of training
    # timesteps via Environment.create(..., max_episode_timesteps=???)
    def max_episode_timesteps(self):
        return 200

    # Optional additional steps to close environment
    def close(self):
        super().close()

    def reset(self):
        self.__init__(self.x_max, self.y_max)
        state = self.get_state()
        return state

    def execute(self, actions):
        action = {1:'up', 2:'down', 3:'left', 0:'right'}[actions]
        reward = self.step(actions)
        next_state = self.get_state()
        terminal = bool(self.flag)
        print(reward)
        return next_state, terminal, reward
    
    def close(self):
        return len(self.snake)


#%%
def run(environment, agent, n_episodes, max_step_per_episode, test=False):
    """
    Train agent for n_episodes
    """
    # environment.FlightModel.max_step_per_episode = max_step_per_episode
    # Loop over episodes
    for i in range(n_episodes):
        # Initialize episode
        episode_length = 0
        states = environment.reset()
        internals = agent.initial_internals()
        terminal = False
        while not terminal:
            # Run episode
            episode_length += 1
            actions = agent.act(states=states)
            states, terminal, reward = environment.execute(actions=actions)
            agent.observe(terminal=terminal, reward=reward)

def runner(
    environment,
    agent,
    max_step_per_episode,
    n_episodes,
    n_episodes_test=1,
    combination=1,
):
    # Train agent
    result_vec = [] #initialize the result list
    for i in range(round(n_episodes / 100)): #Divide the number of episodes into batches of 100 episodes
        if result_vec:
            print("batch", i, "Best result", result_vec[-1]) #Show the results for the current batch
        # Train Agent for 100 episode
        run(environment, agent, 100, max_step_per_episode) 
        # Test Agent for this batch
        test_results = run(
                environment,
                agent,
                n_episodes_test,
                max_step_per_episode,
                test=True
            )
        # Append the results for this batch
        result_vec.append(test_results)
    print(result_vec)
    # Plot the evolution of the agent over the batches
    # plot_multiple(
    #     Series=[result_vec],
    #     labels = ["Reward"],
    #     xlabel = "episodes",
    #     ylabel = "Reward",
    #     title = "Reward vs episodes",
    #     save_fig=True,
    #     path="env",
    #     folder=str(combination),
    #     time=False,
    # )
    #Terminate the agent and the environment
    agent.close()
    environment.close()

# %%
from tensorforce import Agent

environment = CustomEnvironment(25, 25)

# Instantiate a Tensorforce agent
agent = Agent.create(agent="ppo",environment=environment, batch_size=10)

# Call runner
runner(
    environment,
    agent,
    max_step_per_episode=1000,
    n_episodes=10000)

# %%
