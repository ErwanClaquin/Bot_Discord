from classForWerewolf.player import *


# =-=-=-= SEER CLASS =-=-=-= #
class BeginnerSeer(Player):
    def __init__(self, user, firstRole, botRef):
        super().__init__(user=user, firstRole=firstRole, botRef=botRef)

    async def checkingMessage(self, msg):
        self.choice = msg.content
        if self.getRoleFromDeck(position=self.choice) is not None:
            print("Succeed")
            await self.user.send(
                "Il y a " + self.getRoleFromDeck(position=self.choice).lastRole + " à la position choisie.")
            self.courseOfTheGame += ["```css\n" + self.user.name + " était l'apprentie voyante et à vu un(e) " +
                                     self.getRoleFromDeck(position=self.choice).lastRole +
                                     " à/au " + self.choice + ".```"]
        else:
            print("Failed")
            await self.user.send(
                "Erreur, impossible de trouver le rôle visé. Veuillez réessayer parmis :"
                "```gauche``````droite``````milieu```")
            await self.wait()

    async def play(self, members, centralDeck, courseOfTheGame):
        await super().play(members=members, centralDeck=centralDeck, courseOfTheGame=courseOfTheGame)

        if self.user not in ["gauche", "droite", "milieu"]:
            await self.user.send(
                "Vous êtes l'apprentie voyante. Écrivez une position parmis :```gauche``````droite``````milieu```pour"
                " voir une des cartes du deck.")
            await self.wait()

        else:
            await asyncio.sleep(random.randint(a=4, b=7))
            self.courseOfTheGame += [
                "```css\nL'apprentie voyante était à/au " + self.user + ", le rôle n'a donc pas été joué.```"]
