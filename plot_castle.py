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
chess_board.add_piece('e8', False, chess_rules.get_rules('king'))

chess_board.add_piece('d1', True, chess_rules.get_rules('queen'))
chess_board.add_piece('a1', True, chess_rules.get_rules('rook'))
chess_board.add_piece('h1', True, chess_rules.get_rules('rook'))
chess_board.add_piece('e1', True, chess_rules.get_rules('king'))

plot.plot_chess_board(chess_board, direction=True, highlight_moves=['e1', 'e8'])

plt.show()
