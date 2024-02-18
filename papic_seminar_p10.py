# -*- coding: utf-8 -*-
"""
[Statistika]: Seminarski rad

@author: Anamarija Papić
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

# Čitanje podataka iz Excel datoteke
data = pd.read_excel('p10.xlsx', usecols=[0], names=['Vrijeme'])

# Konverzija stupca 'Vrijeme' u numerički format
data['Vrijeme'] = pd.to_numeric(data['Vrijeme'], errors='coerce')

# 1. Deskriptivna statistika
mean = np.mean(data['Vrijeme'])
mode = stats.mode(data['Vrijeme'])
median = np.median(data['Vrijeme'])
five_number_summary = np.percentile(data['Vrijeme'], [0, 25, 50, 75, 100])
variance = np.var(data['Vrijeme'])
std_deviation = np.std(data['Vrijeme'])
interquartile_range = np.percentile(data['Vrijeme'], 75) - np.percentile(data['Vrijeme'], 25)
data_range = np.max(data['Vrijeme']) - np.min(data['Vrijeme'])

print(f"Srednja vrijednost: {mean}")
print(f"Mod: {mode} što znači da je vrijednost {mode[0]} najfrekventnija vrijednost i pojavljuje se {mode[1]} put.",)
print(f"Medijan: {median}")
print(f"Karakteristična petorka uzorka: {five_number_summary}")
print(f"Varijanca: {variance}")
print(f"Standardna devijacija: {std_deviation}")
print(f"Interkvartil: {interquartile_range}")
print(f"Raspon uzorka: {data_range}")

# 2. Razdioba frekvencija
bins = range(0, 35, 5)
frequency_table = pd.Series(pd.cut(data['Vrijeme'], bins=bins, include_lowest=True)).value_counts().sort_index()
relative_frequency = frequency_table / len(data)
cumulative_relative_frequency = relative_frequency.cumsum()

print("\nFrekvencijska tablica:")
print(frequency_table)

print("\nRelativna frekvencija:")
print(relative_frequency)

print("\nKumulativna relativna frekvencija:")
print(cumulative_relative_frequency)

# 3. Grafički prikazi
plt.figure(figsize=(12, 6))

# Računanje središnjih točki za iscrtavanje na grafu
midpoints = [interval.mid for interval in frequency_table.index]

plt.subplot(2, 2, 1)
plt.hist(data['Vrijeme'], bins=bins, edgecolor='black')
plt.title('Histogram frekvencija')
plt.xlabel('Vrijeme (u danima)')
plt.ylabel('Frekvencija')
plt.grid(axis='y', alpha=0.75)
plt.tight_layout()
plt.show()

plt.subplot(2, 2, 2)
plt.hist(data['Vrijeme'], bins=bins, density=True, edgecolor='black')
plt.title('Histogram relativnih frekvencija')
plt.xlabel('Vrijeme (u danima)')
plt.ylabel('Relativna frekvencija')
plt.grid(axis='y', alpha=0.75)
plt.tight_layout()
plt.show()

plt.subplot(2, 2, 3)
plt.plot(midpoints, frequency_table.values, marker='o')
plt.title('Poligon frekvencija')
plt.xlabel('Vrijeme (u danima)')
plt.ylabel('Frekvencija')
plt.grid(axis='y', alpha=0.75)
plt.tight_layout()
plt.show()

plt.subplot(1, 2, 1)
plt.plot(midpoints, cumulative_relative_frequency.values, marker='o')
plt.title('Kumulativni poligon relativnih frekvencija')
plt.xlabel('Vrijeme (u danima)')
plt.ylabel('Kumulativna relativna frekvencija')
plt.grid(axis='y', alpha=0.75)
plt.tight_layout()
plt.show()

plt.subplot(2, 3, 6)
plt.boxplot(data['Vrijeme'], vert=False)
plt.title('Karakteristična petorka')
plt.xlabel('Vrijeme (u danima)')
plt.tight_layout()
plt.show()

plt.figure(figsize=(8, 8))
wedges, texts, autotexts = plt.pie(frequency_table, autopct='%1.1f%%', startangle=90)
plt.title('Strukturni krug frekvencija')
plt.legend(wedges, frequency_table.index, title='Vrijeme (u danima)')
plt.tight_layout()
plt.show()

# 4. Interval povjerenja
confidence_interval = stats.norm.interval(0.90, loc=mean, scale=std_deviation/np.sqrt(len(data)))
print(f"\nInterval povjerenja (90%): {confidence_interval}")

confidence_interval = stats.norm.interval(0.95, loc=mean, scale=std_deviation/np.sqrt(len(data)))
print(f"Interval povjerenja (95%): {confidence_interval}")

confidence_interval = stats.norm.interval(0.99, loc=mean, scale=std_deviation/np.sqrt(len(data)))
print(f"Interval povjerenja (99%): {confidence_interval}")

# 5. Testiranje hipoteze
# Npr. testiranje hipoteze o prosječnom vremenu provedenom na Zavodu za zapošljavanje čekajući posao
# H0: μ = 15, H1: μ ≠ 15
# Koristi se t-test
alpha = 0.05
t_statistic, p_value = stats.ttest_1samp(data['Vrijeme'], popmean=15)

print("\nTestiranje hipoteza:")
print(f"T-statistika: {t_statistic}")
print(f"P-vrijednost: {p_value}")

if p_value < alpha:
    print("Odbacujemo nultu hipotezu.")
else:
    print("Ne možemo odbaciti nultu hipotezu.")
