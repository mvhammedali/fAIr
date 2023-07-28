![example workflow](https://github.com/omranlm/TDB/actions/workflows/backend_build.yml/badge.svg)
![example workflow](https://github.com/omranlm/TDB/actions/workflows/frontend_build.yml/badge.svg)
Navigate to Backend or Frontend to get Installation Instructions.
 
# fAIr: AI-assisted Mapping
fAIr is an open AI-assisted mapping service developed by the [Humanitarian OpenStreetMap Team (HOT)](https://www.hotosm.org/) that aims to improve the efficiency and accuracy of mapping efforts for humanitarian purposes. The service uses AI models, specifically computer vision techniques, to detect objects such as buildings, roads, waterways, and trees from satellite and UAV imagery.

The name fAIr is derived from the following terms:

- **f**: for freedom and free and open-source software
- **AI**: for Artificial Intelligence
- **r**: for resilience and our responsibility for our communities and the role we play within humanitarian mapping

## Features
- Intuitive and fair AI-assisted mapping tool
- Open-source AI models created and trained by local communities
- Uses open-source satellite and UAV imagery from HOT's OpenAerialMap (OAM) to detect map features and suggest additions to OpenStreetMap (OSM)
- Constant feedback loop to eliminate model biases and ensure models are relevant to local communities

Unlike other AI data producers, fAIr is a free and open-source AI service that allows OSM community members to create and train their own AI models for mapping in their region of interest and/or humanitarian need. The goal of fAIr is to provide access to AI-assisted mapping across mobile and in-browser editors, using community-created AI models, and to ensure that the models are relevant to the communities where the maps are being created to improve the conditions of the people living there.

To eliminate model biases, fAIr is built to work with the local communities and receive constant feedback on the models, which will result in the progressive intelligence of computer vision models. The AI models suggest detected features to be added to OpenStreetMap (OSM), but mass import into OSM is not planned. Whenever an OSM mapper uses the AI models for assisted mapping and completes corrections, fAIr can take those corrections as feedback to enhance the AI model’s accuracy.

# Product Roadmap
See below a suggested product roadmap [subject to change] that provides high-level overview for planned work.
![image](https://user-images.githubusercontent.com/98902727/218769416-b3c71d3b-7c20-4d40-ab1e-88442d06445d.png)

# General Workflow of fAIr 

![fAIr1](https://github.com/hotosm/fAIr/assets/97789856/01c0e3b6-a00c-439d-a2ed-1c14b62e6364)

1. Project Area by tha project manager and imagery from Open Areal Map is submitted to the task manager which then is sent to Open Street Map after undergoing the process of manual mapping and validation.
2. Local dataset(created using the imagery and raw API data as inputs) is trained and local model is created and trained.
3. It is then validated , published , mapped and pushed back into Open Street Map.
4. Finally according to the feedback , the published model is sent for improvement and training .
<hr>

# fAIr Architecture
![fAIr2](https://github.com/hotosm/fAIr/assets/97789856/63394f65-ce0d-4a3d-8683-7455f14fb366)

1. Third party extensions are sent to fAIr backend which then generates data for OSM raw data API , osmconflator and geoson2osm xml .
2. Data from fAIr backend is sent to fAIr utilities . The backend is using s separate library we call it fAIr-utilities to handle:

     1. Data preparation for the models
     2. models trainings
     3. inference process
     4. post processing (converting the predicted features to geo data)
3. The public API is then sent to the fAIr frontend.





