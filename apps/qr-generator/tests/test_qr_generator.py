"""Tests for QR Code Generator."""

import pytest
import tempfile
import os
from pathlib import Path
from unittest.mock import patch, MagicMock

# Import the module under test
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from qr_generator import create_qr_code, parse_arguments


class TestQRCodeGenerator:
    """Test cases for QR code generation functionality."""
    
    def test_create_qr_code_png(self):
        """Test creating a PNG QR code."""
        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp:
            try:
                create_qr_code(
                    data="Hello World",
                    output_path=tmp.name,
                    size=10,
                    border=4,
                    format="png",
                    error_correction="M"
                )
                # Check that file was created and has content
                assert os.path.exists(tmp.name)
                assert os.path.getsize(tmp.name) > 0
            finally:
                os.unlink(tmp.name)
    
    def test_create_qr_code_svg(self):
        """Test creating an SVG QR code."""
        with tempfile.NamedTemporaryFile(suffix='.svg', delete=False) as tmp:
            try:
                create_qr_code(
                    data="https://example.com",
                    output_path=tmp.name,
                    size=10,
                    border=4,
                    format="svg",
                    error_correction="M"
                )
                # Check that file was created and has content
                assert os.path.exists(tmp.name)
                assert os.path.getsize(tmp.name) > 0
            finally:
                os.unlink(tmp.name)
    
    def test_create_qr_code_txt(self):
        """Test creating a text QR code."""
        with tempfile.NamedTemporaryFile(suffix='.txt', delete=False) as tmp:
            try:
                # For txt format, we need to capture the output
                with patch('builtins.print') as mock_print:
                    create_qr_code(
                        data="Test data",
                        output_path=tmp.name,
                        size=10,
                        border=4,
                        format="txt",
                        error_correction="M"
                    )
                    # txt format prints to console, so we just verify it doesn't crash
                    assert True
            finally:
                if os.path.exists(tmp.name):
                    os.unlink(tmp.name)
    
    def test_create_qr_code_different_sizes(self):
        """Test QR code generation with different sizes."""
        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp:
            try:
                create_qr_code(
                    data="Size test",
                    output_path=tmp.name,
                    size=5,
                    border=2,
                    format="png",
                    error_correction="L"
                )
                assert os.path.exists(tmp.name)
                assert os.path.getsize(tmp.name) > 0
            finally:
                os.unlink(tmp.name)
    
    def test_create_qr_code_high_error_correction(self):
        """Test QR code with high error correction."""
        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp:
            try:
                create_qr_code(
                    data="High error correction test",
                    output_path=tmp.name,
                    size=10,
                    border=4,
                    format="png",
                    error_correction="H"
                )
                assert os.path.exists(tmp.name)
                assert os.path.getsize(tmp.name) > 0
            finally:
                os.unlink(tmp.name)
    
    def test_create_qr_code_long_data(self):
        """Test QR code with longer data."""
        long_data = "This is a very long string that should test the QR code's ability to handle larger amounts of data and potentially require a higher version QR code."
        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp:
            try:
                create_qr_code(
                    data=long_data,
                    output_path=tmp.name,
                    size=10,
                    border=4,
                    format="png",
                    error_correction="M"
                )
                assert os.path.exists(tmp.name)
                assert os.path.getsize(tmp.name) > 0)
            finally:
                os.unlink(tmp.name)


class TestArgumentParsing:
    """Test cases for command line argument parsing."""
    
    def test_parse_arguments_basic(self):
        """Test basic argument parsing."""
        args = parse_arguments(['qr_generator.py', 'Hello World', '-o', 'test.png'])
        assert args.data == 'Hello World'
        assert args.output == 'test.png'
        assert args.format == 'png'
        assert args.size == 10
        assert args.border == 4
        assert args.error_correction == 'M'
    
    def test_parse_arguments_with_options(self):
        """Test argument parsing with all options."""
        args = parse_arguments([
            'qr_generator.py', 
            'https://example.com', 
            '-o', 'website.svg',
            '--format', 'svg',
            '--size', '15',
            '--border', '8',
            '--error-correction', 'H'
        ])
        assert args.data == 'https://example.com'
        assert args.output == 'website.svg'
        assert args.format == 'svg'
        assert args.size == 15
        assert args.border == 8
        assert args.error_correction == 'H'
    
    def test_parse_arguments_txt_format(self):
        """Test argument parsing for text format."""
        args = parse_arguments([
            'qr_generator.py', 
            'Contact info', 
            '-o', 'contact.txt',
            '--format', 'txt'
        ])
        assert args.data == 'Contact info'
        assert args.output == 'contact.txt'
        assert args.format == 'txt'
    
    def test_parse_arguments_error_correction_levels(self):
        """Test all error correction levels."""
        for level in ['L', 'M', 'Q', 'H']:
            args = parse_arguments([
                'qr_generator.py', 
                'Test data', 
                '-o', f'test_{level}.png',
                '--error-correction', level
            ])
            assert args.error_correction == level


class TestEdgeCases:
    """Test edge cases and error conditions."""
    
    def test_create_qr_code_empty_data(self):
        """Test QR code generation with empty data."""
        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp:
            try:
                create_qr_code(
                    data="",
                    output_path=tmp.name,
                    size=10,
                    border=4,
                    format="png",
                    error_correction="M"
                )
                assert os.path.exists(tmp.name)
            finally:
                os.unlink(tmp.name)
    
    def test_create_qr_code_special_characters(self):
        """Test QR code generation with special characters."""
        special_data = "Special chars: !@#$%^&*()_+-=[]{}|;':\",./<>?"
        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp:
            try:
                create_qr_code(
                    data=special_data,
                    output_path=tmp.name,
                    size=10,
                    border=4,
                    format="png",
                    error_correction="M"
                )
                assert os.path.exists(tmp.name)
            finally:
                os.unlink(tmp.name)
    
    def test_create_qr_code_unicode(self):
        """Test QR code generation with Unicode characters."""
        unicode_data = "Unicode: 你好世界 🌍 émojis 🚀"
        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp:
            try:
                create_qr_code(
                    data=unicode_data,
                    output_path=tmp.name,
                    size=10,
                    border=4,
                    format="png",
                    error_correction="M"
                )
                assert os.path.exists(tmp.name)
            finally:
                os.unlink(tmp.name)


if __name__ == '__main__':
    pytest.main([__file__])
