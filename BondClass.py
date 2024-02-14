import numpy as np

class YieldCurveBootstrapper:
    def __init__(self):
        self.prices = []
        self.coupons = []
        self.payment_counts = []
        self.initial_rate = 0
        self.forward_interest_rates = []
        self.spot_interest_rates = []
        self.maturity_times = []
        self.yield_rates = []
        self.first_coupon_time = 0
        self.nominal_value = 100

    def input_data(self, payment_time, coupon_rate, bond_price, first_coupon_time):
        self.first_coupon_time = first_coupon_time
        self.prices.append(bond_price)
        self.payment_counts.append(payment_time)
        self.coupons.append(coupon_rate)

    def calculate_spot_rate(self):
        index = self.payment_counts.index(min(self.payment_counts))
        organized_data = sorted(zip(self.payment_counts, self.prices, self.coupons), key=lambda x: x[0])
        self.payment_counts, self.prices, self.coupons = zip(*organized_data)
        self.payment_counts = list(self.payment_counts)
        self.prices = list(self.prices)
        self.coupons = list(self.coupons)
        zero_coupon_rate = -(np.log((self.prices[index] + (0.5 - self.first_coupon_time) * self.coupons[index] * self.nominal_value) / self.nominal_value) / self.first_coupon_time)
        self.initial_rate = zero_coupon_rate
        self.maturity_times.append(self.first_coupon_time)
        return zero_coupon_rate

    def calculate_summation(self):
        summation = 0
        for i, time in enumerate(self.maturity_times):
            summation += (self.nominal_value * self.coupons[i] / 2) * np.exp(-self.spot_interest_rates[i] * time)
        return summation

    def calculate_spot_interest_rates(self):
        self.spot_interest_rates.append(self.calculate_spot_rate())
        for i in range(1, len(self.payment_counts)):
            adjusted_price = (0.5 - self.first_coupon_time) * self.coupons[i] * self.nominal_value + self.prices[i]
            rate = -np.log((adjusted_price - self.calculate_summation()) / (self.nominal_value * self.coupons[i] + self.nominal_value)) / (self.maturity_times[-1] + 0.5)
            self.spot_interest_rates.append(rate)
            self.maturity_times.append(self.maturity_times[-1] + 0.5)
        return self.spot_interest_rates

    def get_maturity_times(self):
        return self.maturity_times

    def calculate_yield_rates(self):
        for price, coupon, count in zip(self.prices, self.coupons, self.payment_counts):
            yield_rate = (self.nominal_value * coupon / 2 + ((self.nominal_value - price) / count)) / ((self.nominal_value + price) / 2)
            self.yield_rates.append(yield_rate)
        return self.yield_rates

    def calculate_forward_rates(self):
        for i in range(1, 5):
            rate = ((1 + self.spot_interest_rates[2 * i]) ** (2 * (i + 1)) / (1 + self.spot_interest_rates[2 * i - 2])) ** (1 / (2 * i)) - 1
            self.forward_interest_rates.append(rate)
        return self.forward_interest_rates
