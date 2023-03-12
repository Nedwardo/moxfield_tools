from src.Cards.Card import Card
from src.Cards.CardList import CardList


class ManaSources(CardList):
    def __init__(self, cards: CardList) -> None:
        super().__init__(cards.cards)
        self.land_values = [land.ritual_mana_generation() for land in self.lands()]
        self.land_values.sort(reverse=True)

        self.ritual_values = [
            ritual.ritual_mana_generation() for ritual in self.rituals()
        ]
        self.ritual_values.sort(reverse=True)
        self.rock_ritual_values = [
            rock.ritual_mana_generation() for rock in self.rocks()
        ]
        self.rock_values = [rock.mana_generated_per_turn() for rock in self.rocks()]
        self.rock_values.sort(reverse=True)

    def ritual_mana(self) -> int:
        return sum(self.ritual_values)

    def get_max_mana(self, turn: int = 0) -> int:
        return self.land_mana(turn) + self.non_land_mana(turn)

    def non_land_mana(self, turn: int = 0) -> int:
        return self.rock_mana(turn) + self.ritual_mana()

    def land_mana(self, turn: int = 0) -> int:
        land_mana_value = sum(self.land_values)
        if turn != 0:
            land_mana_value = sum(self.land_values[:turn])
        return land_mana_value

    def rock_mana(self, turn: int = 1) -> int:
        rock_mana_value = sum(self.rock_values)
        if turn > 1:
            return sum(self.rock_ritual_values)
        return rock_mana_value

    def is_castable(self, card: Card | str, turn: int = -1) -> bool:
        """Returns if a card is castable by a given turn, or castable ever

        # TODO later improvements:
            Colours of mana calculation
            tutor into ritual
            tutor for given card
            can I cast tutors?
            can I cast rituals?
            mana on board?

        Args:
            card (Card): A given card
            turn (int, optional): A give turn. Defaults to -1.

        Returns:
            bool: If the card is castable by a given turn
        """
        if isinstance(card, str):
            card = self.__getitem__(card)
        self.hand_copy = self.cards.copy()
        if card in self.hand_copy:
            self.hand_copy.remove(card)

        return self.get_max_mana(turn) > card.cmc()
