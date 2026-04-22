from patient_zero.experiments import get_estimate_error, get_rank

class TestExperiments:
    def test_estimate_error_guessing_correctly(self):
        """
        Test the get_estimate_error function gives correct result when patient-zero node has the highest score.
        """
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
        """
        Test if get_rank returns 0 when answer is correct.
        """
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
        """
        Test if get_rank returns the correct amount when answer is bad.
        """
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
        """
        Test if get_rank returns 0 if scores are tied with patient-zero
        """
        result = {
            1: 2,
            2: 2,
            3: 2
        }
        patient_zero = 2

        rank = get_rank(result, patient_zero)

        assert rank == 0 # nodes tied with patient_zero are not included in the rank
