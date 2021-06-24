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
        
        holder = self.ask_selection(self.holders, "holder_request", data={}, min_conf=0.65, numeric=False)
        if topping_response is not None:
            requested_toppings = join_list(self.toppings_validator(topping_response), "and")
            self.speak_dialog("icecream_with_toppings", data={
                "flavour": flavour, "toppings": requested_toppings, "holder": holder
            })
        else:
            self.speak_dialog("icecream_without_toppings", data={
                "flavour": flavour, "holder": holder
            })
        self.process_payment()

    def process_payment(self, cost=5.00):
        self.speak_dialog("total_bill")
        tip_response = self.ask_yesno("tip_request", data={})
        if tip_response == "yes":
            # An affirmative response was received
            tip = cost * 0.2
            self.speak_dialog("thank_you")
        elif tip_response == "no":
            # A negative response was received
            tip = 0
        elif tip_response is None:
            # No response was received
            tip = 0
        else:
            # tip_response == utterance
            tip = cost * 0.5
        total_cost = cost + tip

    def ask_yesno(self, prompt, data=None):
        """Read prompt and wait for a yes/no answer

        This automatically deals with translation and common variants,
        such as 'yeah', 'sure', etc.

        Args:
              prompt (str): a dialog id or string to read
              data (dict): response data
        Returns:
              string:  'yes', 'no' or whatever the user response if not
                       one of those, including None
        """
        response = self.get_response(dialog=prompt, data=data)

        if self.voc_match(response, 'yes'):
            return 'yes'
        elif self.voc_match(response, 'no'):
            return 'no'
        else:
            return response


def create_skill():
    return IcecreamShop()

