import asyncio
import discord


# 1投票単位.
class VoteUnit:

    # クラス変数
    gi_vote_instance_number = 0     # 全投票数
    gi_MAX_VOTE = 10                # 同時進行できる投票数最大数
    gi_VOTE_LIFE_TIME = 12          # 投票開始から何時間有効かどうか
    gCLIENT = None
    gEMOJI = ['👍', '🏓']

    def __init__(self, channel, title, hour=6):
        if VoteUnit.gCLIENT is None:
            print("コードの先頭らへんでVoteUnit.gCLIENTを設定してください")
        self.vote_data_array = []       # 投票データの配列
        self.vote_user_array = []
        self.msg = ""
        self.channel = channel
        tmp = title.split(",")
        self.title = "\n"
        self.isEndVote = False
        count = 1
        for s in tmp:
            self.title += "{0}:".format(count) + s + "\n"
            self.vote_data_array.append(0)
            count += 1

    async def dispTitle(self):
        msg = await VoteUnit.gCLIENT.send_message(
            self.channel, self.title)
        self.setAnchorMessage(msg)
        await self.setReactions()

    async def mainLoop(self, sleepinterval_sec=1):
        while not self.isEndVote:
            print("mainloop")
            msg = await VoteUnit.gCLIENT.get_message(self.channel, self.msg.id)
            index = 0
            isModified = False
            for reaction in msg.reactions:
                reactors = await VoteUnit.gCLIENT.get_reaction_users(reaction)
                for r in reactors:
                    # ユーザーIDリスト内にIDがなければ
                    if r.id not in self.vote_user_array:
                        self.vote_user_array.append(r.id)
                        self.vote_data_array[index] += 1    # 投票数を1上げる
                        isModified = True                    # リアクションリセットフラ

                index += 1
            # 投票数表示
            await VoteUnit.gCLIENT.change_presence(
                game=discord.Game(name=self.getResultStr())
            )
            # 投票がされていたらリアクションのリセット
            if isModified:
                await self.resetReactions()
            # お休み
            await asyncio.sleep(sleepinterval_sec)

    def getResultStr(self):
        tmp = ""
        for i in self.vote_data_array:
            tmp = tmp + "{0}:".format(i)
        tmp = tmp[:-1]        # 最後の:を削除
        return tmp

    async def setReactions(self):
        msg = await VoteUnit.gCLIENT.get_message(
            self.channel, self.getAnchorMessage().id)
        count = 0
        for i in self.vote_data_array:
            if (len(VoteUnit.gEMOJI)-1) < count:
                break
            else:
                await VoteUnit.gCLIENT.add_reaction(
                    msg, VoteUnit.gEMOJI[count])
                count += 1

    async def removeReactions(self):
        try:
            await VoteUnit.gCLIENT.clear_reactions(self.msg)
        except:
            print("HTTPException or Forbidden error")

    async def resetReactions(self):
        await self.removeReactions()
        await self.setReactions()

    def endVote(self):
        self.isEndVote = True

    # 投票開始に使ったメッセージ（リアクション付き）
    def setAnchorMessage(self, msg):
        self.msg = msg

    def getAnchorMessage(self):
        return self.msg
