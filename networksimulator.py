import random
import matplotlib.pyplot as plt
import numpy as np

NUM_COMPUTERS = 8
QUEUE_SIZE = 5
WAVELENGTHS = 4
TRANSMISSION_PROBABILITY = 0.5

computers = [
    {"queue": [], "wavelength": i // 2} for i in range(NUM_COMPUTERS)
]

def simulate(p_arrival, slots=10000):
    total_delay = 0
    successful_transmissions = 0
    lost_packets = 0

    for _ in range(slots):
        for computer in computers:
            if len(computer["queue"]) < QUEUE_SIZE and random.random() < p_arrival:
                computer["queue"].append({"arrival_time": _})
            elif len(computer["queue"]) >= QUEUE_SIZE and random.random() < p_arrival:
                lost_packets += 1

        transmission_count = [0] * WAVELENGTHS
        transmitting_computers = [[] for _ in range(WAVELENGTHS)]

        for i, computer in enumerate(computers):
            if computer["queue"] and random.random() < TRANSMISSION_PROBABILITY:
                wavelength = computer["wavelength"]
                transmission_count[wavelength] += 1
                transmitting_computers[wavelength].append(i)

        for wavelength, transmission_list in enumerate(transmitting_computers):
            if transmission_count[wavelength] == 1:
                computer_index = transmission_list[0]
                packet = computers[computer_index]["queue"].pop(0)
                successful_transmissions += 1
                total_delay += _ - packet["arrival_time"]

    avg_delay = total_delay / successful_transmissions if successful_transmissions > 0 else 0
    throughput = successful_transmissions / slots
    loss_rate = lost_packets / (slots * NUM_COMPUTERS)
    return avg_delay, throughput, loss_rate

probabilities = np.linspace(0.1, 1.0, 10)
avg_delays = []
throughputs = []
loss_rates = []

for p in probabilities:
    avg_delay, throughput, loss_rate = simulate(p)
    avg_delays.append(avg_delay)
    throughputs.append(throughput)
    loss_rates.append(loss_rate)

# Plot average delay
plt.figure(figsize=(10, 6))
plt.plot(probabilities, avg_delays, marker="o", label="Average Delay")
plt.xlabel("Packet Arrival Probability (p)")
plt.ylabel("Average Packet Delay (slots)")
plt.title("Average Packet Delay vs Arrival Probability")
plt.grid()
plt.legend()
plt.savefig("average_delay.png")
plt.show()

# Plot throughput
plt.figure(figsize=(10, 6))
plt.plot(probabilities, throughputs, marker="o", label="Throughput")
plt.xlabel("Packet Arrival Probability (p)")
plt.ylabel("Throughput (successful transmissions per slot)")
plt.title("Throughput vs Arrival Probability")
plt.grid()
plt.legend()
plt.savefig("throughput.png")
plt.show()

# Plot loss rate
plt.figure(figsize=(10, 6))
plt.plot(probabilities, loss_rates, marker="o", label="Loss Rate")
plt.xlabel("Packet Arrival Probability (p)")
plt.ylabel("Loss Rate (fraction of lost packets)")
plt.title("Loss Rate vs Arrival Probability")
plt.grid()
plt.legend()
plt.savefig("loss_rate.png")
plt.show()