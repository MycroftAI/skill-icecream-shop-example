from mycroft import MycroftSkill, intent_file_handler


class IcecreamShop(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)

    @intent_file_handler('shop.icecream.intent')
    def handle_shop_icecream(self, message):
        self.speak_dialog('shop.icecream')


def create_skill():
    return IcecreamShop()

