import alphazero.envs.chess.chess_env as chess_env
import alphazero.envs.chess.ChessLogic as ChessLogic
uci = ChessLogic.create_uci_labels()
print(len(uci))
# a = chess_env.Game()
# while True:
#     a.render()
#     move = input("Insert Move: ")
#     if move not in uci:
#         move = input("Insert Valid Move: ")
#     a.play_action(move)
#     print(a.valid_moves())
#     if True in a.win_state(): 
#         a.render()
#         break
