import pandas as pd
import numpy as np

class DieGame():
    """
    This Class is used in combination of the Game Class and Analyzer Class to 
    create a Monte Carlo Simulator. The die has multiple sides and weights that 
    can be "rolled" to select a face.
    """
    def __init__(self, faces):
        """
        This function requires a set of already instiated faces as a list.
        The Class creates a private Dataframe to store the Faces. 
        The weights of the faces are initialized as 1s, unless changed by using the change weight function.

        Parameters
        ------
        faces: list
            has to be an array of faces
            examples: [1,2,3,4]
        """
        self.weights = np.ones(len(faces))
        self.faces = faces
        self._FacesWeights = pd.DataFrame({
            'Face': self.faces,
            'Weights' : self.weights
        })

    
    def change_weight(self,face, newweight):
        """
        This function changes the weight of the faces of the "die" that you use.
        The function checks if the Face is in the Dataset, and then will change the weight to whatever the second input was.

        Parameters
        ------

        face: any
            have to be a number in the array of faces passed to the __init__ function
            examples: 2
        newweight: int
            changes the weight of the face that was passed first
            examples: 3
        """
        faceplace = self._FacesWeights['Face'].to_numpy()
        if face not in faceplace:
            return ValueError("Not a Valid Face")
        indexed = list(self._FacesWeights.index[self._FacesWeights['Face'] ==face])[0]
        self._FacesWeights.loc[indexed,'Weights']= newweight
        

    def roll_die(self, rolls = 1):
        """
        This function randomly picks a face from the array of faces. Also takes into account the weights if Change Weight was used.
        Will roll once if no other number is put in.

        Parameters
        ------
        rolls = 1: int
            requires any integer >1.
            example: 100
        """
        rolled = self._FacesWeights.sample(n= rolls, replace = True, weights = 'Weights').reset_index(drop=True)
        return list(rolled['Face'])

    def show(self):
        """
        This function shows the Dataframe of Faces and Weights.
        Does not require a parameter.
        """
        return (self._FacesWeights)    



class Games():
    """
    This Class is used in combination of the Die Class and Analyzer Class. 
    This class rolls the instiated dice of the same kind one or more times.
    This class has the function play and show.
    """
    def __init__(self, dieobjects):
        """
        This function requires a list of one of more similarly defined dice.
        The Class uses the Class DieGame to create the list of die and change their weights.
    
        Parameters
        ------
        dieobject: list
            example:    die3 = {1:1,2:1,3:1,4:1}
                        dice = {1:die1}
                        for iterable,theDie in dice.items():
                            dice[iterable] = DieGame(theDie.keys())
                            for key in theDie.keys():
                                dice[iterable].change_weight(key, theDie[key])
                        dice.values() #pass into the class
                        game = Games(dice.values())
        """
        self.dieobjects = list(dieobjects)
        
    def play(self, rollnumber=1):
        """
        This function uses the die that was instaniated by the __init__ function 
        to randomly choose a number of the faces. The number chosen will also vary 
        by the weight that was given along with the die.
        The function will roll the die once unless another integer number is used.
        The rolled number will stored in a private dataframe called _rolled.

        Parameters
        ------
        rollnumber =1 :int
            example: 10000
                    game = Games(dice.values())
                    game.play(10000)
        """
        RolledNumber = []
        for dice in self.dieobjects:
            RolledNumber.append(dice.roll_die(rollnumber))
        RolledNumber = np.array([np.array(x) for x in RolledNumber]).T
        self._rolled = pd.DataFrame(RolledNumber, columns= range(1,len(self.dieobjects)+1), index = range(1,rollnumber+1))
        

    def show(self, NorW = 'wide'):
        """
        This function takes the rolled dataframe that was made and returns it to the user.
        The function can be ran by itself, which would return an unstacked (each role is 
        an observation and each column is a feature and each cell shows the resulting
        face for the die on the roll) dataframe, but if given the parameter 'narrow' it will 
        stack (two-column index with the roll number and the die number and a single column for the face rolled) 
        the dataframe. If given a different parameter the function will return 'ValueError Invalid Option.'

        Parameters
        ------
        NorW: 'narrow' | 'wide'
            example: game.show() | game.show('narrow')
        """
        if NorW == 'narrow':
            return (self._rolled.stack())
        if NorW == 'wide': 
            return self._rolled
        if NorW != 'wide' or 'narrow':
            return ValueError("Invalid Option")



class Analyzer():
    """
    This Class is used in combination of the Die Class and Game Class. 
    This class specifically takes the reults of a single game and computes various descriptive
    statistical properties about it.
    This class has the function faceperroll, combo, and jackpot.
    """
    def __init__(self,objects):
        """
        This function requires a game object as its input parameter.
        It analyzes the numbers that were rolled and puts them into a data frame. It then
        allows the user to see the amount of of times a given face is rolled in each event.
        Then from the other functions allows the user to see the distinct combinations of faces rolled, 
        along with their counts and to see how many times the game resulted in all faces 
        being identical.

        Parameters
        ------
        objects: list
            example:    die3 = {1:1,2:1,3:1,4:1}
                dice = {1:die1}
                for iterable,theDie in dice.items():
                    dice[iterable] = DieGame(theDie.keys())
                    for key in theDie.keys():
                        dice[iterable].change_weight(key, theDie[key])
                dice.values() #pass into the class
                game = Games(dice.values())
                game.play(10)
                game.show()
                Analyzed = Analyzer(game)
        """
        self.objects = objects
        self._faces = list(self.objects.dieobjects[0].faces)


    def faceperroll(self):
        """
        This function requires no inputs and does not return anything for the user to see.
        This function stores the results of how many times a given face is rolled in each 
        event in the game function. The dataframe is a public attribute and has an index of the 
        roll number and face values as columns.

        Parameters
        ------
        none 
        """
        self.data = pd.DataFrame(columns = self._faces, index = range(1,len(self.objects.show())+1))
        for index,series in self.objects.show().iterrows():
            events = []
            event = (series.value_counts().to_dict())
            for ithappened in self._faces: 
                if ithappened in event:
                    events.append(event[ithappened])
                else:
                    events.append(0)
            self.data.loc[index]=events 

            
    def combo(self):
        """
        This function requires no inputs and does not return anything for the user to see.
        This function computes the distinct combinations of faces rolled, along with their counts.
        The combinations are sorted and saved as a multi-columned index. The data is 
        stored in a public dataframe.

        Parameters
        ------
        none 
        """
        data_copy = self.data.copy()
        data_copy['count']= 0
        self.something = data_copy.groupby(by= self._faces).count()
        

    def jackpot(self):
        """
        This function requires no inputs, but returns an integer number for how many times
        the game results in all faces being identical. The data is stored in a public dataframe.
        The dataframe has the roll number as its named index.

        Parameters
        ------
        none 
        """
        jackpot = self.data == len(self.objects.dieobjects)
        self.jackpotresults = self.data[jackpot.any(axis=1)]
        return(jackpot.any(axis = 1).sum())
        


if __name__ == '__main__':
    die1 = {1:1,2:1,3:1,4:1}
    die2 = {1:1,2:1,3:1,4:2}
    die3 = {1:1,2:1,3:1,4:10}

    dice = {1:die1, 2:die2, 3:die3}

    for iterable,theDie in dice.items():
        dice[iterable] = DieGame(theDie.keys())
        for key in theDie.keys():
            dice[iterable].change_weight(key, theDie[key])
    game = Games(dice.values())
    game.play(10)
    game.show()
    Analyze = Analyzer(game)
    Analyze.faceperroll()
    Analyze.jackpot()