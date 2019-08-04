# Phát biểu bài toán: có n thành phố và m tuyến đường nối với các thành phố
# một người muốn đi từ thành phố 1 và qua tất cả các thành phố và trở về thành phố ban đầu
# với chi phí nhỏ nhất. Hãy thiết lập tuyến đường cho người này.

import random

n = 5   # so luong thanh pho
m = 6 # so luong ca the trong quan the
n_generations = 100 # so vong doi
losses = []  # de ve bieu de losses

# load data
def load_data():
    map = []
    file = open('data_route.txt', 'r')
    lines = file.readlines()
    for line in lines:
        strings = line.split(',')
        citys = [int(s.strip()) for s in strings]
        map.append(citys)
    file.close()
    return map

map = load_data()

# tao individual
def create_individual():
    list = []  # list cac thanh pho
    for i in range(n):
        list.append(i)
    random.shuffle(list)
    return list

# tinh loss
def compute_loss(individual):
    i = 0
    price = 0
    while i < n-1:
        a = individual[i]
        b = individual[i+1]
        price += map[a][b]
        i += 1
    # cong voi quang duong tp cuoi ve tp dau
    start = individual[0]
    finish = individual[n-1]
    price += map[finish][start]
    return price


# tinh fitness
def compute_fitness(individual):
    loss = compute_loss(individual)
    return 1 / (1 + loss)

# chon loc
def selection(sorted_population):
    index1 = random.randint(0, n-2)
    while True:
        index2 = random.randint(0, n-2)
        if index2 != index1:
            break
    individual = sorted_population[index1]
    if index2 > index1:
        individual = sorted_population[index2]
    return individual

# lai ghep:
def crossover(individual1, individual2, corossover_rate = 0.9):
    individual_c1 = individual1.copy()
    individual_c2 = individual2.copy()
    if random.random() < corossover_rate:
        # chọn một vị trí bất kì
        index = random.randint(1, n-3)
        # rà từng thành phố ở cá thể 2 xem đã có ở cá thể 1 chưa
        # nếu chưa có thì cho vào cá thể 1
        for i in range(index, n):
            for j in range(n):
                if individual_c1[:i].count(individual2[j]) == 0:
                    individual_c1[i] = individual2[j]
                    break
        for i in range(index, n):
            for j in range(n):
                if individual_c2[:i].count(individual1[j]) == 0:
                    individual_c2[i] = individual1[j]
                    break
    return individual_c1, individual_c2

# dot bien
def mutate(individual, mutation_rate = 0.05):
    individual_new = individual.copy()
    if random.random() < mutation_rate:
        index1 = random.randint(0, n-1)
        while True:
            index2 = random.randint(0, n-1)
            if index1 != index2:
                break
        individual_new[index1] = individual[index2]
        individual_new[index2] = individual[index1]
    return individual_new

# tao quan the moi
def create_new_population(soted_old_population):
    # luu vao losses
    losses.append(compute_loss(sorted_old_population[-1]))
    # in cac gia tri tot nhat qua tung doi
    # print(losses[-1])
    new_population = []
    while len(new_population) < m-2:
        # chon loc
        individual1 = selection(sorted_old_population)
        individual2 = selection(sorted_old_population)

        # lai ghep
        individual_c1, individual_c2 = crossover(individual1, individual2)

        # dot bien
        individual_m1 = mutate(individual_c1)
        individual_m2 = mutate(individual_c2)
    
        # cho vao quan the moi
        new_population.append(individual_m1)
        new_population.append(individual_m2)
    
    # cho 2 con dep nhat cua quan the cu vao quan the moi
    new_population.append(sorted_old_population[-1])
    new_population.append(sorted_old_population[-2])

    return new_population

# tao quan the ban dau
population = [create_individual() for _ in range(m)]

for _ in range(n_generations):
    sorted_old_population = sorted(population, key = compute_fitness)
    population = create_new_population(sorted_old_population)

# bieu do su bien thien cua loss qua tung doi
# import matplotlib.pyplot as plt
# plt.plot(losses)
# plt.xlabel('generation')
# plt.ylabel('loss')
# plt.show()

# hien thi tuyen duong ngan nhat
route_min = sorted_old_population[-1]
route_min.append(sorted_old_population[-1][0])
print('duong di ngan nhat: ', route_min, 'chi phi: ', losses[-1])