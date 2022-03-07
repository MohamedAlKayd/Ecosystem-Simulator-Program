# Mohamed Yasser Anwar Mahmoud AlKayd
# Ecosystem Simulator Program

# - Start of the Program -
  
import matplotlib.pyplot as plt
from helpers import (random_neighbor, random_empty_position, sort_animals,
                     remove_dead)
 
class Animal:
    """ Represents an animal in the ecosystem
    """
    def __init__(self, species, row, column):
        """ Initializes a new animal
        Args:
           self (Animal): the object being created
           species (str): species name ("Lion" or "Zebra")
           row (int): row for the new animal in the grid
           column (int): column for the new animal in the grid
        """
        self.species = species
        self.row = row
        self.col = column
        self.age = 0
        self.starving_duration = 0
        self.is_alive = True
 
    def __str__(self):
        """ Creates a string from an object
        Args:
           self (Animal): the object on which the method is called
        Returns:
           str: String summarizing the object
        """
        string = ("<species:" + self.species + ", row:" + str(self.row) +
                  ", col:" + str(self.col) + ", age:" + str(self.age) +
                  ", starving_duration:" + str(self.starving_duration) +
                  ", is_alive:" + str(self.is_alive) + ">")
        return string
 
    def can_eat(self, other):
        """ Checks if self can eat other
        Args:
           self (Animal): the object on which the method is called
           other (Animal): another animal
        Returns:
           boolean: True if self can eat other, and False otherwise
        """
        if self.species=="Lion" and other.species=="Zebra":
            return True
        else:
            return False
 
    def time_passes(self):
        """ Increases age and starving_duration
        Args:
           self (Animal): the object on which the method is called
        Returns:
           Nothing
        """
        self.age+=1
        self.starving_duration+=1
        
    def dies_of_old_age(self):
        """ If an animal dies of old age, sets is_alive to False
        Args:
           self (Animal): the object on which the method is called
        Returns: None
        """
        if self.species=="Lion" and self.age>=18:
            self.is_alive=False
        elif self.species=="Zebra" and self.age>=7:
            self.is_alive=False
        
    def dies_of_hunger(self):
        """ If an animal dies of hunger, sets is_alive to False
        Args:
           self (Animal): the object on which the method is called
        Returns: None
        """
        if self.species=="Lion" and self.starving_duration>=6:
            self.is_alive=False
        
        
    def will_reproduce(self):
        """ Determines if an animal will reproduce at their current age
        Args:
           self (Animal): the object on which the method is called
        Returns:
           bool: True if ready to reproduce, False otherwise
        """
        if self.species=="Lion" and self.age>6 and self.age%7==0:
            return True
        elif self.species=="Zebra" and self.age>2 and self.age%3==0:
            return True
        else:
            return False
 
### end of Animal class ###
 
def initialize_population(grid_size):
    """ Initializes the grid by placing animals onto it.
    Args:
       grid_size (int): The size of the grid
    Returns:
       list of animals: The list of animals in the ecosystem
    """
    all_animals = []
    all_animals.append(Animal("Lion", 3, 5))
    all_animals.append(Animal("Lion", 7, 4))
    all_animals.append(Animal("Zebra", 2, 1))
    all_animals.append(Animal("Zebra", 5, 8))
    all_animals.append(Animal("Zebra", 9, 2))
    all_animals.append(Animal("Zebra", 4, 4))
    all_animals.append(Animal("Zebra", 4, 8))
    all_animals.append(Animal("Zebra", 1, 2))
    all_animals.append(Animal("Zebra", 9, 4))
    all_animals.append(Animal("Zebra", 1, 8))
    all_animals.append(Animal("Zebra", 5, 2))
 
    return all_animals
 
def move_animal(current_animal, grid_size, all_animals):
    """ Move an animal to a neighboring cell and either make it eat the
        neighboring animal or get eaten.
    Args:
        current_animal (Animal): The animal to be moved
        grid_size (int): The size of the grid
        all_animals (list of animals): The animals in the ecosystem
    Returns: None
    """ 
    RandomNeighbor=random_neighbor(current_animal, grid_size, all_animals)
    row=RandomNeighbor[0]
    col=RandomNeighbor[1]
    neighbor=RandomNeighbor[2]
    
    if neighbor is None:
        current_animal.row=row
        current_animal.col=col
    elif neighbor is not None:
        if current_animal.can_eat(neighbor)==True:
            current_animal.row=row
            current_animal.col=col
            current_animal.starving_duration=0
            neighbor.is_alive=False
        elif neighbor.can_eat(current_animal)==True:
            neighbor.starving_duration=0
            current_animal.is_alive=False
            
def reproduce_animal(parent_animal, grid_size, all_animals):
    """ Creates a new animal at a neighboring cell if the parent animal
        is ready to reproduce.
        The new animal is added to the list of all animals
    Args:
        parent_animal (Animal): The parent animal which may reproduce
        grid_size (int): The size of the grid
        all_animals (list of animals): The animals in the ecosystem
    """
    answer=Animal.will_reproduce(parent_animal)
    if answer==True:
        intial=random_empty_position(parent_animal,grid_size,all_animals)
        if intial is None:
            pass
        elif intial is not None:
            rows=intial[0]
            columns=intial[1]
            all_animals.append(Animal(parent_animal.species,rows,columns))
 
def one_step(all_animals, grid_size):
    """ Simulates the evolution of the ecosystem for one step (1 month)
    Args:
       all_animals (list of animals): The animals in the ecosystem
       grid_size (int): The size of the grid
    Returns: None
    """
    sort_animals(all_animals)
    
    for j in all_animals:
        j.time_passes()
        j.dies_of_old_age()
    remove_dead(all_animals)
    
    for i in all_animals:
        i.dies_of_hunger() 
    remove_dead(all_animals)
 
    for x in all_animals:
        if x.is_alive is True:
            move_animal(x,grid_size,all_animals)
    remove_dead(all_animals)
    sort_animals(all_animals)
    
    for z in all_animals:
        reproduce_animal(z,grid_size,all_animals)
 
def run_whole_simulation(grid_size=10, duration=20):
    """ Simulates the evolution of the whole ecosystem.
        Generates graph of species abundance and saves it to populations.png
    Args:
       grid_size (int): Size of the grid
       duration (int): Number of steps of the simulation
    Returns:
       Nothing
    """
    all_animals = initialize_population(grid_size)
    
    number_of_zebras_over_time=[]
    number_of_lions_over_time=[]
    zebras=0
    lions=0
    for i in all_animals:
        if i.species =="Lion":
            lions+=1
        elif i.species =="Zebra":
            zebras+=1
    number_of_zebras_over_time.append(zebras)
    number_of_lions_over_time.append(lions)
    
    for j in range(0,20):
        one_step(all_animals, grid_size)
        zebras=0
        lions=0
        for i in all_animals:
            if i.species=="Lion":
                lions+=1
            elif i.species=="Zebra":
                zebras+=1
        number_of_zebras_over_time.append(zebras)
        number_of_lions_over_time.append(lions)
        
    plt.plot(number_of_zebras_over_time,",-r",label="Zebras")
    plt.plot(number_of_lions_over_time,",-b",label="Lions")
    
    plt.title("Ecosystem simulator")
    plt.xlabel("Time in months")
    plt.ylabel("Number of animals")
        
    plt.legend()
    plt.savefig("population.png")

# - End of the Program -