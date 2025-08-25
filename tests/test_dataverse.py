import unittest
import pandas as pd
from gget.gget_dataverse import dataverse, calculate_md5_checksum, get_file_metadata, verify_file_checksum
import os
import shutil
import tempfile
import hashlib

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

    def test_calculate_md5_checksum(self):
        """Test MD5 checksum calculation"""
        # Create a temporary file with known content
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
            test_content = "Hello, World!"
            f.write(test_content)
            temp_file = f.name
        
        try:
            # Calculate checksum
            checksum = calculate_md5_checksum(temp_file)
            
            # Calculate expected checksum
            expected = hashlib.md5(test_content.encode()).hexdigest()
            
            self.assertEqual(checksum, expected)
        finally:
            os.unlink(temp_file)
    
    def test_calculate_md5_checksum_nonexistent_file(self):
        """Test MD5 checksum calculation with non-existent file"""
        with self.assertRaises(RuntimeError):
            calculate_md5_checksum('/path/that/does/not/exist.txt')
    
    def test_get_file_metadata_mock(self):
        """Test file metadata retrieval (mocked since we don't have network access)"""
        # This test would require mocking the requests.get call
        # For now, we just test that the function exists and handles errors gracefully
        metadata = get_file_metadata('nonexistent_id')
        # Should return None if there's a network error or file doesn't exist
        self.assertIsNone(metadata)
    
    def test_verify_file_checksum_no_file(self):
        """Test checksum verification with non-existent file"""
        result = verify_file_checksum('/path/that/does/not/exist.txt', '12345', verbose=False)
        self.assertFalse(result)
    
    def test_dataverse_with_checksum_parameter(self):
        """Test that dataverse function accepts verify_checksum parameter"""
        df = pd.DataFrame({
            'id': [6180617],
            'name': ['test_nodes'],
            'type': ['tab']
        })
        
        # Test that the function accepts the verify_checksum parameter without errors
        try:
            dataverse(df, path='/tmp/test_dataverse_checksum', verify_checksum=True, verbose=False)
            # Clean up if directory was created
            if os.path.exists('/tmp/test_dataverse_checksum'):
                shutil.rmtree('/tmp/test_dataverse_checksum')
        except Exception as e:
            # If it fails due to network/download issues, that's okay for testing
            if "Failed to download" in str(e) or "connection" in str(e).lower():
                pass  # Network failure is acceptable for validation test
            else:
                raise e

if __name__ == '__main__':
    unittest.main()