from src.image_analyser import analyse_image
from flask import Flask, request, jsonify

from src.utils.image_utils import load_image

# ------------------------------------------------------------------------------
# Entry 
# ------------------------------------------------------------------------------

app = Flask(__name__)

@app.route('/analyse-color', methods=['POST'])
def analyse_color():
    data = request.get_json()
    image_url = data.get('image_url')
    # Default to 5 colors if not provided
    n_colors = data.get('n_colors', 5)  
    print('Args',image_url, n_colors)

    if not image_url:
        return jsonify({'error': 'You must supply an image url'}), 400

    try:
        image = load_image(image_url) 
        result = analyse_image(image, n_colors)
        print('Result',result)
        return jsonify(result)
    except FileNotFoundError:
        error = f"The image couldn't be found at: '{image_url}'"
        return jsonify({'error': error}), 404
    except Exception as e:
        print('Exception',e)
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
