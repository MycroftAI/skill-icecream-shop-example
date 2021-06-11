from mycroft import MycroftSkill, intent_file_handler
from mycroft.util.format import join_list

class IcecreamShop(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)
        self.toppings = ["sprinkles", "whipped cream", "nuts", "gummy bears", "chocolate chips"]
        self.holders = ["cup", "regular cone", "waffle cone"]

    def toppings_validator(self, response):
        # Simplest validator
        # return response in self.toppings

        # A more detailed option
        requested_toppings = []
        for topping in self.toppings:
            if topping in response:
                requested_toppings.append(topping)
        print(requested_toppings)
        return requested_toppings

        # The same code as a list comprehension
        # requested-toppings = [topping if topping in response for topping in self.toppings]

    @intent_file_handler("request_icecream.intent")
    def handle_shop_icecream(self, message):
        self.speak_dialog("welcome", data={"name": "stratus"})
        flavour = message.data.get("flavour")
        topping_response = self.get_response("toppings_request",
                                             validator=self.toppings_validator,
                                             on_fail="topping_missing", num_retries=2)
        self.speak_dialog("holder_request")
        holder = self.ask_selection(self.holders, "which_one", data={}, min_conf=0.65, numeric=False)
        if topping_response is not None:
            requested_toppings = join_list(self.toppings_validator(topping_response), "and")
            self.speak_dialog("icecream_with_toppings", data={
                "flavour": flavour, "toppings": requested_toppings, "holder": holder
            })
        else:
            self.speak_dialog("icecream_without_toppings", data={
                "flavour": flavour, "holder": holder
            })


def create_skill():
    return IcecreamShop()

