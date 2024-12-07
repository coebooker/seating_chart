class Floor:
    def __init__(self):
        self.is_empty = True
    def __repr__(self):
        return "."
    def __eq__(self, other):
        return self.is_empty == other.is_empty
    def next_state(self, _):
        return self
        
class Seat:
    def __init__(self, is_empty, position):
        self.is_empty = is_empty
        self.x, self.y = position
        #List that contains the mutation for each adjacent space
        self.mutations = (
            (-1, -1), (0, -1), (1, -1),
            (-1,  0),          (1,  0), 
            (-1,  1), (0,  1), (1,  1)
        )
    def __repr__(self):
        if self.is_empty:
            return "L"
        else:
            return "#"
    def __eq__(self, other):
        if self.x == other.x and self.y == other.y and self.is_empty == other.is_empty:
            return True
        else:
            return False
        
    ## returns the next_state for a given Seat. Either occupied or empty
    def next_state(self, layout):
        adjacent_count = 0
        for mutation_x,mutation_y in self.mutations:
            #The x,y of the current space being checked
            adj_x = self.x + mutation_x
            adj_y = self.y + mutation_y

            if adj_x < 0 or adj_x >= len(layout[0]):
                continue
            if adj_y < 0 or adj_y >= len(layout):
                continue
            if not layout[adj_y][adj_x].is_empty:
                adjacent_count += 1

        #When 4 or more adjacent spaces are occupied this space should become empty
        if adjacent_count >= 4:
            return Seat(True, (self.x, self.y))
        #If there are no adjacent spaces this space should become occupied
        elif adjacent_count == 0:
            return Seat(False, (self.x, self.y))
        #Between 0 and 4 adjacent space, the space should not change
        else:
            return self
        
#Container Class makes the structure that holds the layout list
class Container:
    def __init__(self, input_string):
        self.layout = []
        row = []
        x = 0
        y = 0

        for char in input_string:
            position_tup = (x,y)
            x += 1
            if char == "L":
                row.append(Seat(True, position_tup))
            elif char == ".":
                row.append(Floor())
            elif char == "#":
                row.append(Seat(False, position_tup))
            #When hitting a new line char the row should be added to the layout and y should be incremented 
            # and the x should be reset
            else:
                self.layout.append(row)
                row = []
                y += 1
                x = 0
        #The last line doesn't have an additional new line, so whatever's left when the characters run out is the extra
        self.layout.append(row)
            

#Creates the next seating chart, gets the next_state for each space and returns the next_seating_chart
def run(seating_chart):
    next_seating_chart = Container(input_string)

    for y in range(len(seating_chart.layout)):
        for x in range(len(seating_chart.layout[0])):
            space = seating_chart.layout[y][x]
            next_seating_chart.layout[y][x] = space.next_state(seating_chart.layout)
    return next_seating_chart

#Main function, sets up the general flow and returns the answer after stabilization
def main():
    seating_chart = Container(input_string)
    next_seating_chart = run(seating_chart)
    seat_count = 0
    #While the seating chart has not stabalized
    while seating_chart.layout != next_seating_chart.layout:
        seating_chart = next_seating_chart
        next_seating_chart = run(seating_chart)
    for row in seating_chart.layout:
        for space in row:
            #Because Floor.is_empty returns False, it needs to check if the object is a Seat
            if isinstance(space, Seat):
                if not space.is_empty:
                    seat_count += 1
    return seat_count

infile = open("input.txt","r")
input_string = infile.read()
infile.close()

print(main())
