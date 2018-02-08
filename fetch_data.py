import urllib.request
import json
from pynode.main import *

API_KEY = ""


class Bill:
    def __init__(self, initial_state):
        pass


class VoteTally:
    def __init__(self, initial_state):
        self.yes = initial_state['yes']
        self.no = initial_state['no']
        self.present = initial_state['present']
        self.not_voting = initial_state['not_voting']
        pass

    def set_yes(self, value):
        self.yes = value

    def get_yes(self):
        return self.yes

    def set_no(self, value):
        self.no = value

    def get_no(self):
        return self.no

    def set_present(self, value):
        self.present = value

    def get_present(self):
        return self.present

    def set_not_voting(self, value):
        self.not_voting = value

    def get_not_voting(self):
        return self.not_voting


class Party(VoteTally):
    def __init__(self, initial_state):
        VoteTally.__init__(self, initial_state)

        self.majority_position = initial_state['majority_position']

        pass

    def get_majority_position(self):
        pass


class Vote:
    def __init__(self, initial_state):

        # Populate class with data taken from JSON returned by ProPublica's Congress API request.
        # Result is one of the votes returned by a vote endpoint request.

        self.congress = initial_state['congress']
        self.session = initial_state['session']
        self.roll_call = initial_state['roll_call']
        self.chamber = initial_state['chamber']
        self.source = initial_state['source']
        self.url = initial_state['url']
        self.bill = Bill(initial_state['bill'])
        self.amendment = initial_state['amendment']
        self.question = initial_state['question']
        self.description = initial_state['description']
        self.vote_type = initial_state['vote_type']
        self.data = initial_state['date']
        self.time = initial_state['time']
        self.result = initial_state['result']
        self.democratic = Party(initial_state['democratic'])
        self.republican = Party(initial_state['republican'])
        self.independent = VoteTally(initial_state['independent'])
        self.total = VoteTally(initial_state['total'])
        self.positions = initial_state['positions']  # Replace this with positions[member_id] = {stuff}
        self.vacant_seats = initial_state['vacant_seats']

        pass

    def get_congress(self):
        pass

    def get_chamber(self):
        pass

    def get_roll_call(self):
        pass

    def get_source(self):
        pass

    def get_url(self):
        pass

    def get_bill(self):
        pass

    def get_amendment(self):
        pass

    def get_question(self):
        pass

    def get_description(self):
        pass

    def get_vote_type(self):
        pass

    def get_date(self):
        pass

    def get_time(self):
        pass

    def get_result(self):
        pass

    def get_democratic(self):
        pass

    def get_republican(self):
        pass

    def get_independent(self):
        pass

    def get_total(self):
        pass

    def get_positions(self):
        pass

    def get_vacant_seats(self):
        pass


class Member:
    def __init__(self):
        pass


def get_api_key():
    global API_KEY
    api_file = open("propublica_api_key.txt")
    API_KEY = api_file.readline()
    api_file.close()


# Chamber: "house", "senate"
def get_members(chamber):
    request_str = "https://api.propublica.org/congress/v1/115/{chamber}/members.json".format(chamber=chamber)
    request = urllib.request.Request(request_str, headers={'X-API-Key': API_KEY})
    with urllib.request.urlopen(request) as res:
        chamber_members = json.loads(res.read().decode('utf-8'))

    return chamber_members['results']


# Chamber: "both", "house", "senate"
def get_recent_votes(chamber):

    request_str = "https://api.propublica.org/congress/v1/{chamber}/votes/recent.json".format(chamber=chamber)
    request = urllib.request.Request(request_str, headers={'X-API-Key': API_KEY})
    with urllib.request.urlopen(request) as res:
        recent_votes = json.loads(res.read().decode('utf-8'))

    if recent_votes['status'] != 'OK':  # Consider doing something if API status != OK
        pass

    return recent_votes['results']


def get_vote(vote_uri):
    request = urllib.request.Request(vote_uri, headers={'X-API-Key': API_KEY})
    with urllib.request.urlopen(request) as res:
        vote_data = json.loads(res.read().decode('utf-8'))

    return vote_data


def parse_recent_votes(recent_votes):
    vote_count = recent_votes['num_results']
    vote_arr = recent_votes['votes']
    vote_data = {}

    for i in range(vote_count):
        vote_id = vote_arr[i]['roll_call']
        vote_data[vote_id] = get_vote(vote_arr[i]['vote_uri'])

        print(vote_data[vote_id])

    return vote_data

get_api_key()
parse_recent_votes(get_recent_votes("house"))


#def pynode_run():
    #members = getMembers("house")[0]['members']
    #recent_votes = parseRecentVotes(getRecentVotes("house"))

    #vote_edges = {}

    #for i in recent_votes:
    #    vote_edges[i['name']] = i

    #for i in members:
    #    graph.add_node(id=(i['first_name'] + " " + i['last_name']))


#begin_pynode(pynode_run)