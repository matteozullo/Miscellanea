import random
import matplotlib.pyplot as plt
import numpy as np
from collections import defaultdict
from google.colab import files
import math

def initialize_kids():
    """ The function initializes the classroom with kid_0 as infected."""
    kids = ['kid_0'] + ['kid_' + str(i) for i in range(1, 21)]  # kid tag
    sick = [1] + [0 for i in range(1, 21)]  # infected yes/no
    counter = [1] + [0 for i in range(1, 21)]  # lenght of infection
    return {'kids': kids, 'sick': sick, 'counter': counter}  # output dictionary


def count_infected(probs: list):
    """ The function returns the number of infected kids"""
    return sum(probs)


def update_kids(kids: dict, n_infected: int):
    """ The function updates the health status of kids."""

    # Begin of day: Update status of healthy kids.
    for i in range(21):  # loop through kids

      # update sick kids
      if kids['counter'][i] > 0:
        kids['counter'][i] += 1

      # update healthy kids
      if kids['counter'][i] == 0:
        count = 0
        while count < n_infected:  # n independent Bern(0.02)
          p = random.random()  # generate random Unif(0,1)
          if (p <= 0.02): # probability of infection
            kids['sick'][i] = 1  # update status to sick
            kids['counter'][i] += 1  # add 1 to counter
          count += 1

    # End of day: Update status of recovered kids.
    for i in range(21):
      if kids['counter'][i] >= 4:
        kids['sick'][i] = 0
    return kids


def simulate_day1(no_runs = 10000):
  """ The function simulates day-1 spread."""
  output = []
  run = 0

  while run < no_runs:
    # initialize classroom
    kids_0 = initialize_kids()
    n_0 = count_infected(kids_0['sick'])
    # day 1
    kids_1 = update_kids(kids_0, n_0)
    no_1 = count_infected(kids_1['sick'])
    output.append(no_1)
    run += 1
  return output


def simulate_day2(no_runs = 10000):
  """ The function simulates day-2 spread."""
  output = []
  run = 0

  while run < no_runs:
    # initialize classroom
    kids_0 = initialize_kids()
    n_0 = count_infected(kids_0['sick'])
    # day 1
    kids_1 = update_kids(kids_0, n_0)
    no_1 = count_infected(kids_1['sick'])
    # day 2
    kids_2 = update_kids(kids_1, no_1)
    no_2 = count_infected(kids_2['sick'])
    output.append(no_2)
    run += 1
  return output


def simulate_epidemic(no_runs = 10000):
  """ The function simulates an epidemic."""

  length = []
  days = defaultdict(list)
  run = 0

  while run < no_runs:
  
    # initialize classroom
    kids__ = initialize_kids()
    no__ = count_infected(kids__['sick'])
    no_day = 0
    # stop epidemic when everyone's healthy again
    while no__ > 0:
      kids__ = update_kids(kids__, no__)
      no__ = count_infected(kids__['sick'])
      no_day += 1  # add to counter
      days[str(no_day)].append(no__)

    # save output
    length.append(no_day)
    run += 1
  
  # fill in 0s for missing days (epidemic ends at different times but arrays must have equal length!)
  for day, values in days.items():
    days[day] = values + [0 for i in range(no_runs - len(values))]

  return length, days


def expected_value(cases: list):
  return sum([cases.count(x_i)/len(cases)*x_i for x_i in set(cases)])


def plot_cases(cases: list, xlab :str, file_name: str):
  """ The function returns the pdf of number of cases."""
  plt.hist(cases, density=True, bins = list(set(cases)))
  plt.ylabel('Frequency')
  plt.xlabel(xlab)
  plt.savefig(file_name)
  files.download(file_name)
  return plt.show()
  
# set parameters
DAYS_INCUB = 2 + 1  # days of incubation (add 1 b/c counter starts at 1)
SICK_SPELL = [7,9]  # length of infection (mode and median of lognormal)
SOCIAL = [[8,10], [4,5]]  # number of social interactions w/o and w/ social distancing (mode and median of lognormals)
PROBS = [0.8,0.7,0.5,0.4]  # probabilities of infection when meeting sick
PROB_DEATH = 0.02  # probability of dying when infected
VAX_RATE = 0.01  # rate of vaccination as % of population
VAX_BETWEEN = 15  # days between 1st and 2nd injection
VAX_LAG = 10  # days between injection and immunity


def logN(mode_med: list) -> int:
  """
  Samples from a lognormal and floors.

  :param mode: mode of lognormal distribution
  :param median: median of lognormal distribution
  :return: floored lognormal(mu, sigma) observation
  """
  mode, median = mode_med
  assert mode < median, "Mode might not be greater than the median. Set the parameters accordingly."

  mu = math.log(median)  # mu parameter
  sigma = math.sqrt(mu-math.log(mode))  # sigma parameter
  return math.floor(np.random.lognormal(mu, sigma))


def initialize_population(n: int, n_sick: int) -> dict:
  """
  Initializes a population.

  :param n: number of individuals
  :param n__: number of sick individuals
  :return: dictionary with individual features
  """

  # infection
  id = ['id_' + str(i) for i in range(n)]  # IDs
  sick = [1 for i in range(n_sick)] + [0 for i in range(n-n_sick)]  # status {'healthy': 0, , 'sick': 1, 'recovered': 2, 'dead': 3}
  sick_counter = [DAYS_INCUB + 1 for i in range(n_sick)] + [0 for i in range(n-n_sick)]  # days from infection 
  dead = [0 for i in range(n)]  # dead dummy
  sick_spell = [logN(SICK_SPELL) for i in range(n_sick)] + [0 for i in range(n-n_sick)]  # length of infection

  # vaccine
  vax = [0 for i in range(n)]  # vaccine {'no': 0, '1st dose': 1, '2nd dose': 2}
  vax1_counter = [0 for i in range(n)]  # days from 1st dose
  vax2_counter = [0 for i in range(n)]  # days from 2nd dose

  # policies
  mask = [0 for i in range(n)]  # masking dummy
  socdist = [0 for i in range(n)]  # social distancing dummy

  keys = ['id', 'sick', 'sick_counter', 'sick_spell', 'vax', 'vax1_counter', 'vax2_counter', 'dead', 'mask', 'socdist']
  
  return {k:v for k,v in locals().items() if k in keys}


def count_sick(sick: list) -> int:
  """
  Counts number of sick individuals.
  """
  return int(len([i for i in sick if i == 1]))


def subset_population(pop: dict):
  """
  Returns lists of indexes for the different health status.
  """

  idx_healthy, idx_incubation, idx_recovered, idx_dead, idx_sick = [], [], [], [], []

  # extract features
  ids = [i for i in range(len(pop['id']))]
  statuses = [s for s in pop['sick']]
  counters = [c for c in pop['sick_counter']]

  # subset
  for idx, status, counter in zip(ids, statuses, counters):
    if (status == 0): idx_healthy.append(idx)
    elif (status == 1) and (counter <=DAYS_INCUB): idx_incubation.append(idx)
    elif (status == 2): idx_recovered.append(idx)
    elif (status == 3): idx_dead.append(idx)
    else: idx_sick.append(idx)

  return idx_healthy, idx_incubation, idx_recovered, idx_dead, idx_sick


def calculate_conditional(pop: dict, idx: int) -> float:
  """
  Returns the conditional probability of an infection given a contact with a carrier.

  :param pop: dictionary holding population
  :param idx: individual index
  :return: probability of infection
  """

  # extract individual features
  status = [pop['mask'][idx],  # masking
            pop['vax'][idx],  # vaccine dummy
            pop['vax1_counter'][idx] > VAX_LAG,  # more than 10 days from 1st vaccine
            pop['vax2_counter'][idx] > VAX_LAG]  # more than 10 days from 1st vaccine

  # calculate probability
  if status == ([1,0,0,0] or [1,1,0,0]):  p = PROBS[1] # masking  
  elif status == ([1,1,1,0] or [0,1,1,0]):  p = PROBS[3] # vaccine 1st dose
  elif status == ([1,1,2,0] or [1,1,2,0]):  p = PROBS[3] # vaccine 2nd dose (not yet immune)
  elif status == ([0,1,2,1] or [1,1,2,1]):  p = PROBS[2] # vaccine 2nd dose
  else: p = PROBS[0]
  return p


def day_report(sick__: list, sick: list) -> list:
  """
  Returns a summary of new cases, deaths, and recovered patients.

  :param pop__: population at prior time-period
  :param pop: population at current time-period
  :return: list holding summary stats 
  """
  cases, recovered, deaths = 0,0,0

  # for each individual
  for before, after in zip(sick__, sick):
    # if before-after statuses differ
    if before != after:
      if after == 3: deaths += 1
      if after == 2: recovered += 1
      if after == 1: cases += 1
  return [cases, recovered, deaths]


def update_population(pop: dict, masking: int, socdist: int) -> dict:
  """
  Updates the population for the next time-period.

  :param pop: population
  :param p_death: probability of death conditional on infection
  :param masking: mask-wearing dummy
  :param socdist: social distancing dummy
  :return: updated population
  """

  # containment policies
  for idx in range(len(pop['id'])):
    pop['mask'][idx] = 1 if masking else 0
    pop['socdist'][idx] = 1 if socdist else 0
  
  # subset population
  idx_healthy, idx_incubation, idx_recovered, idx_dead, idx_sick = subset_population(pop)
  
  # calculate probabilities
  p1 = len(idx_incubation + idx_sick)/len(idx_healthy + idx_recovered + idx_incubation + idx_sick)  # P(meeting someone sick)
  p3 = PROB_DEATH  # P(death | infection)
  print(len(idx_healthy))

  # update healthy

  # for each individual
  for idx in idx_healthy:

    # number of social interactions depends on social distancing
    social = logN(SOCIAL[0]) if pop['socdist'][idx] == 0 else logN(SOCIAL[1])
    # for each interaction, Bernoulli(p) trials with prob p1 of meeting someone sick
    s = 0
    while s < social:
      s += 1
      # if meets someone sick
      if random.random() <= p1:
        # if gets infected
        p2 = calculate_conditional(pop, idx)  # P(infection | meeting someone sick)
        if random.random() <= p2:
          pop['sick'][idx] += 1  # update status to sick
          pop['sick_counter'][idx] += 1  # update counter
          pop['sick_spell'][idx] == logN(SICK_SPELL)  # assign length of infection
          pop['dead'][idx] == 1 if random.random() <= p3 else 0  # assign fatality with prob p3

          # stop Bernoulli trials if gets infected
          break


  # update sick

  # for each individual
  for idx in idx_sick + idx_incubation:
    pop['sick_counter'][idx] += 1

    # if last day of infection
    if pop['sick_counter'][idx] == (pop['sick_spell'][idx] + DAYS_INCUB + 1):
      # dies
      if (pop['dead'][idx] == 1): pop['sick'][idx] += 2  
      # recovers
      else: pop['sick'][idx] += 1
  
  return pop


def vaccine_update(pop: dict, vax_n: int, vax_strategy: int = 0)  -> dict:
  """
  Updates the vaccine rollout.
  Two rollout strategies are possible, maximizing first dose injections or second dose injections.

  :param pop: population
  :param vax_n: number of vaccines / day
  :param days_between: days between 1st and 2nd dose
  :param vax_strategy: vaccine strategy dummy (1 if prioritize first dose, else complete vaccination)
  :return: updated population
  """

  # vaccines require individuals not to be sick
  # 2nd dose eligible
  idx_elig2 = [idx for idx in range(len(pop['id'])) if (pop['sick'][idx]==0) and (pop['vax1_counter'][idx]> VAX_BETWEEN)]
  # 1st dose eligible
  idx_elig1 = [idx for idx in range(len(pop['id'])) if (pop['sick'][idx]==0) and (pop['vax'][idx]==0)]

  # prioritization
  idx_elig = idx_elig2 + idx_elig1 if vax_strategy == 0 else idx_elig1 + idx_elig2

  # rollouts
  idx_injections = idx_elig[:vax_n]
  for idx in idx_injections:
    pop['vax'][idx] += 1
  
  # update counters
  # for each individual
  for idx in range(len(pop['id'])):
    # if vaccinated, update counters
    if pop['vax'][idx] > 0:
      if pop['vax'][idx] == 2: pop['vax2_counter'][idx] += 1
      if pop['vax'][idx] == 1: pop['vax1_counter'][idx] += 1       
  return pop


def simulate_pandemic(day_stop: int = 365, day_vax: int = 100):
  """
  Simulates a pandemic and returns daily cases, death tolls, and recoveries.

  :param day_stop: day simulation ends
  :param day_vax: day of vaccine distribution
  :param vax_rate: percent of population vaccinated / day
  :return: records
  """

  assert day_stop > day_vax, "Vaccine must be distributed before simulation ends."

  # initialize population
  population = initialize_population(10000, 100)
  n_pop = len(population['id'])
  n = count_sick(population['sick'])
  
  # initialize counters
  day = 0
  days, cases, recovered, deaths = [0],[n],[0],[0]

  # until vaccine
  while (day < day_vax) and (n > 0):
    day += 1

    # sick at begin
    sick__ = [s for s in population['sick']]

    # update population
    population = update_population(population, masking = 1, socdist = 1)
    sick = [s for s in population['sick']]
    n = count_sick(population['sick'])

    # update records
    c, r, d = day_report(sick__, sick)
    days.append(day)
    cases.append(c)
    recovered.append(r)
    deaths.append(d)

  
  # after vaccine
  vax_n = math.floor(VAX_RATE * n_pop)  # vaccines per day

  # until end or no more sick individuals
  while (day < day_stop) and (n > 0):
    day += 1

    # sick at begin
    sick__ = [s for s in population['sick']]

    # update vaccines
    population = vaccine_update(population, vax_n, vax_strategy = 0)

    # update population
    population = update_population(population, masking = 1, socdist = 1)
    sick = [s for s in population['sick']]
    n = count_sick(population['sick'])

    # update records
    c, r, d = day_report(sick__, sick)
    days.append(day)
    cases.append(c)
    recovered.append(r)
    deaths.append(d)

  return days, cases, recovered, deaths
  
# simulate day I
day_1 = simulate_day1()  # day 1 simulation
plot_cases(day_1, "Number of cases", "day_1_hist.png")  # plot PDF

print("\n")
print("Here's the event set with associated probabilities:")
print("p = 0, if x = 0")
for x_i in set(day_1):
  p_i = day_1.count(x_i)/len(day_1)
  print("p = {}, if x = {}".format(x_i, p_i))
print("p = 0, otherwise")

# expected number of infections day I
E_X = expected_value(day_1)
print("The expected value is {}.".format(E_X))

# expected number of infections day II
day_2 = simulate_day2()  # day 1 simulation
E_X = expected_value(day_2)
print("The expected value is {}.".format(E_X))

# length of pandemic
length, days = simulate_epidemic()
plot_cases(length, "Length (Days)", "pandemic_len.png")  # plot PDF

print("Expected values for each day:")
for day, values in days.items():
  E_X = expected_value(values)
  print("E[x={}] = {}".format(day, E_X))
