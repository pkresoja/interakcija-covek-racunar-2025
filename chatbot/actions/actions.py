from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
import requests


class ActionHelloWorld(Action):

    def name(self) -> Text:
        return "action_hello_world"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(text="Hello World from Actions!")
        return []
    
class ActionLatestMovies(Action):

    def name(self) -> Text:
        return "action_latest_movies"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        url = 'https://movie.pequla.com/api/movie'
        rsp = requests.get(url)
        movies = rsp.json()

        if len(movies) >= 3:
            bot_response = {
                "type": "movie_list",
                "data": movies[-3:]
            }
            dispatcher.utter_message(text='Here are some movies', attachment=bot_response)
        else:
            dispatcher.utter_message(text='Not enought movies found') 
        return []
    
class ActionSearchMovies(Action):

    def name(self) -> Text:
        return "action_search_movies"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        criteria=tracker.get_slot("search_criteria")

        url = 'https://movie.pequla.com/api/movie?search=' + criteria
        rsp = requests.get(url)
        movies = rsp.json()

        dispatcher.utter_message(
                text='Here are the search results for ' + criteria,
                attachment={
                "type": "movie_list",
                "data": movies
               }
            )
        return []
    
class ActionGenreList(Action):

    def name(self) -> Text:
        return "action_genre_list"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        url = 'https://movie.pequla.com/api/genre'
        rsp = requests.get(url)

        dispatcher.utter_message(
                text='Here are all the available genres:',
                attachment={
                "type": "genre_list",
                "data": rsp.json()
               }
            )
        return []

class ActionActorList(Action):

    def name(self) -> Text:
        return "action_actor_list"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        url = 'https://movie.pequla.com/api/actor'
        rsp = requests.get(url)

        dispatcher.utter_message(
                text='Here are all the available actors:',
                attachment={
                "type": "actor_list",
                "data": rsp.json()
               }
            )
        return []
    
class ActionDirectorList(Action):

    def name(self) -> Text:
        return "action_director_list"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        url = 'https://movie.pequla.com/api/director'
        rsp = requests.get(url)

        dispatcher.utter_message(
                text='Here are all the available directors:',
                attachment={
                "type": "director_list",
                "data": rsp.json()
               }
            )
        return []

class ActionExtractMovie(Action):

    def name(self) -> Text:
        return "action_extract_movie"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        criteria=tracker.get_slot("order_criteria")

        url = 'https://movie.pequla.com/api/movie?search=' + criteria
        rsp = requests.get(url)
        movies = rsp.json()

        if len(movies) > 0:
            exact_movie = movies[0]
            dispatcher.utter_message(text='Selected movie: '+ exact_movie['title'])
            return [SlotSet('movie_permalink',exact_movie['shortUrl'])]
        
        dispatcher.utter_message(text='No movie for that criteria found!') 
        return []
    
class ActionPlaceOrder(Action):

    def name(self) -> Text:
        return "action_place_order"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        permalink=tracker.get_slot("movie_permalink")        
        dispatcher.utter_message(text='Permalink: '+permalink) 
        return []