const express = require('express');
const app = express();
const port = process.env.PORT || 3000;
const Cloudant = require('@cloudant/cloudant');
const axios = require('axios'); // Import axios for making HTTP requests

// Initialize Cloudant connection with IAM authentication
async function dbCloudantConnect() {
    try {
        const cloudant = Cloudant({
            plugins: { iamauth: { iamApiKey: 'acGzE9Wk-Xe8ivRRjhg2Fu161mRQtZinsuzDWCBB6KEl' } },
            url: 'https://2499599b-eb24-4be7-aed5-4ef1aab36104-bluemix.cloudantnosqldb.appdomain.cloud'
        });

        const db = cloudant.use('dealerships');
        console.info('Connect success! Connected to DB');
        return db;
    } catch (err) {
        console.error('Connect failure: ' + err.message + ' for Cloudant DB');
        throw err;
    }
}

let db;

(async () => {
    db = await dbCloudantConnect();
})();

app.use(express.json());

// Define a route to get all dealerships with optional state and ID filters
app.get('/dealerships/get', async (req, res) => {
    const { state, id } = req.query;

    console.log('State parameter:', state); // Log the state parameter

    // Create a selector object based on query parameters
    const selector = {};
    if (state) {
        selector.state = state;
        console.log('Selector:', selector); // Log the selector object
    }
    
    if (id) {
        selector.id = parseInt(id); // Filter by "id" with a value of 1
    }

    const queryOptions = {
        selector,
        limit: 10, // Limit the number of documents returned to 10
    };

    console.log('Query options:', queryOptions); // Log the query options

    try {
        // Send a request to the specified URL
        const response = await axios.get('https://adeshademmin-3000.theiadockernext-0-labs-prod-theiak8s-4-tor01.proxy.cognitiveclass.ai/dealerships/get', {
            params: {
                st: state // Pass the state parameter to the URL
            }
        });

        // Assuming the response is in JSON format, you can return it as a JSON response
        const data = response.data;
        res.json(data);
    } catch (error) {
        console.error('Error fetching dealerships:', error);
        res.status(500).json({ error: 'An error occurred while fetching dealerships.' });
    }
});

app.listen(port, () => {
    console.log(`Server is running on port ${port}`);
});
