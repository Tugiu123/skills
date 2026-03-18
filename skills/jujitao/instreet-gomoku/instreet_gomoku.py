"""
InStreet 五子棋AI技能
基于极小极大搜索和Alpha-Beta剪枝
"""
import numpy as np


class GomokuAI:
    def __init__(self, board_size=15):
        self.board_size = board_size
        self.board = np.zeros((board_size, board_size), dtype=int)
        self.directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
        
        # 估值权重
        self.score_weights = {
            "live4": 10000,
            "rush4": 1000,
            "live3": 500,
            "sleep3": 100,
            "live2": 50,
            "sleep2": 10
        }
        
    def is_valid(self, x, y):
        return 0 <= x < self.board_size and 0 <= y < self.board_size and self.board[x][y] == 0
    
    def check_win(self, x, y, player):
        for dx, dy in self.directions:
            count = 1
            nx, ny = x + dx, y + dy
            while 0 <= nx < self.board_size and 0 <= ny < self.board_size and self.board[nx][ny] == player:
                count += 1
                nx += dx
                ny += dy
            nx, ny = x - dx, y - dy
            while 0 <= nx < self.board_size and 0 <= ny < self.board_size and self.board[nx][ny] == player:
                count += 1
                nx -= dx
                ny -= dy
            if count >= 5:
                return True
        return False
    
    def evaluate_pos(self, x, y, player):
        score = 0
        opponent = 3 - player
        
        for dx, dy in self.directions:
            line = []
            for i in range(-4, 5):
                nx = x + dx * i
                ny = y + dy * i
                if 0 <= nx < self.board_size and 0 <= ny < self.board_size:
                    line.append(self.board[nx][ny])
                else:
                    line.append(-1)
            
            for i in range(len(line) - 4):
                window = line[i:i+5]
                empty = window.count(0)
                self_pieces = window.count(player)
                opp_pieces = window.count(opponent)
                
                if opp_pieces > 0:
                    continue
                
                if self_pieces == 4 and empty == 1:
                    if window[0] == 0 or window[-1] == 0:
                        score += self.score_weights["live4"]
                elif self_pieces == 4:
                    score += self.score_weights["rush4"]
                elif self_pieces == 3 and empty == 2:
                    if (window[0] == 0 and window[1] == player) or (window[-1] == 0 and window[-2] == player):
                        score += self.score_weights["live3"]
                elif self_pieces == 3 and empty == 1:
                    score += self.score_weights["sleep3"]
                elif self_pieces == 2 and empty == 3:
                    if (window[0] == 0 and window[1] == player) or (window[-1] == 0 and window[-2] == player):
                        score += self.score_weights["live2"]
        
        return score
    
    def minimax(self, depth, alpha, beta, is_max, player):
        best_score = -float('inf') if is_max else float('inf')
        best_move = None
        
        if depth == 0:
            total_score = 0
            for x in range(self.board_size):
                for y in range(self.board_size):
                    if self.board[x][y] != 0:
                        total_score += self.evaluate_pos(x, y, 1) - self.evaluate_pos(x, y, 2)
            return total_score, None
        
        candidates = []
        for x in range(self.board_size):
            for y in range(self.board_size):
                if self.is_valid(x, y):
                    has_neighbor = False
                    for dx in [-2, -1, 0, 1, 2]:
                        for dy in [-2, -1, 0, 1, 2]:
                            nx, ny = x + dx, y + dy
                            if 0 <= nx < self.board_size and 0 <= ny < self.board_size and self.board[nx][ny] != 0:
                                has_neighbor = True
                                break
                        if has_neighbor:
                            break
                    if has_neighbor or (depth == self.max_depth and x == self.board_size // 2 and y == self.board_size // 2):
                        candidates.append((x, y))
        
        if not candidates:
            return 0, None
        
        for x, y in candidates:
            self.board[x][y] = player
            
            if self.check_win(x, y, player):
                score = self.score_weights["live4"] if is_max else -self.score_weights["live4"]
            else:
                next_player = 3 - player
                score, _ = self.minimax(depth-1, alpha, beta, not is_max, next_player)
            
            self.board[x][y] = 0
            
            if is_max:
                if score > best_score:
                    best_score = score
                    best_move = (x, y)
                alpha = max(alpha, best_score)
                if beta <= alpha:
                    break
            else:
                if score < best_score:
                    best_score = score
                    best_move = (x, y)
                beta = min(beta, best_score)
                if beta <= alpha:
                    break
        
        return best_score, best_move
    
    def ai_move(self, depth=4):
        self.max_depth = depth
        
        center = self.board_size // 2
        if np.sum(self.board) == 0:
            self.board[center][center] = 1
            return center, center
        
        _, (x, y) = self.minimax(depth, -float('inf'), float('inf'), True, 1)
        
        if x is not None and y is not None:
            self.board[x][y] = 1
            return x, y
        
        return None


def get_best_move(board, player=1, depth=4):
    """
    对外接口：获取最佳落子
    
    Args:
        board: 15x15二维数组，0=空, 1=黑棋, 2=白棋
        player: 1=黑棋(AI), 2=白棋
        depth: 搜索深度，默认4
    
    Returns:
        (x, y): 最佳落子坐标
    """
    ai = GomokuAI(board_size=15)
    ai.board = np.array(board)
    ai.max_depth = depth
    
    # 第一步下天元
    center = 7
    if np.sum(ai.board) == 0:
        return center, center
    
    _, (x, y) = ai.minimax(depth, -float('inf'), float('inf'), True, player)
    
    return x, y


if __name__ == "__main__":
    # 测试
    ai = GomokuAI(board_size=15)
    ai.board[7][7] = 1  # 黑棋占天元
    ai.board[7][8] = 2  # 白棋
    
    x, y = ai.ai_move(depth=4)
    print(f"最佳落子: ({x}, {y})")
