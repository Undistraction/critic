import pytest
from flask import Flask

from app import app
from unittest.mock import patch

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_analyse_color_valid(client, mocker):
    mock_image = 'mock_image_data'
    mock_result = {'colors': ['#FFFFFF', '#000000']}
    
    mocker.patch('src.utils.image_utils.load_image', return_value=mock_image)
    mocker.patch('src.image_analyser.analyse_image', return_value=mock_result)
    
    response = client.post('/analyse-color', json={'image_url': 'valid_path', 'n_colors': 5})
    
    assert response.status_code == 200
    assert response.json == mock_result

def test_analyse_color_no_image_url(client):
    response = client.post('/analyse-color', json={'n_colors': 5})
    
    assert response.status_code == 400
    assert response.json == {'error': 'You must supply an image url'}

def test_analyse_color_invalid_image_url(client, mocker):
    response = client.post('/analyse-color', json={'image_url': 'invalid_path'})
    
    assert response.status_code == 404
    assert response.json == {'error': "The image couldn't be found at: 'invalid_path'"}

# def test_analyse_color_unexpected_exception(client, mocker):
#     mocker.patch('src.utils.image_utils.load_image', side_effect=Exception('Unexpected error'))
#     response = client.post('/analyse-color', json={'image_url': 'valid_path'})
    
#     assert response.status_code == 500
#     assert response.json == {'error': 'Unexpected error'}