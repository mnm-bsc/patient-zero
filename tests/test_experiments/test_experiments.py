from patient_zero.experiments import get_estimate_error, get_rank

class TestExperiments:
    def test_estimate_error(self):
        result = {
            1: 1, 
            2: 2, 
            3: 3, 
            4: 4, 
            5: 2, 
            6: 2
        }
        shortest_path_lengths = {
            1: 2, 
            2: 1, 
            3: 1,
            4: 0, 
            5: 2, 
            6: 1
        }

        estimate, estimate_error = get_estimate_error(result, shortest_path_lengths)

        assert estimate == 4
        assert estimate == max(result, key=result.get)
        assert estimate_error == 0
        assert estimate_error == shortest_path_lengths[estimate]

    def test_rank_when_estimate_is_good(self):
        result = {
            1: 1, 
            2: 2, 
            3: 3, 
            4: 4, 
            5: 2, 
            6: 2
        }
        patient_zero = 4
        
        rank = get_rank(result, patient_zero)

        assert rank == 0

    def test_rank_when_estimate_is_bad(self):
        result = {
            1: 1, 
            2: 2, 
            3: 3, 
            4: 4, 
            5: 2, 
            6: 2
        }
        patient_zero = 6

        rank = get_rank(result, patient_zero)

        assert rank == 2 # node 4 and 3 is scored higher than 3
        
    def test_rank_with_ties(self):
        result = {
            1: 2,
            2: 2,
            3: 2
        }

        rank = get_rank(result, 2)

        assert rank == 0
