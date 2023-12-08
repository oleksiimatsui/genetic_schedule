from models import *
import random



class genetic:
    def __init__(self, subjects, teachers, groups, audiences, max_lessons):
        self.subjects = subjects
        self.teachers = teachers
        self.groups = groups
        self.audiences = audiences
        self.max_lessons = max_lessons

    def get_default(self,population_size):
        res = []
        for i in range(population_size):
            chromosome = []
            for group in self.groups:
                for subject in group.subjects_hours:
                    for t in range(subject[1]):
                        gene = Lesson(
                                    subject[0], 
                                    random.choice(self.teachers),
                                    group,
                                    random.choice(self.audiences),
                                    random.choice(range(1,self.max_lessons+1)),
                                    random.choice(range(1,6))
                                )
                    chromosome.append(gene)
            res.append(chromosome)
        return res
    
    def get_fitness(self, chromosome):
        conflicts = 0

        # Check for time conflicts between pairs of classes
        conflicts += sum(
            1 for i, c1 in enumerate(chromosome)
            for c2 in chromosome[i + 1:]
            if (
                c1.day == c2.day and c1.pair == c2.pair and
                (
                    c1.group == c2.group or
                    c1.teacher == c2.teacher or
                    c1.group == c2.group or
                    c1.audience == c2.audience
                )
            )
        )

        # # Check for conflicts where teachers or groups teach the wrong subject
        conflicts += sum(1 for c in chromosome if c.teacher.subjects.count(c.subject) == 0)

        for lesson in chromosome:
            if(lesson.subject not in lesson.teacher.subjects):
                conflicts += 1

        for lesson in chromosome:
            groupsubjects = [ x[0] for x in lesson.group.subjects_hours]
            if(lesson.subject not in groupsubjects):
                conflicts += 1

        teaching_hours = {}
        for c in chromosome:
            teacher_name = c.teacher.name
            if teacher_name not in teaching_hours:
                teaching_hours[teacher_name] = 0
            teaching_hours[teacher_name] += 1
        

        for teacher_name, hours in teaching_hours.items():
            if hours > [c.hours for c in self.teachers if c.name == teacher_name][0]:
                conflicts += 1

       # print(f"Conflicts: {conflicts}, rating: {1.0 / (1.0 + conflicts)}")
        return 1.0 / (1.0 + conflicts)


    def binary_tournament_selection(self,population):
        parent1 = random.choice(population)
        parent2 = random.choice(population)
        if self.get_fitness(parent1) > self.get_fitness(parent2):
            return parent1
        else:
            return parent2
        
    def single_point_crossover(parent1, parent2):
        min_length = min(len(parent1), len(parent2))
        crossover_point = random.randint(1, min_length - 1)
        offspring1 = parent1[:crossover_point] + parent2[crossover_point:]
        offspring2 = parent2[:crossover_point] + parent1[crossover_point:]
        return offspring1, offspring2
    
    def two_point_crossover(parent1, parent2):
        crossover_point1 = random.randint(1, len(parent1) - 2)
        crossover_point2 = random.randint(crossover_point1 + 1, len(parent1) - 1)
        offspring1 = parent1[:crossover_point1] + parent2[crossover_point1:crossover_point2] + parent1[crossover_point2:]
        offspring2 = parent2[:crossover_point1] + parent1[crossover_point1:crossover_point2] + parent2[crossover_point2:]
        return offspring1, offspring2
    
    def select_elite_baker(self, sorted_population, default_size):
        elite_individuals = []
        size=0
        while(size < default_size):
            size=len(elite_individuals)
            for i in range(default_size):
                N = default_size - i
                p = N/default_size
                if(random.random() < p):
                    elite_individuals.append(sorted_population[i][0])
                else:
                    pass
        return elite_individuals
    
    def create_next_generation(self, original_population, offspring, mutated, elitism_rate):
        population_size = len(original_population)
        elitism_count = int(elitism_rate * population_size)
        elite_individuals = self.select_elite(original_population, elitism_count)
        next_generation = elite_individuals + offspring + mutated
        return next_generation
    
    def mutate(self, chromosome, mutation_rate):
        if random.random() < mutation_rate:
            for i in range(len(chromosome)):
                lesson = chromosome[i]
                #chromosome[i].subject = random.choice(self.subjects)
                #chromosome[i].teacher = random.choice(self.teachers)
                #chromosome[i].group = random.choice(self.groups)
                chromosome[i].audience = random.choice(self.audiences)
                chromosome[i].pair = random.choice(range(1,self.max_lessons+1))
                chromosome[i].day = random.choice(range(1,6))
        return chromosome

    def solve(self, population_size, max_generations, CROSSOVER_RATE, MUTATION_RATE):
        population = self.get_default(population_size)
        index=0
        best_fitness = 0
        
        while(best_fitness < 0.9):
            
            #population = population[int(ELITISM_RATE*population_size):]
            children = []
            population_size
            for j in range(population_size//2):
                if random.random() < CROSSOVER_RATE:
                    parent1 = self.binary_tournament_selection(population)
                    parent2 = self.binary_tournament_selection(population)
                    child1, child2 = genetic.two_point_crossover(parent1, parent2)
                    children.append(child1)
                    children.append(child2)
                    for chromosome in children[-2:]:
                        chromosome = self.mutate(chromosome, MUTATION_RATE)
            
            population = population + children

            population_with_fitness = [(chromosome, self.get_fitness(chromosome)) for chromosome in population]
            population_with_fitness.sort(key=lambda x: x[1], reverse= True)
            best_fitness = population_with_fitness[0][1]
            print(f"Generation {index + 1}: Best Fitness = {best_fitness}, size = {population_size}")

            population = self.select_elite_baker(population_with_fitness, population_size)

            index += 1
            if(index > max_generations):
                print("generation limit exceeded")
                break

        best_individual = max(population_with_fitness, key=lambda x: x[1])
        return best_individual 
           
