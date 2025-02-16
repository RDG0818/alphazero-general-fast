import numpy, pyximport

pyximport.install(setup_args={'include_dirs': numpy.get_include()})

from alphazero.Arena import Arena
from alphazero.GenericPlayers import *
from alphazero.NNetWrapper import NNetWrapper as NNet


"""
use this script to play any two agents against each other, or play manually with
any agent.
"""
if __name__ == '__main__':
    from alphazero.envs.connect4.Connect4Game import Connect4Game as Game
    #from alphazero.envs.tafl.players import GreedyTaflPlayer
    from alphazero.envs.gobang.train import args

    args.numMCTSSims = 800
    #args.arena_batch_size = 64

    # all players
    # rp = RandomPlayer(g).play
    # gp = OneStepLookaheadConnect4Player(g).play
    # hp = HumanTaflPlayer(g).play
    g = Game
    # nnet players
    nn1 = NNet(Game, args)
    nn1.load_checkpoint('./checkpoint/hnefatafl', 'iteration-0001.pkl')
    #nn2 = NNet(Game, args)
    #nn2.load_checkpoint('./checkpoint/hnefatafl', 'iteration-0000.pkl')
    #player1 = nn1.process
    #player2 = nn2.process

    player1 = MCTSPlayer(nn1, args=args)
    #player2 = MCTSPlayer(nn2, args=args)
    #player2 = RandomPlayer()
    player2 = GreedyTaflPlayer()

    players = [player2, player1]
    arena = Arena(players, Game, use_batched_mcts=False, args=args, display=print)
    wins, draws, winrates = arena.play_game(verbose=True)
    for i in range(len(wins)):
        print(f'player{i+1}:\n\twins: {wins[i]}\n\twin rate: {winrates[i]}')
    print('draws: ', draws)
