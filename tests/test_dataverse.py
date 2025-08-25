import unittest
import pandas as pd
from gget.gget_dataverse import dataverse
import os
import shutil

class TestDataverse(unittest.TestCase):
    def test_dataverse_validation(self):
        """Test that dataverse function validates input properly"""
        # Test with valid DataFrame
        df = pd.DataFrame({
            'id': [6180617],
            'name': ['test_nodes'],
            'type': ['tab']
        })
        
        # Test validation without actually downloading
        try:
            # This should not raise an error
            dataverse(df, path='/tmp/test_dataverse_validation', verbose=False)
            # If we get here, validation passed. Clean up if directory was created
            if os.path.exists('/tmp/test_dataverse_validation'):
                shutil.rmtree('/tmp/test_dataverse_validation')
        except Exception as e:
            # If it fails due to network/download issues, that's okay for testing
            if "Failed to download" in str(e) or "connection" in str(e).lower():
                pass  # Network failure is acceptable for validation test
            else:
                raise e

    def test_dataverse_invalid_input(self):
        """Test that dataverse function raises appropriate errors for invalid input"""
        # Test with missing columns
        df_missing_cols = pd.DataFrame({
            'wrong': ['columns']
        })
        
        with self.assertRaises(ValueError) as context:
            dataverse(df_missing_cols, path='/tmp/test', verbose=False)
        self.assertIn("missing required columns", str(context.exception))
        
        # Test with empty DataFrame
        df_empty = pd.DataFrame({
            'id': [],
            'name': [],
            'type': []
        })
        
        with self.assertRaises(ValueError) as context:
            dataverse(df_empty, path='/tmp/test', verbose=False)
        self.assertIn("empty", str(context.exception))
        
        # Test with invalid file path
        with self.assertRaises(FileNotFoundError):
            dataverse('/path/that/does/not/exist.csv', path='/tmp/test', verbose=False)

if __name__ == '__main__':
    unittest.main()