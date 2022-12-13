const express = require('express');

const app = express();

app.get('/', (req, res) => {
    console.log(`Got a request from ${req.ip}`);
    res.send(`Hello from Server ${process.env.SERVER_NUMBER}`);
});

app.listen(process.env.PORT, () => {
    console.log(`Server is running on port ${process.env.PORT}`);
});

