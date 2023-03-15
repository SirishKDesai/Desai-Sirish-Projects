import pandas as pd
import numpy as np
import unittest
from MonteCarlo.montecarlo import Games
from MonteCarlo.montecarlo import DieGame
from MonteCarlo.montecarlo import Analyzer


class MonteCarloTests(unittest.TestCase):

    
    def test_DieInit(self):
        test_object = DieGame([1,2,3,4])
        x = test_object._FacesWeights['Face']
        self.assertEqual([1, 2, 3, 4], list(x))
    
    def test_DieChangeWeight(self):
        test_object1 = DieGame([1,2,3,4])
        test_object1.change_weight(2,3)
        x = test_object1._FacesWeights['Weights']
        self.assertTrue(3 == list(x)[1])
    
    def test_DieRollDie(self):
        test_object2 = DieGame([1,2,3,4])
        y = test_object2.roll_die()
        self.assertTrue(y[0] in [1,2,3,4])
    
    def test_DieShow(self):
        test_object3 = DieGame([1,2,3,4])
        x = test_object3._FacesWeights['Face']
        y = test_object3._FacesWeights['Weights']
        self.assertEqual(list(x), list(test_object3.show()['Face']))
        self.assertEqual(list(y), list(test_object3.show()['Weights']))

    def test_GamesInit(self):
        test_game = Games([1,2,3,4])
        x = test_game.dieobjects
        self.assertTrue(x == [1,2,3,4])

    def test_GamesPlay(self):
        die1 = {1:1,2:1,3:1,4:1}
        dice = {1:die1}
        for k,v in dice.items():
            dice[k] = DieGame(v.keys())
            for key in v.keys():
                dice[k].change_weight(key, v[key])
        test_game1 = Games(dice.values())
        test_game1.play(1)
        x = test_game1._rolled
        self.assertTrue(list(x)[0] in [1,2,3,4])

    def test_GameShow(self):
        die1 = {1:1,2:1,3:1,4:1}
        dice = {1:die1}
        for k,v in dice.items():
            dice[k] = DieGame(v.keys())
            for key in v.keys():
                dice[k].change_weight(key, v[key])
        test_game2 = Games(dice.values())
        test_game2.play(1)
        self.assertTrue(list(test_game2._rolled) == list(test_game2.show('wide')))
        self.assertFalse((test_game2._rolled.shape) == (test_game2.show('narrow').shape))
        self.assertFalse(test_game2.show('anythingelse') == list(test_game2._rolled))

    def test_AnalyzerInit(self):
        die1 = {1:1,2:1,3:1,4:1}
        dice = {1:die1}
        for k,v in dice.items():
            dice[k] = DieGame(v.keys())
            for key in v.keys():
                dice[k].change_weight(key, v[key])
        test_analyzer = Games(dice.values())
        test_analyzer.play(1)
        analyzer = Analyzer(test_analyzer)
        self.assertTrue([1,2,3,4] == analyzer._faces)
        self.assertTrue(analyzer.objects.show().values in [1,2,3,4])

    def test_AnalyzerFaceperRoll(self):
        die1 = {1:1,2:1,3:1,4:1}
        dice = {1:die1}
        for iterable,theDie in dice.items():
            dice[iterable] = DieGame(theDie.keys())
            for key in theDie.keys():
                dice[iterable].change_weight(key, theDie[key])
        test_analyzer = Games(dice.values())
        test_analyzer.play(1)
        analyzer1 = Analyzer(test_analyzer)    
        analyzer1.faceperroll()
        y = list(analyzer1.data)
        for things in y:
            self.assertTrue(things in die1.keys())

    def test_AnalyzerCombo(self):
        die1 = {1:1,2:1,3:1,4:1}
        dice = {1:die1}
        for iterable,theDie in dice.items():
            dice[iterable] = DieGame(theDie.keys())
            for key in theDie.keys():
                dice[iterable].change_weight(key, theDie[key])
        test_analyzer = Games(dice.values())
        rollnumber = 10
        test_analyzer.play(rollnumber)
        analyzer2 = Analyzer(test_analyzer)    
        analyzer2.faceperroll()
        analyzer2.combo()
        self.assertTrue(sum(analyzer2.something['count']) == rollnumber)
    
    def test_AnalyzerJackpot(self):
        die1 = {1:1,2:1,3:1,4:1}
        dice = {1:die1}
        for iterable,theDie in dice.items():
            dice[iterable] = DieGame(theDie.keys())
            for key in theDie.keys():
                dice[iterable].change_weight(key, theDie[key])
        test_analyzer = Games(dice.values())
        rollnumber = 10
        test_analyzer.play(rollnumber)
        analyzer3 = Analyzer(test_analyzer)    
        analyzer3.faceperroll()
        analyzer3.combo()
        analyzer3.jackpot()
        self.assertTrue(analyzer3.jackpot() == rollnumber)
        
    
if __name__ == '__main__':
    
    unittest.main(verbosity=2)