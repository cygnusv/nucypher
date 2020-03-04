import sys

from web3 import Web3

worklock_supply = Web3.toWei(280_000_000, 'ether')
min_bid = Web3.toWei(7, 'ether')
max_bid = Web3.toWei(14_000, 'ether')

min_stake = Web3.toWei(14_000, 'ether')
max_stake = Web3.toWei(28_000_000, 'ether')

import random

# initial_bids = [7, 14_000, 100, ] + [8] * 10

# initial_bids = [8]*750 + [14000]*5 + list(range(10,14000,50))

#
# initial_bids = list(range(10,14000,14000//150))
#
# initial_bids = [8]*1000 + [14000]*1000

# Edge case where the iterative algorithm may take too many rounds
# initial_bids = [random.randrange(7, 10) for _ in range(10)] + [random.randrange(1390, 1400) for _ in range(9)]

# Edge case where the small bidder doesn't get enough tokens
# initial_bids = [7] + [70]*2000

# Another edge case where the iterative algorithm may take too many rounds
# small_bids = [random.randrange(min_bid, int(1.5 * min_bid)) for _ in range(10)]
# total_small_bids = sum(small_bids)
# min_potential_whale_bid = (max_bid - total_small_bids) // 9
# whales_bids = [random.randrange(min_potential_whale_bid, max_bid) for _ in range(9)]
# initial_bids = small_bids + whales_bids

# initial_bids = [7] + [700]*400 + [7000]

# edgeware locked 12m
initial_bids = [42570,40791,28529,27936,26004,22000,20000,20000,20000,20000,20000,20000,20000,20000,20000,15925,15287,15001,15000,11000,10995,10000,10000,8000,5000,5000,4000,3364,3348,3148,3059,3000,3000,3000,3000,3000,2685,2501,2020,2000,2000,2000,2000,2000,1909,1829,1631,1500,1323,1300,1100,1038,1015,1000,1000,1000,1000,1000,1000,1000,1000,1000,1000,1000,1000,1000,1000,1000,1000,1000,1000,1000,1000,1000,1000,1000,1000,1000,1000,1000,979,957,900,823,801,800,780,769,750,750,702,656,630,615,555,550,531,500,500,500,500,500,500,500,500,500,500,500,500,500,500,500,500,500,500,500,500,480,458,455,431,410,400,400,400,400,398,370,359,350,330,320,320,301,301,300,300,300,300,300,300,300,300,300,300,280,261,259,255,253,250,250,250,228,220,213,203,200,200,200,200,200,200,200,200,200,200,200,200,200,200,199,182,181,168,164,164,161,155,152,151,150,150,150,150,150,150,149,146,146,143,140,140,136,130,129,125,124,124,120,117,115,110,108,106,106,105,105,104,103,102,102,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,97,96,94,90,90,90,90,89,89,88,86,85,85,83,81,80,80,80,80,79,78,77,76,76,76,75,75,75,72,72,72,72,70,70,69,65,65,64,64,63,60,60,60,60,60,60,59,57,56,55,55,55,53,52,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,49,49,48,47,47,46,45,45,45,45,45,44,44,44,44,42,41,41,41,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,39,39,39,38,38,37,37,37,36,36,36,35,35,35,35,35,34,34,33,33,32,32,32,32,31,30,30,30,30,30,30,30,30,30,30,30,30,30,30,30,30,30,30,30,30,30,30,29,29,28,28,27,26,26,26,26,25,25,25,25,25,25,25,25,25,25,25,25,25,24,24,24,24,24,23,23,23,23,23,23,22,22,22,22,21,21,21,21,21,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,19,19,19,19,19,19,18,18,18,18,18,18,17,17,17,17,17,17,17,17,17,17,16,16,16,16,16,16,16,16,16,16,16,16,16,16,16,16,16,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,14,14,14,14,14,14,14,14,13,13,13,13,13,13,13,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,11,11,11,11,11,11,11,11,11,11,11,11,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7]
initial_bids = map(lambda x: x * 10**18, initial_bids)

initial_bids = list(sorted(initial_bids))


def distribute(bids):
    total_bids = sum(bids)
    # nu_per_eth = worklock_supply / total_bids
    distribution = [(bid, (bid*worklock_supply) // total_bids, i) for i, bid in enumerate(bids)]
    return distribution


def print_distribution(distribution):
    for bid, tokens, i in distribution:
        print(i, "OK " if tokens <= max_stake else "BAD",
              Web3.fromWei(bid, 'ether'), Web3.fromWei(tokens, 'ether'))


def check_distribution(distribution):
    bids = [bid for bid, _, _ in distribution]
    total_bids = sum(bids)
    nu_per_eth = worklock_supply / total_bids
    max_potential_stake = max_bid * nu_per_eth
    if max_potential_stake <= max_stake:
        return True

    bid, tokens, _i = distribution[-1]
    return tokens <= max_stake


def reduce_whale(distribution):
    whale = max(distribution)
    print("whale", whale)

    whale_bid, whale_tokens, whale_index = whale
    new_bids = [bid for bid, _, _ in distribution]

    if whale_tokens <= max_stake:
        sys.exit()

    allowed_ratio_for_whale = 0.9 * max_stake / whale_tokens

    new_whale_bid = allowed_ratio_for_whale * whale_bid

    new_bids = [bid for bid, _, _ in distribution]
    new_bids[whale_index] = new_whale_bid
    return new_bids


from bisect import bisect_right
# def find_gt_index(a, x):
#     'Find leftmost value greater than x'
#     i = bisect_right(a, x)
#     if i != len(a):
#         return a[i]
#     raise ValueError


def reduce_whales(distribution, coefficient):
    bids, tokens, _ = list(map(list, zip(*distribution)))

    clip_index = bisect_right(tokens, max_stake)

    # for i in range(clip_index, len(bids)):
    #     print(f"whale {i}: {bids[i]} -> {tokens[i]}")

    if clip_index >= len(bids):
        sys.exit()

    whale_bid, whale_tokens, whale_index = bids[clip_index], tokens[clip_index], clip_index

    if whale_tokens <= max_stake:
        sys.exit()

    for i in range(clip_index, len(bids)):
        whale_bid, whale_tokens, whale_index = bids[i], tokens[i], i
        allowed_ratio_for_whale = coefficient * max_stake / whale_tokens
        new_whale_bid = allowed_ratio_for_whale * whale_bid
        bids[whale_index] = new_whale_bid
        print(f"whale {i}: {whale_bid} -> {new_whale_bid}")

    bids = list(sorted(bids))
    return bids


def reduce_whales_2(distribution, previous_whales):
    bids, tokens, _ = list(map(list, zip(*distribution)))

    clip_index = bisect_right(tokens, max_stake)

    # for i in range(clip_index, len(bids)):
    #     print(f"whale {i}: {bids[i]} -> {tokens[i]}")

    if clip_index >= len(bids):
        sys.exit()

    clip_index -= previous_whales

    # whale_bid, whale_tokens, whale_index = bids[clip_index], tokens[clip_index], clip_index

    # if whale_tokens <= max_stake:
    #     sys.exit()

    bids = solidity_reduce(bids, clip_index)
    bids = list(sorted(bids))
    return bids, (len(bids) - clip_index)


def solidity_reduce(bids, clip_index):
    min_whale_bid = min(bids[clip_index:])
    max_whale_bid = max(bids[clip_index:])

    if min_whale_bid != max_whale_bid:
        print(f"STEP 1")
        for i in range(clip_index, len(bids)):
            whale_bid, whale_index = bids[i], i
            bids[whale_index] = min_whale_bid
            print(f"whale {i}: {Web3.fromWei(whale_bid, 'ether')} -> {Web3.fromWei(min_whale_bid, 'ether')}")

    total_bids = sum(bids)
    assert (min_whale_bid * worklock_supply) // total_bids > max_stake

    print(f"STEP 2")
    n_whales = len(bids) - clip_index

    a = min_whale_bid * worklock_supply - max_stake * total_bids
    b = worklock_supply - max_stake * n_whales
    # delta = (a + b - 1) // b

    # delta = math.ceil(((min_whale_bid * worklock_supply - max_stake * total_bids) * 1e18 /
    #                   ((worklock_supply - max_stake * n_whales) * 1e18)) * 1e18)
    # delta = float(Web3.fromWei(delta, 'ether'))
    # delta = math.ceil(a / b)
    delta = -(-a//b)
    # print(f"delta {delta1} -> {delta}")
    print(f"delta {delta}")
    # min_whale_bid = int(Web3.toWei(min_whale_bid, 'ether'))
    min_whale_bid -= delta
    # min_whale_bid = float(Web3.fromWei(min_whale_bid, 'ether'))
    for i in range(clip_index, len(bids)):
        whale_bid, whale_index = bids[i], i
        bids[whale_index] = min_whale_bid
        print(f"whale {i}: {Web3.fromWei(whale_bid, 'ether')} -> {Web3.fromWei(min_whale_bid, 'ether')}")
    return bids


# print("--------------------------------")
# bids_i = initial_bids
# coefficient = 0.9
# for i in range(1000):
#     print(" ROUND ", i)
#     round_i = distribute(bids_i)
#     print_distribution(round_i)
#     if check_distribution(round_i):
#     #     print(" ROUND ", i)
#     #     print_distribution(round_i)
#         break
#     bids_i = reduce_whales(round_i, coefficient)

print("--------------------------------")
bids_i = initial_bids
previous_whales = 0
for i in range(1000):
    print(" ROUND ", i, "eth supply:", sum(bids_i)//10**18)
    round_i = distribute(bids_i)
    print_distribution(round_i)
    if check_distribution(round_i):
    #     print(" ROUND ", i)
    #     print_distribution(round_i)
        break
    bids_i, previous_whales = reduce_whales_2(round_i, previous_whales)

# print(" POST ROUND ")
# distribution = distribute(initial_bids)
# print(" BEFORE ")
# print_distribution(distribution)
# bids = solidity_reduce(initial_bids, len(initial_bids) - previous_whales)
# bids = list(sorted(bids))
# result = distribute(bids)
# print(" AFTER ")
# print_distribution(result)