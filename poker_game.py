import random
import itertools
import os

class Terminal:
    """OS依存の処理（主にターミナル）"""
    def __init__(self):
        if os.name == "nt":
            self.os_type = "win"
        elif os.name == "posix":
            self.os_type = "posix"
    def clear(self):
        if self.os_type == "win":
            os.system("cls")
        elif self.os_type == "posix":
            os.sutem("clear")
    
class Card:
    """カードクラス"""
    def __init__(self):
        # トランプのカード
        self.cards= [{"kind":kind,"num":num} for kind,num in itertools.product(range(1,4+1),range(1,13+1))]
        # カードのシャッフル
        random.shuffle(self.cards)
        # 最初の5枚のカードをとる
        self.hand = []
        self.take(5)
        self.sort_hand()
        # 選択した手札がない状態にする
        self.clear_selects()
        
    # カードの山から指定した枚数をとる
    def take(self,num):
        # 手札をnum枚とる
        self.hand += self.cards[:num]
        # num枚数目以降を残りカードとする
        self.cards = self.cards[num:]
        
    # 選択したカードをクリアする
    def clear_selects(self):
        self.selects = set()
    # 選択したカードの枚数を知る
    def number_of_selects(self):
        return len(self.selects)
    
    # 手札の並べ替え
    def sort_hand(self):
        for i in range(0,4):
            for j in range(i+1,5):
                if self.hand[i]["num"] > self.hand[j]["num"]:
                    tmp = self.hand[j]
                    self.hand[j] = self.hand[i]
                    self.hand[i] = tmp
        return
    
    # カードの選択
    def select_card(self,num):
        if num in self.selects:
            # 選ばれたカードの選択を解除
            self.selects.remove(num)
        else:
            # 選択されていないカードであれば選択
            self.selects.add(num)
            
    # 手札から選んだカードを削除
    def remove_card(self):
        remove_cards = []
        # 選択されたカードを選ぶ
        for n in self.selects:
            remove_cards.append(self.hand[n-1])
        # 手札から選択されたカードを削除する
        for card in remove_cards:
            self.hand.remove(card)
        return
            
    # 手札の表示    
    def show_hand(self):
        for i in range(1,5+1):
            num_string = str(i)
            if i in self.selects:
                num_string = "*" + num_string
            print("{:>5} ".format(num_string),end="")
        print()
        for card in self.hand:
            card_kind = self.get_kind(card["kind"])
            card_number = self.get_num(card["num"])
            print("[{}{:>2}]".format(card_kind,card_number),end=" ")
        print()
        
    #　カードの種類の取得
    def get_kind(self,index):
        kind = ["♠︎" , "❤️" , "♣️" , "♦️"]
        return kind[index - 1]
    
    # 数字の種類の取得
    def get_num(self,index):
        nums = ["2" , "3" , "4" , "5" , "6" , "7" , "8" , "9" , "10" , "J" , "Q" , "K" , "A"]
        return nums[index - 1]
    
    # ゲーム結果の判定
    def judge(self):
        # 判定クラスのインスタンスを生成
        judge = Judge(self.hand)
        # 結果の判定
        judge.judge()
        
class Judge:
    """ポーカーの役を判定するクラス"""
    def __init__(self,hand):
        self.hand = hand
    # フラッシュかどうかを調べる
    def judge_flush(self):
        for i in range(4):
            if  self.hand[i]["kind"] != self.hand[i+1]["kind"]:
                return False
        return True
    
    # ストレートかどうかを調べる
    def judge_straight(self):
        for i in range(4):
            if self.hand[i]["num"]+1 != self.hand[i+1]["num"]:
                return False
            return True
    
    # ストレートフラッシュかどうか調べる
    def judge_straight_flush(self):
        # ストレートであり、かつフラッシュであるかどうかを調べる
        return self.judge_flush() & self.judge_straight()
    
    # カードの数値だけを取り出す
    def det_only_number(self):
        numbers = []
        # カードから数値だけをピックアップする
        for card in self.hand:
            numbers.append(card["num"])
        return numbers
    
    # 指定した数値の重複があるかどうかを調べる
    def judge_same_card(self,same_nums):
        numbers = self.get_only_numbers()
        # カードの重複の調整
        for n in numbers:
            # それぞれの数値のダブりをカウントする
            if numbers.count(n) == same_nums:
                return True
        return False
    
    # カード内のペアの数をカウントする
    def get_pair_count(self):
        numbers = self.get_only_numbers()
        count = 0
        # ペアカードのカウント（同じカードが2回カウントされる）
        for n in numbers:
            # それぞれの数値のダブりをカウントする
            if numbers.count(n) == 2:
                count = count + 1
        # カウントの重複の解消
        count //= 2
        return count
    
    # ゲームの判定
    def judge(self):
        hand_name = "ブタ"
        score = 0
        # 役の判定
        if self.hand[0]["num"] == 9 and self.judge_straight_flush():
            # 同じ種類のカードで10、J、Q、K、Aと並んだらロイヤル・ストレート・フラッシュ
            hand_name = "ロイヤル・ストレート・フラッシュ"
            score = 10000
        elif self.judge_straight_flush():
            # 同じ種類のカードでカードが連続していたらストレート・フラッシュ
            hand_name = "ストレート・フラッシュ"
            score = 5000
        elif self.judge_same_card(4) == True:
            # 同じ数値カードが4つあったら、フォーカード
            hand_name = "フォーカード"
            score = 2500
        elif self.judge_same_card(3) == True and self.judge_same_card(2) == True:
            # 同じカードの組み合わせが3枚と2枚であれば、フルハウス
            hand_name = "フルハウス"
            score = 2000
        elif self.judge_flush():
            # カードの種類が全て同じであればフラッシュ
            hand_name = "フラッシュ"
            score = 1500
        elif self.judge_straight():
            # 番号が連続していればストレート
            hand_name = "ストレート"
            score = 1200
        elif self.judge_same_card(3) == True:
            # 同じカードが3枚あればスリーカード
            hand_name = "スリーカード"
            score =1000
        elif self.get_pair_count() == 2:
            # ペアが2組あればツーペア
            hand_name = "ツーペア"
            score = 800
        elif self.get_pair_count() == 1:
            # ペアが1組しかなければワンペア
            hand_name = "ワンペア"
            score = 100
        print("{} score:{}".format(hand_name,score))
            
    
class Poker_Game:
    """ポーカーのメイン処理を行うクラス"""
    def __init__(self):
        #　カードの初期化（シャッフルし、手札を５枚とる
        self.game_card = Card()
        #　ターミナルの生成
        self.term = Terminal()
        
    def main(self):
        # ゲームプレイのループ
        for turn in range(1,3+1):
            end_flag = self.game_main(turn)
            if end_flag == True:
                break
            self.game_end()
            return
        
        # メインのゲーム処理
        def game_main(self,turn):
            # 捨てるカードの候補
            self.game_card.clear.selectsu()
            # 捨てるカードの選択
            while True:
                self.term.clear()
                print("{}回目".format(turn))
                self.game_card.show_hand()
                n = self.input_data()
                if n >= 1 and n <= 5:
                    self .game_card.select_card(n)
                elif n == 0 or n == -1:
                    break
                else:
                    continue
            # 入れ替えるカードの枚数を取得
            change_nums = self.game_card.number_of_selects()
            print("change_nums:{}".format(change_nums))
            # カードを削除する
            self.game_card.remove_card()
            # カードを追加する
            self.game_card.take(change_nums)
            #  手札の並べ替え
            self.game_card.sort_hand()
            end_flag = False
            if n == -1:
                end_flag = True
            return end_flag
        
        # 入力処理
        def input_data(self):
            s = input("カードの選択:(1-5) 選択完了（０） 終了(e):")
            if s == "e":
                return -1
            try:
                num = int(s)
            except ValueError:
                return -2
            if num >= 0 and num <= 5:
                return num
            else:
                return -2
            
            # ゲーム終了
            def game_end(self):
                # ターミナルのクリア
                self.term.clear()
                print("ゲーム終了")
                # 手札の表示
                self.game_card.show_hand()
                # 結果の判定
                self.game_card.judge()
                
            
        
            
            
            
            
        
            
            