from __future__ import print_function

import time, math
from itertools import count
from collections import namedtuple, defaultdict

# ... (code omitted for brevity)

# The engine section of the code
def get_best_move(board):
    Move = namedtuple("Move", "i j prom")

    ###############################################################################
    # Chess logic
    ###############################################################################

    Move = namedtuple("Move", "i j prom")

    class Position(namedtuple("Position", "board score wc bc ep kp")):
        """A state of a chess game
        board -- a 120 char representation of the board
        score -- the board evaluation
        wc -- the castling rights, [west/queen side, east/king side]
        bc -- the opponent castling rights, [west/king side, east/queen side]
        ep - the en passant square
        kp - the king passant square
        """

        def gen_moves(self):
            # For each of our pieces, iterate through each possible 'ray' of moves,
            # as defined in the 'directions' map. The rays are broken e.g. by
            # captures or immediately in case of pieces such as knights.
            for i, p in enumerate(self.board):
                if not p.isupper():
                    continue
                for d in directions[p]:
                    for j in count(i + d, d):
                        q = self.board[j]
                        # Stay inside the board, and off friendly pieces
                        if q.isspace() or q.isupper():
                            break
                        # Pawn move, double move and capture
                        if p == "P":
                            if d in (N, N + N) and q != ".": break
                            if d == N + N and (i < A1 + N or self.board[i + N] != "."): break
                            if (
                                    d in (N + W, N + E)
                                    and q == "."
                                    and j not in (self.ep, self.kp, self.kp - 1, self.kp + 1)
                                    # and j != self.ep and abs(j - self.kp) >= 2
                            ):
                                break
                            # If we move to the last row, we can be anything
                            if A8 <= j <= H8:
                                for prom in "NBRQ":
                                    yield Move(i, j, prom)
                                break
                        # Move it
                        yield Move(i, j, "")
                        # Stop crawlers from sliding, and sliding after captures
                        if p in "PNK" or q.islower():
                            break
                        # Castling, by sliding the rook next to the king
                        if i == A1 and self.board[j + E] == "K" and self.wc[0]:
                            yield Move(j + E, j + W, "")
                        if i == H1 and self.board[j + W] == "K" and self.wc[1]:
                            yield Move(j + W, j + E, "")

        def rotate(self, nullmove=False):
            """Rotates the board, preserving en passant, unless nullmove"""
            return Position(
                self.board[::-1].swapcase(), -self.score, self.bc, self.wc,
                119 - self.ep if self.ep and not nullmove else 0,
                119 - self.kp if self.kp and not nullmove else 0,
            )

        def move(self, move):
            i, j, prom = move
            p, q = self.board[i], self.board[j]
            put = lambda board, i, p: board[:i] + p + board[i + 1:]
            # Copy variables and reset ep and kp
            board = self.board
            wc, bc, ep, kp = self.wc, self.bc, 0, 0
            score = self.score + self.value(move)
            # Actual move
            board = put(board, j, board[i])
            board = put(board, i, ".")
            # Castling rights, we move the rook or capture the opponent's
            if i == A1: wc = (False, wc[1])
            if i == H1: wc = (wc[0], False)
            if j == A8: bc = (bc[0], False)
            if j == H8: bc = (False, bc[1])
            # Castling
            if p == "K":
                wc = (False, False)
                if abs(j - i) == 2:
                    kp = (i + j) // 2
                    board = put(board, A1 if j < i else H1, ".")
                    board = put(board, kp, "R")
            # Pawn promotion, double move and en passant capture
            if p == "P":
                if A8 <= j <= H8:
                    board = put(board, j, prom)
                if j - i == 2 * N:
                    ep = i + N
                if j == self.ep:
                    board = put(board, j + S, ".")
            # We rotate the returned position, so it's ready for the next player
            return Position(board, score, wc, bc, ep, kp).rotate()

        def value(self, move):
            i, j, prom = move
            p, q = self.board[i], self.board[j]
            # Actual move
            score = pst[p][j] - pst[p][i]
            # Capture
            if q.islower():
                score += pst[q.upper()][119 - j]
            # Castling check detection
            if abs(j - self.kp) < 2:
                score += pst["K"][119 - j]
            # Castling
            if p == "K" and abs(i - j) == 2:
                score += pst["R"][(i + j) // 2]
                score -= pst["R"][H1 if j < i else A1]
            # Promotion
            if A8 <= j <= H8:
                score += pst[prom][j] - pst["P"][j]
            return score

        def __str__(self):
            return "\n".join(
                [
                    "   +------------------------+",
                    *[
                        " %d | %s |" % (
                            8 - i,
                            " ".join(self.board[i * 16: i * 16 + 8]),
                        )
                        for i in range(8)
                    ],
                    "   +------------------------+",
                    "     a b c d e f g h",
                ]
            )

    ###############################################################################
    # Engine logic
    ###############################################################################

    def search(pos, alpha, beta, depth):
        if depth == 0:
            return pos.evaluate()

        best_score = -10000

        for move in pos.generate_moves():
            pos.make_move(move)
            score = -search(pos, -beta, -alpha, depth - 1)
            pos.undo_move()

            if score > best_score:
                best_score = score

            if best_score > alpha:
                alpha = best_score

            if alpha >= beta:
                break

        return best_score

    def go(pos, movetime):
        depth = 1
        while True:
            score = search(pos, -10001, 10001, depth)
            print("Depth:", depth, "Score:", score)
            depth += 1
            if time.time() - start > movetime / 1000:
                break
        return pv[0]

    def main():
        pos = Position(STARTPOS, 0, (True, True), (True, True), 0, 0)
        bestmove = go(pos, movetime=3000)
        print("Best Move:", bestmove)

   #return bestmove or '(none)'

print(get_best_move("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"))