import retro
import numpy as np
import pandas as pd


# Hacen lista de los archivos que generaro
jugadas = []

for numeroJugada in range(27):
    jugadas.append('SonicTheHedgehog-Genesis-GreenHillZone.Act1-000000'+str(numeroJugada)+'.bk2')

for i in jugadas:
    print(i)

for n in jugadas:
    print()
    movie = retro.Movie("records/"+n)
    merge = pd.read_csv('dataset.csv', names=["data", "target"], header=None, skiprows=1)
    # Los cargan
    movie.step()
    ## Y leen otra vez el csv ,de manera tal que si se va la luz, se cae la compu, o paso algo fortuito, ustedes siguen desdel punto que quedaron
    ###vuelven a leer csv
    #pd.read_csv('dataset.csv')
    ###
    env = retro.make(
        game=movie.get_game(),
        state=None,
        # bk2s can contain any button presses, so allow everything
        use_restricted_actions=retro.Actions.ALL,
        players=movie.players,
    )
    env.initial_state = movie.get_state()
    world = np.asarray(env.reset()).reshape(-1)
    target = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
    while movie.step():
        img = np.asarray(env.render(mode='rgb_array')).reshape(-1)
        world = np.vstack((world, img))
        keys = []
        for p in range(movie.players):
            for i in range(env.num_buttons):
                keys.append(movie.get_key(i, p))
        # print(keys)
        target = np.vstack((target, keys))
        ob, rew, done, info = env.step(keys)
    
    import ipdb;ipdb.set_trace()
    
    df= pd.DataFrame(list(zip(world,target)), columns=["data","target"])
    df_2 = merge.append(df, ignore_index=True) 
    df_2.to_csv("dataset.csv")
    world = []
    target = []
    env.close()

    ### Y van a tener que investigar como se append a un dataframe usando pandas


