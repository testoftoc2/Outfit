from flask import Flask, request, jsonify
import json
import os

app = Flask(__name__)

with open('itemData.json') as f:
    item_data = json.load(f)

@app.route('/item', methods=['GET'])
def get_icon():
    item_id = request.args.get('id', type=int)
    key = request.args.get("key", "")
    
    if key is None:
        return jsonify({"error": "INVALID REQUEST. 'key' PARAMETER IS MISSING"}), 403
        
    if key != "TOC":
        return jsonify({"error": "INVALID API KEY"}), 403

    if item_id is None:
        return jsonify({"error": "INVALID REQUEST. 'id' PARAMETER IS MISSING"}), 400

    for item in item_data:
        if item.get("Id") == item_id:
            icon_name = item.get("Icon")
            item_name = item.get("name")

            if icon_name.startswith("Icon_callsign_storebg"):
                icon_name = icon_name.replace("Icon_callsign_storebg", "Icon_callsign_basebg", 1)

            image_url = f"https://freefiremobile-a.akamaihd.net/common/Local/PK/FF_UI_Icon/{icon_name}.png"
            return jsonify({
                "Id": item_id,
                "Name": item_name,
                "Icon": icon_name,
                "Image": image_url
            })

    return jsonify({"error": f"NO ITEM FOUND WITH ID{item_id}"}), 404

if __name__ == '__main__':
    app.run(debug=True)
