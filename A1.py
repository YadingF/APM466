from BondClass import YieldCurveBootstrapper
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from Q1_assignment import all_yield


def payments_count(bond):
    payments = 1
    if float(bond['MATURITY DATE'][0]) == 9:
        payments += 1
    payments += 2 * (float(bond['MATURITY DATE'][-1]) - 4)
    return payments


def select_bond(data, index):
    if str(data.loc[index, 'MATURITY DATE'][0]) in ['3', '9'] and int(
            data.loc[index, 'MATURITY DATE'][-1]) < 9 and int(
        data.loc[index, 'MATURITY DATE'][-2]) == 2:
        return True
    return False


def first_coupon_time(bond, chosen_bonds):
    index = 0
    while bond['ASK'] != chosen_bonds[index]['ASK']:
        index += 1
    if index > 4:
        index += 2
    return (52 - index) / 365


all_yields = []
all_forwards = []

for j in range(10):
    data = pd.read_excel('Yield curves.xlsx', engine='openpyxl',
                         sheet_name=j)
    curve_bootstrapper = YieldCurveBootstrapper()
    selected_bonds = []
    for i in range(len(data)):
        if select_bond(data, i):
            selected_bonds.append(data.loc[i])

    for bond in selected_bonds:
        curve_bootstrapper.input_data(payments_count(bond),bond['COUPON'],bond['ASK'],first_coupon_time(bond, selected_bonds))
    yield_rates = curve_bootstrapper.calculate_yield_rates()
    spot_rates = curve_bootstrapper.calculate_spot_interest_rates()
    time_values = curve_bootstrapper.get_maturity_times()


    # Plotting

    plt.plot(time_values, spot_rates)
    plt.title("Zero Curve", fontsize=16, fontweight='bold')
    plt.ylabel("Zero Rate", fontsize=14)
    plt.xlabel("Maturity in Years", fontsize=14)
    plt.xlim(1, 4.55)
    plt.ylim(0.01, 0.06)
    payment_numbers = curve_bootstrapper.payment_counts
    plt.plot(payment_numbers, yield_rates)
    plt.title("Yield Curve", fontsize=16, fontweight='bold')
    plt.ylabel("Yields", fontsize=14)
    plt.xlabel("# of Coupon Payments", fontsize=14)
    plt.xlim(1, 10)
    forward_rates = curve_bootstrapper.calculate_forward_rates()
    plt.plot([1, 2, 3, 4, 5], forward_rates, linestyle='-', linewidth=2,
             marker='o', markersize=8, label='Forward Rate')
    plt.title("Forward Curve", fontsize=16, fontweight='bold')
    plt.xlabel("Years", fontsize=14)
    plt.ylabel("Forward Rate", fontsize=14)
    selected_yields = [item for index, item in enumerate(yield_rates) if
                       index % 2 == 0]
    all_yields.append(selected_yields)
    all_forwards.append(forward_rates)

plt.show()

