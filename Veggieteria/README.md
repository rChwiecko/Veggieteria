# React + Vite

This template provides a minimal setup to get React working in Vite with HMR and some ESLint rules.

Currently, two official plugins are available:

- [@vitejs/plugin-react](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react/README.md) uses [Babel](https://babeljs.io/) for Fast Refresh
- [@vitejs/plugin-react-swc](https://github.com/vitejs/vite-plugin-react-swc) uses [SWC](https://swc.rs/) for Fast Refresh


Overview
VeggieTeria is an application that encourages healthy eating habits by rewarding users with CarrotCoins for consuming vegetables. The application uses a webcam to detect eating actions and verifies the presence of vegetables using Google Cloud Vision. Users can earn CarrotCoins and manage their balances via the Polkadot AssetHub.

Prerequisites
Python 3.7+
Node.js and npm
Google Cloud Vision
Polkadot AssetHub account
Python
Backend Setup
Clone the repository:

bash
Copy code
git clone https://github.com/your-repo/Veggieteria.git
cd Veggieteria
Install Python dependencies:

bash
Copy code
pip install -r requirements.txt
Set up Google Cloud Vision API:

Create a Google Cloud project and enable the Vision API.
Download the JSON key file and place it in the Backend directory.
Set the environment variable for the Google Cloud credentials:
bash
Copy code
export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/keyfile.json"
Configure the backend:

Modify the mnemonic and recipient_address in EatingAction.py with your own Polkadot mnemonic and recipient address.
Run the backend script:

bash
Copy code
python EatingAction.py
Frontend Setup
Navigate to the Frontend directory:

bash
Copy code
cd Frontend
Install Node.js dependencies:

bash
Copy code
npm install
Install Vite:

bash
Copy code
npm install vite
Run the React app:

bash
Copy code
npm run dev
Using the Application
Start the backend server:

bash
Copy code
python EatingAction.py
Open the React app:

Navigate to http://localhost:3000/ in your web browser.
Enter your wallet address (or leave blank and hit submit for default test wallet address):

Input your Polkadot wallet address to start earning CarrotCoins.
Start an eating session:

Click on "Start session" to begin the webcam monitoring.
Earn CarrotCoins by eating vegetables in front of the webcam.
Shop and manage coins:

Access the shop to manage your earned CarrotCoins and view the NFT or produce store.

Key Components
Backend:

EatingAction.py: Main script for detecting eating actions and transferring CarrotCoins.
veggiedetection.py: Utility functions for detecting vegetables using Google Cloud Vision.
asset_hub.py: Utility functions for interacting with Polkadot AssetHub.
requirements.txt: List of required Python packages.
Frontend:

App.js: Main React component for the application.
App.css: CSS styles for the application.
index.js: Entry point for the React application.
Contributing
Fork the repository.
Create a new branch (git checkout -b feature-branch).
Commit your changes (git commit -am 'Add new feature').
Push to the branch (git push origin feature-branch).
Create a new Pull Request.
License
This project is licensed under the MIT License - see the LICENSE file for details.

Acknowledgments
Google Cloud Vision for image recognition.
MediaPipe for pose and hand tracking.
Polkadot AssetHub for blockchain integration.
React and Flask for frontend and backend frameworks.