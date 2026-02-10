import json

def generate_navigation_structure(num_elements):
    # Define the list for storing the navigation elements
    navigation_list = []

    # Add the BEGIN NODE
    begin_node = {
        "extents": "SurveyTemplateObject",
        "objectType": "Navigation",
        "origin": "BEGIN NODE",
        "index": 0,
        "inNavigations": [],
        "routes": [{"extents": "SurveyTemplateObject",
                    "objectType": "Route",
                    "origin": "BEGIN NODE",
                    "destination": "TML1",
                    "name": "BEGIN NODE_TML1",
                    "isDefault": True,
                    "conditions": []}]
    }
    navigation_list.append(begin_node)

    # Add the END NODE with placeholder for inNavigations, to fill after adding intermediate nodes
    end_node = {
        "extents": "SurveyTemplateObject",
        "objectType": "Navigation",
        "origin": "END NODE",
        "index": 1,
        "inNavigations": [None] * 2,  # Placeholder for inNavigations
        "routes": []
    }
    navigation_list.append(end_node)

    # Add intermediate TML nodes
    for i in range(num_elements):
        origin = f"TML{i + 1}"
        # Destination TML or END NODE
        destination = f"TML{i + 2}" if i + 1 < num_elements else "END NODE"

        # Create TML node
        tml_node = {
            "extents": "SurveyTemplateObject",
            "objectType": "Navigation",
            "origin": origin,
            "index": i + 2,
            "inNavigations": [{"origin": f"BEGIN NODE" if i == 0 else f"TML{i}", "index": i + 1}],
            "routes": [{"extents": "SurveyTemplateObject",
                        "objectType": "Route",
                        "origin": origin,
                        "destination": destination,
                        "name": f"{origin}_{destination}",
                        "isDefault": True,
                        "conditions": []}]
        }
        navigation_list.append(tml_node)

    # Fill inNavigations for END NODE to point to the last TML node
    if num_elements > 0:
        end_node["inNavigations"] = [None, {"origin": f"TML{num_elements}", "index": 1 + num_elements + 1}]

    return {"navigationList": navigation_list}
