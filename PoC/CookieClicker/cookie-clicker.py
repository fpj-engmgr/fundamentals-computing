"""
Cookie Clicker Simulator
"""

import simpleplot
import math

# Used to increase the timeout, if necessary
import codeskulptor
codeskulptor.set_timeout(20)

import poc_clicker_provided as provided

# Constants
SIM_TIME = 10000000000.0
#SIM_TIME = 1000000.0

class ClickerState:
    """
    Simple class to keep track of the game state.
    """
    # init note:
    # _history: (time, upgrade bought, cost of upgrade, total cookies)
    #
    def __init__(self):
        self._total_cookies = 0.0
        self._current_cookies = 0.0
        self._time = 0.0
        self._cps = 1.0
        self._history = [(0.0, None, 0.0, 0.0)]
        
    def __str__(self):
        """
        Return human readable state
        """
        ret_str = "\nTime: \t\t\t" + str(self._time) + "\nCurrent Cookies:\t" + str(self._current_cookies)
        ret_str = ret_str + "\nTotal Cookies:\t\t" + str(self._total_cookies)
        ret_str = ret_str + "\nCps:\t\t\t" + str(self._cps) 
        
        return ret_str
        
    def get_cookies(self):
        """
        Return current number of cookies 
        (not total number of cookies)
        
        Should return a float
        """
        return self._current_cookies
    
    def get_cps(self):
        """
        Get current CPS

        Should return a float
        """
        return self._cps
    
    def get_time(self):
        """
        Get current time

        Should return a float
        """
        return self._time
    
    def get_history(self):
        """
        Return history list

        History list should be a list of tuples of the form:
        (time, item, cost of item, total cookies)

        For example: [(0.0, None, 0.0, 0.0)]

        Should return a copy of any internal data structures,
        so that they will not be modified outside of the class.
        """
        
        return list(self._history)

    def time_until(self, cookies):
        """
        Return time until you have the given number of cookies
        (could be 0.0 if you already have enough cookies)

        Should return a float with no fractional part
        """
        if self._current_cookies >= cookies:
            wait_time = 0.0
        else:
            wait_time = int(math.ceil((cookies - self._current_cookies)/self._cps)) * 1.0
        #
        return wait_time
        
    def wait(self, time):
        """
        Wait for given amount of time and update state

        Should do nothing if time <= 0.0
        """
        if time > 0.0:
            self._time += time
            self._total_cookies += time * self._cps
            self._current_cookies += time * self._cps
        #
    
    def buy_item(self, item_name, cost, additional_cps):
        """
        Buy an item and update state for
        _current_cookies
        _cps
        _history

        Should do nothing if you cannot afford the item
        """
        if cost <= self._current_cookies:
            self._current_cookies -= cost
            self._cps += additional_cps
            buy_record = (self._time, item_name, cost, self._total_cookies)
            self._history.append(buy_record)
   
    
def simulate_clicker(build_info, duration, strategy):
    """
    Function to run a Cookie Clicker game for the given
    duration with the given strategy.  Returns a ClickerState
    object corresponding to the final state of the game.
    """
    # make a clone of the build_info object and create a ClickerState object
    local_build_info = build_info.clone()
    clicker_state = ClickerState()
    # start the simulation loop
    current_time = clicker_state.get_time()
    #
    while current_time < duration:
        # call strategy to determine what to purchase next
        next_item = strategy(clicker_state.get_cookies(),
                             clicker_state.get_cps(),
                             clicker_state.get_history(),
                             duration - current_time,
                             local_build_info)
        # if None is returned, then we're done
        if next_item == None:
            clicker_state.wait(duration - current_time)
            break
        # get the cost of the item to be purchased and cookies on hand
        item_cost = local_build_info.get_cost(next_item)        
        # figure how long until we can buy the item
        wait_until = clicker_state.time_until(item_cost)
        # wait until we have the cookies
        if (current_time + wait_until) <= duration:
            clicker_state.wait(wait_until)
            # and get our cookies
            current_cookies = clicker_state.get_cookies()
            # keep buying this item as long as we have cookies
            while current_cookies >= item_cost:
                # buy the item
                clicker_state.buy_item(next_item,
                                       item_cost,
                                       local_build_info.get_cps(next_item))
                # update the item information
                local_build_info.update_item(next_item)
                # update our current cookies on hand
                current_cookies = clicker_state.get_cookies()
                # and the item cost, as we just update it
                item_cost = local_build_info.get_cost(next_item)
            # close the loop
        else:
            # we ran out of time, so get the last cookies and get out
            clicker_state.wait(duration - current_time)
            break
        # get the current sim time to continue the loop
        current_time = clicker_state.get_time()
        # that's the loop
    return clicker_state


def strategy_cursor_broken(cookies, cps, history, time_left, build_info):
    """
    Always pick Cursor!

    Note that this simplistic (and broken) strategy does not properly
    check whether it can actually buy a Cursor in the time left.  Your
    simulate_clicker function must be able to deal with such broken
    strategies.  Further, your strategy functions must correctly check
    if you can buy the item in the time left and return None if you
    can't.
    """
    return "Cursor"

def strategy_none(cookies, cps, history, time_left, build_info):
    """
    Always return None

    This is a pointless strategy that will never buy anything, but
    that you can use to help debug your simulate_clicker function.
    """
    return None

def strategy_cheap(cookies, cps, history, time_left, build_info):
    """
    Always buy the cheapest item you can afford in the time left.
    """
    # set lowest item cost to the max and low-cost item to None
    item_low_cost = float('inf')
    lc_item = None
    # go through the list of buildable items and find the lowest cost one
    for bld_item in build_info.build_items():
        # get the item's current cost
        item_cost = build_info.get_cost(bld_item)
        # if it's lower than the current low save the item
        if item_cost < item_low_cost:
            item_low_cost = item_cost
            lc_item = bld_item
    # check to see if we have enough time left to build this item
    if (time_left * cps) >= item_low_cost:
        # yes, so return this item
        return lc_item
    else:
        # no - return None
        return None

def strategy_expensive(cookies, cps, history, time_left, build_info):
    """
    Always buy the most expensive item you can afford in the time left.
    """
    # set highest item cost to the min and high-cost item to None
    item_high_cost = 0.0
    hc_item = None
    # go through the list of buildable items and find the highest cost one
    for bld_item in build_info.build_items():
        # get the item's current cost
        item_cost = build_info.get_cost(bld_item)
        # if it's higher that the current high save the item and fits in the time
        max_cookies = cookies + (cps * time_left)
        if ((item_cost <= max_cookies) and (item_cost > item_high_cost)):
            item_high_cost = item_cost
            hc_item = bld_item
    # check to see if we have enough time left to build this item
    return hc_item

def strategy_best(cookies, cps, history, time_left, build_info):
    """
    The best strategy that you are able to implement.
    
    Optimized strategy focuses on the maximum impact on cps per cookie
    spent for the time remaining in the simulation.
    """
    # initialize the Cookies per Second (cps) impact and the cps winner
    cps_impact = 0.0
    cps_item_cost = 0.0
    cps_item = None
    # go through the list of buildable items and find the highest impact one
    for bld_item in build_info.build_items():
        # get the items current cost
        item_cost = build_info.get_cost(bld_item)
        item_cps = build_info.get_cps(bld_item)
        # let's use cps per cookie spent as impact for right now
        item_impact = item_cps / item_cost
        # figure out the impact that the item would have
        if item_impact > cps_impact:
            cps_impact = item_impact
            cps_item_cost = item_cost
            cps_item = bld_item
    # check to see if we have enough time left to build this item
    if (time_left * cps) >= cps_item_cost:
        # yes, so return this item
        return cps_item
    else:
        # no - return None
        return None
        
def run_strategy(strategy_name, time, strategy):
    """
    Run a simulation for the given time with one strategy.
    """
    state = simulate_clicker(provided.BuildInfo(), time, strategy)
    print strategy_name, ":", state
    print state.get_history()

    # Plot total cookies over time

    # Uncomment out the lines below to see a plot of total cookies vs. time
    # Be sure to allow popups, if you do want to see it

    # history = state.get_history()
    # history = [(item[0], item[3]) for item in history]
    # simpleplot.plot_lines(strategy_name, 1000, 400, 'Time', 'Total Cookies', [history], True)

def run():
    """
    Run the simulator.
    """    
#    run_strategy(None, SIM_TIME, strategy_none)
#    run_strategy("Cursor", 15.0, strategy_cursor_broken)
#    state = simulate_clicker(provided.BuildInfo({'Cursor': [15.0, 50.0]}, 1.15), 16.0, strategy_cursor_broken)
#    print state
#    item = strategy_expensive(500000.0, 1.0, [(0.0, None, 0.0, 0.0)], 5.0, provided.BuildInfo({'A': [5.0, 1.0], 'C': [50000.0, 3.0], 'B': [500.0, 2.0]}, 1.15))
#    print "expensive item is ", item
#    # Add calls to run_strategy to run additional strategies
    run_strategy("Expensive", SIM_TIME, strategy_expensive)
#    run_strategy("Cheap", SIM_TIME, strategy_cheap)
#    run_strategy("Best", SIM_TIME, strategy_best)
    
run()
    

