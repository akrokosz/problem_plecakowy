import random
import time


def alg_wyczerpujacy(items, max_waga, time_to_exec):
    start_time = time.time()
    optim_comb = None
    best_value = 0
    best_size = max_waga + 1
    checked = 0

    end_time = start_time + time_to_exec * 60

    for i in range(1, 2 ** len(items[0])):

        if time.time() >= end_time:
            break

        combination = []
        current_size = 0
        current_value = 0

        for j in range(len(items[0])):

            if (i >> j) & 1:
                combination.append([j + 1, items[0][j], items[1][j]])
                current_size += items[0][j]
                current_value += items[1][j]

        checked += 1

        if current_size <= max_waga:
            if current_value > best_value or (current_value == best_value and current_size < best_size):
                optim_comb = combination
                best_value = current_value
                best_size = current_size

    end_time = time.time()
    exec_time = (end_time - start_time)

    print("optymalny zestaw: ", optim_comb)
    print("wielkosc plecaka: ", best_size)
    print("wartosc plecaka: ", best_value)
    print("execution time: ", exec_time, "sec")
    print("checked combinations: ", checked, "/", 2 ** len(items[0]) - 1)

    return optim_comb, best_value


def alg_heurystyczny(rzeczy, max_waga):
    start_time = time.time()

    num_items = len(rzeczy[0])
    item_indices = list(range(num_items))
    item_ratios = [rzeczy[1][i] / rzeczy[0][i] for i in item_indices]
    sorted_items = sorted(zip(item_indices, rzeczy[0], rzeczy[1], item_ratios), key=lambda x: x[3], reverse=True)

    total_value = 0
    total_size = 0
    remaining_capacity = max_waga
    sklad_plecaka = []

    for item in sorted_items:
        if item[1] <= remaining_capacity:
            sklad_plecaka.append([item[0] + 1, item[1], item[2]])
            total_value += item[2]
            total_size += item[1]
            remaining_capacity -= item[1]

    end_time = time.time()
    exec_time = (end_time - start_time)

    print("optymalny zestaw: ", sklad_plecaka)
    print("wielkosc plecaka: ", total_size)
    print("wartosc plecaka: ", total_value)
    print("execution time: ", exec_time, "sec")

    return sklad_plecaka, total_value, max_waga - remaining_capacity


def main():
    linijki = []

    with open("plecak.txt", "r") as plecak:
        data = plecak.readlines()
        linijki.extend([linia.replace("\n", "") for linia in data])

    max_waga = linijki[0].split()[4]
    nums = []
    sizes = []
    vals = []

    for line in data[1:]:
        if "dataset" in line:
            nums.append(int(line.strip("dataset").replace(":", "")))
        elif "sizes" in line:
            sizes.append(list(map(int, line.split("sizes = ")[1].replace(" ", "").strip('{} \n').split(','))))
        elif "vals" in line:
            vals.append(list(map(int, line.split("vals = ")[1].replace(" ", "").strip('{} \n').split(','))))

    losowy_nr = random.randint(0, len(nums) - 1)
    losowy_dataset = [sizes[losowy_nr], vals[losowy_nr]]

    print(losowy_nr)
    print("algorytm wyczerpujacy: ")
    alg_wyczerpujacy(losowy_dataset, int(max_waga), 1)
    print("algorytm heurystyczny: ")
    alg_heurystyczny(losowy_dataset, int(max_waga))


if __name__ == "__main__":
    main()
