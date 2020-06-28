from chess import board, plot, rules

import matplotlib.pyplot as plt

chess_board = board.ChessBoard()
chess_rules = rules.RulesLoader.from_jsons('./pieces')

for i in range(8):
    if i not in [3, 4]:
        chess_board.add_piece((i, 1), True, chess_rules.get_rules('pawn'))
for i in range(8):
    if i not in [4]:
        chess_board.add_piece((i, 6), False, chess_rules.get_rules('pawn'))

chess_board.add_piece('a8', False, chess_rules.get_rules('rook'))
chess_board.add_piece('h8', False, chess_rules.get_rules('rook'))
chess_board.add_piece('c6', False, chess_rules.get_rules('knight'))
chess_board.add_piece('g8', False, chess_rules.get_rules('knight'))
chess_board.add_piece('c8', False, chess_rules.get_rules('bishop'))
chess_board.add_piece('f8', False, chess_rules.get_rules('bishop'))
chess_board.add_piece('d8', False, chess_rules.get_rules('queen'))
chess_board.add_piece('e8', False, chess_rules.get_rules('king'))

chess_board.add_piece('e4', True, chess_rules.get_rules('pawn'))
chess_board.add_piece('a1', True, chess_rules.get_rules('rook'))
chess_board.add_piece('h1', True, chess_rules.get_rules('rook'))
chess_board.add_piece('b1', True, chess_rules.get_rules('knight'))
chess_board.add_piece('d4', True, chess_rules.get_rules('knight'))
chess_board.add_piece('c1', True, chess_rules.get_rules('bishop'))
chess_board.add_piece('f1', True, chess_rules.get_rules('bishop'))
chess_board.add_piece('d1', True, chess_rules.get_rules('queen'))
chess_board.add_piece('e1', True, chess_rules.get_rules('king'))

chess_board.update()
fig, ax = plot.plot_chess_board(chess_board, direction=False, highlight_moves=['d4'])

plt.show()